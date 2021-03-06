# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 NEC Corporation
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Akihiro Motoki, NEC Corporation

from testtools import matchers
from webob import exc

from neutron.common import exceptions as q_exc
from neutron import context
from neutron.extensions import portbindings
from neutron.tests.unit import _test_extension_portbindings as test_bindings
from neutron.tests.unit.nec import test_nec_plugin
from neutron.tests.unit import test_security_groups_rpc as test_sg_rpc


class TestNecPortBinding(test_bindings.PortBindingsTestCase,
                         test_nec_plugin.NecPluginV2TestCase):
    VIF_TYPE = portbindings.VIF_TYPE_OVS
    HAS_PORT_FILTER = True
    FIREWALL_DRIVER = test_sg_rpc.FIREWALL_HYBRID_DRIVER

    def setUp(self):
        test_sg_rpc.set_firewall_driver(self.FIREWALL_DRIVER)
        super(TestNecPortBinding, self).setUp()


class TestNecPortBindingNoSG(TestNecPortBinding):
    HAS_PORT_FILTER = False
    FIREWALL_DRIVER = test_sg_rpc.FIREWALL_NOOP_DRIVER


class TestNecPortBindingHost(
    test_bindings.PortBindingsHostTestCaseMixin,
    test_nec_plugin.NecPluginV2TestCase):
    pass


class TestNecPortBindingPortInfo(test_nec_plugin.NecPluginV2TestCase):
    def _get_portinfo(self, datapath_id=None, port_no=None, prefix=None):
        if datapath_id is None:
            datapath_id = '0xabc'
        if port_no is None:
            port_no = 1
        if prefix is None:
            prefix = 'portinfo:'
        return {prefix + 'datapath_id': datapath_id,
                prefix + 'port_no': port_no}

    def _check_response_portbinding_profile(self, port, datapath_id=None,
                                            port_no=None):
        expected = self._get_portinfo(datapath_id, port_no, prefix='')
        profile = port[portbindings.PROFILE]
        self.assertEqual(len(profile), 2)
        self.assertEqual(profile['portinfo:datapath_id'],
                         expected['datapath_id'])
        self.assertEqual(profile['portinfo:port_no'],
                         expected['port_no'])

    def _check_response_portbinding_no_profile(self, port):
        self.assertIn('status', port)
        self.assertNotIn(portbindings.PROFILE, port)

    def _get_non_admin_context(self):
        return context.Context(user_id=None,
                               tenant_id=self._tenant_id,
                               is_admin=False,
                               read_deleted="no")

    def test_port_create_portinfo(self):
        profile_arg = {portbindings.PROFILE: self._get_portinfo()}
        with self.port(arg_list=(portbindings.PROFILE,),
                       **profile_arg) as port:
            port_id = port['port']['id']
            # Check a response of create_port
            self._check_response_portbinding_profile(port['port'])
            self.assertEqual(self.ofc.create_ofc_port.call_count, 1)
            # Check a response of get_port
            ctx = context.get_admin_context()
            port = self._show('ports', port_id, neutron_context=ctx)['port']
            self._check_response_portbinding_profile(port)
            # By default user is admin - now test non admin user
            ctx = self._get_non_admin_context()
            non_admin_port = self._show(
                'ports', port_id, neutron_context=ctx)['port']
            self._check_response_portbinding_no_profile(non_admin_port)
            # port-update with non admin user should fail
            self._update('ports', port_id,
                         {'port': profile_arg},
                         expected_code=404,
                         neutron_context=ctx)

    def test_port_update_portinfo(self):
        profile_arg = {portbindings.PROFILE: self._get_portinfo()}
        with self.port() as port:
            self.assertEqual(self.ofc.create_ofc_port.call_count, 0)
            port_id = port['port']['id']
            # Check a response of create_port
            self._check_response_portbinding_no_profile(port['port'])
            # Check a response of update_port
            ctx = context.get_admin_context()
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self.assertEqual(self.ofc.create_ofc_port.call_count, 1)
            self._check_response_portbinding_profile(port)
            port = self._show('ports', port_id, neutron_context=ctx)['port']
            self._check_response_portbinding_profile(port)

    def test_port_update_portinfo_detail(self):
        with self.port() as port:
            self.assertEqual(self.ofc.create_ofc_port.call_count, 0)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 0)
            port_id = port['port']['id']
            ctx = context.get_admin_context()

            # add portinfo
            profile_arg = {portbindings.PROFILE: self._get_portinfo()}
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self.assertEqual(self.ofc.create_ofc_port.call_count, 1)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 0)

            # portinfo unchanged
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self.assertEqual(self.ofc.create_ofc_port.call_count, 1)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 0)

            # modify portinfo
            profile_arg = {portbindings.PROFILE:
                           self._get_portinfo(datapath_id='0x1234567890',
                                              port_no=99)}
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self.assertEqual(self.ofc.create_ofc_port.call_count, 2)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 1)

            # delete portinfo
            profile_arg = {portbindings.PROFILE: {}}
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self.assertEqual(self.ofc.create_ofc_port.call_count, 2)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 2)

    def test_port_create_portinfo_with_empty_dict(self):
        profile_arg = {portbindings.PROFILE: {}}
        with self.port(arg_list=(portbindings.PROFILE,),
                       **profile_arg) as port:
            port_id = port['port']['id']

            # Check a response of create_port
            self._check_response_portbinding_no_profile(port['port'])
            self.assertEqual(self.ofc.create_ofc_port.call_count, 0)
            # add portinfo
            ctx = context.get_admin_context()
            profile_arg = {portbindings.PROFILE: self._get_portinfo()}
            port = self._update('ports', port_id, {'port': profile_arg},
                                neutron_context=ctx)['port']
            self._check_response_portbinding_profile(port)
            self.assertEqual(self.ofc.create_ofc_port.call_count, 1)
            self.assertEqual(self.ofc.delete_ofc_port.call_count, 0)

    def test_port_create_portinfo_non_admin(self):
        with self.network(set_context=True, tenant_id='test') as net1:
            with self.subnet(network=net1) as subnet1:
                profile_arg = {portbindings.PROFILE: self._get_portinfo()}
                try:
                    with self.port(subnet=subnet1,
                                   expected_res_status=403,
                                   arg_list=(portbindings.PROFILE,),
                                   set_context=True, tenant_id='test',
                                   **profile_arg):
                        pass
                except exc.HTTPClientError:
                    pass
                self.assertEqual(self.ofc.create_ofc_port.call_count, 0)

    def test_port_update_portinfo_non_admin(self):
        profile_arg = {portbindings.PROFILE: self._get_portinfo()}
        with self.network() as net1:
            with self.subnet(network=net1) as subnet1:
                with self.port(subnet=subnet1) as port:
                    # By default user is admin - now test non admin user
                    # Note that 404 is returned when prohibit by policy.
                    # See comment for PolicyNotAuthorized except clause
                    # in update() in neutron.api.v2.base.Controller.
                    port_id = port['port']['id']
                    ctx = self._get_non_admin_context()
                    port = self._update('ports', port_id,
                                        {'port': profile_arg},
                                        expected_code=404,
                                        neutron_context=ctx)
                self.assertEqual(self.ofc.create_ofc_port.call_count, 0)

    def test_port_create_portinfo_validation_called(self):
        # Check validate_portinfo is called.
        profile_arg = {portbindings.PROFILE:
                       {'portinfo:datapath_id': '0xabc',
                        'portinfo:port_no': 0xffff + 1}}
        try:
            with self.port(arg_list=(portbindings.PROFILE,),
                           expected_res_status=400,
                           **profile_arg):
                pass
        except exc.HTTPClientError:
            pass


