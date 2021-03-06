# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Cisco Systems, Inc.  All rights reserved.
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
# @author: Sumit Naiksatam, Cisco Systems, Inc.


# Attachment attributes
INSTANCE_ID = 'instance_id'
TENANT_ID = 'tenant_id'
TENANT_NAME = 'tenant_name'
HOST_NAME = 'host_name'

# Network attributes
NET_ID = 'id'
NET_NAME = 'name'
NET_VLAN_ID = 'vlan_id'
NET_VLAN_NAME = 'vlan_name'
NET_PORTS = 'ports'

# Network types
NETWORK_TYPE_FLAT = 'flat'
NETWORK_TYPE_LOCAL = 'local'
NETWORK_TYPE_VLAN = 'vlan'
NETWORK_TYPE_NONE = 'none'

CREDENTIAL_ID = 'credential_id'
CREDENTIAL_NAME = 'credential_name'
CREDENTIAL_USERNAME = 'user_name'
CREDENTIAL_PASSWORD = 'password'
CREDENTIAL_TYPE = 'type'
MASKED_PASSWORD = '********'

USERNAME = 'username'
PASSWORD = 'password'

LOGGER_COMPONENT_NAME = "cisco_plugin"

NEXUS_PLUGIN = 'nexus_plugin'
VSWITCH_PLUGIN = 'vswitch_plugin'

DEVICE_IP = 'device_ip'

NETWORK_ADMIN = 'network_admin'

NETWORK = 'network'
PORT = 'port'
BASE_PLUGIN_REF = 'base_plugin_ref'
CONTEXT = 'context'
SUBNET = 'subnet'

#### N1Kv CONSTANTS
# Special vlan_id value in n1kv_vlan_allocations table indicating flat network
FLAT_VLAN_ID = -1

# Topic for tunnel notifications between the plugin and agent
TUNNEL = 'tunnel'

# Maximum VXLAN range configurable for one network profile.
MAX_VXLAN_RANGE = 1000000

# Values for network_type
NETWORK_TYPE_FLAT = 'flat'
NETWORK_TYPE_VLAN = 'vlan'
NETWORK_TYPE_VXLAN = 'vxlan'
NETWORK_TYPE_LOCAL = 'local'
NETWORK_TYPE_NONE = 'none'
NETWORK_TYPE_TRUNK = 'trunk'
NETWORK_TYPE_MULTI_SEGMENT = 'multi-segment'

# Values for network sub_type
NETWORK_SUBTYPE_TRUNK_VLAN = NETWORK_TYPE_VLAN
NETWORK_SUBTYPE_TRUNK_VXLAN = NETWORK_TYPE_VXLAN

# Prefix for VM Network name
VM_NETWORK_NAME_PREFIX = 'vmn_'

SET = 'set'
INSTANCE = 'instance'
PROPERTIES = 'properties'
NAME = 'name'
ID = 'id'
POLICY = 'policy'
TENANT_ID_NOT_SET = 'TENANT_ID_NOT_SET'
ENCAPSULATIONS = 'encapsulations'
STATE = 'state'
ONLINE = 'online'
MAPPINGS = 'mappings'
MAPPING = 'mapping'
SEGMENTS = 'segments'
SEGMENT = 'segment'
BRIDGE_DOMAIN_SUFFIX = '_bd'
ENCAPSULATION_PROFILE_SUFFIX = '_profile'

UUID_LENGTH = 36
