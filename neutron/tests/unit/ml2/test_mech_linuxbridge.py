# Copyright (c) 2013 OpenStack Foundation
# All Rights Reserved.
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

from neutron.common import constants
from neutron.extensions import portbindings
from neutron.plugins.ml2.drivers import mech_linuxbridge
from neutron.tests.unit.ml2 import _test_mech_agent as base


class LinuxbridgeMechanismBaseTestCase(base.AgentMechanismBaseTestCase):
    VIF_TYPE = portbindings.VIF_TYPE_BRIDGE
    CAP_PORT_FILTER = True
    AGENT_TYPE = constants.AGENT_TYPE_LINUXBRIDGE

    GOOD_MAPPINGS = {'fake_physical_network': 'fake_interface'}
    GOOD_CONFIGS = {'interface_mappings': GOOD_MAPPINGS}

    BAD_MAPPINGS = {'wrong_physical_network': 'wrong_interface'}
    BAD_CONFIGS = {'interface_mappings': BAD_MAPPINGS}

    AGENTS = [{'alive': True,
               'configurations': GOOD_CONFIGS}]
    AGENTS_DEAD = [{'alive': False,
                    'configurations': GOOD_CONFIGS}]
    AGENTS_BAD = [{'alive': False,
                   'configurations': GOOD_CONFIGS},
                  {'alive': True,
                   'configurations': BAD_CONFIGS}]

    def setUp(self):
        super(LinuxbridgeMechanismBaseTestCase, self).setUp()
        self.driver = mech_linuxbridge.LinuxbridgeMechanismDriver()
        self.driver.initialize()


class LinuxbridgeMechanismGenericTestCase(LinuxbridgeMechanismBaseTestCase,
                                          base.AgentMechanismGenericTestCase):
    pass


class LinuxbridgeMechanismLocalTestCase(LinuxbridgeMechanismBaseTestCase,
                                        base.AgentMechanismLocalTestCase):
    pass


class LinuxbridgeMechanismFlatTestCase(LinuxbridgeMechanismBaseTestCase,
                                       base.AgentMechanismFlatTestCase):
    pass


class LinuxbridgeMechanismVlanTestCase(LinuxbridgeMechanismBaseTestCase,
                                       base.AgentMechanismVlanTestCase):
    pass