class TestNecPortBindingValidatePortInfo(test_nec_plugin.NecPluginV2TestCase):

    def test_validate_portinfo_ok(self):
        profile = {'portinfo:datapath_id': '0x1234567890abcdef',
                   'portinfo:port_no': 123}
        portinfo = self.plugin._validate_portinfo(profile)
        self.assertEqual(portinfo['datapath_id'], '0x1234567890abcdef')
        self.assertEqual(portinfo['port_no'], 123)

    def test_validate_portinfo_ok_without_0x(self):
        profile = {'portinfo:datapath_id': '1234567890abcdef',
                   'portinfo:port_no': 123}
        portinfo = self.plugin._validate_portinfo(profile)
        self.assertEqual(portinfo['datapath_id'], '0x1234567890abcdef')
        self.assertEqual(portinfo['port_no'], 123)

    def _test_validate_exception(self, profile, expected_msg):
        e = self.assertRaises(q_exc.InvalidInput,
                              self.plugin._validate_portinfo, profile)
        self.assertThat(str(e), matchers.StartsWith(expected_msg))

    def test_validate_portinfo_dict_validation(self):
        expected_msg = ("Invalid input for operation: "
                        "Validation of dictionary's keys failed.")

        profile = {'portinfo:port_no': 123}
        self._test_validate_exception(profile, expected_msg)

        profile = {'portinfo:datapath_id': '0xabcdef'}
        self._test_validate_exception(profile, expected_msg)

    def test_validate_portinfo_negative_port_number(self):
        profile = {'portinfo:datapath_id': '0x1234567890abcdef',
                   'portinfo:port_no': -1}
        expected_msg = ("Invalid input for operation: "
                        "'-1' should be non-negative.")
        self._test_validate_exception(profile, expected_msg)

    def test_validate_portinfo_invalid_datapath_id(self):
        expected_msg = ("Invalid input for operation: "
                        "portinfo:datapath_id should be a hex string")

        # non hexidecimal datapath_id
        profile = {'portinfo:datapath_id': 'INVALID',
                   'portinfo:port_no': 123}
        self._test_validate_exception(profile, expected_msg)

        # Too big datapath_id
        profile = {'portinfo:datapath_id': '0x10000000000000000',
                   'portinfo:port_no': 123}
        self._test_validate_exception(profile, expected_msg)

    def test_validate_portinfo_too_big_port_number(self):
        profile = {'portinfo:datapath_id': '0x1234567890abcdef',
                   'portinfo:port_no': 65536}
        expected_msg = ("Invalid input for operation: "
                        "portinfo:port_no should be [0:65535]")
        self._test_validate_exception(profile, expected_msg)
