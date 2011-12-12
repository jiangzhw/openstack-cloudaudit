# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011, Piston Cloud Computing, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from cloudaudit.control import nist


class ControlRegistry(object):

    """
        This class acts as a registry and factory for all Control
         class implementations

        Registry head is a N-tiered dictionary with the following conventions:

        { Compliance Regimes } -> { Compliance Versions }
        -> { Control Ids } -> Class Instances
    """

    registryHead = {}

    def __init__(self):
        return 

    def register_control(self, new_control):
        if new_control.regime in self.registryHead.keys():
            versions_dict = self.registryHead[new_control.regime]
        else:
            self.registryHead[new_control.regime] = {}
            versions_dict = self.registryHead[new_control.regime]

        if new_control.regime_version in versions_dict.keys():
            control_dict = versions_dict[new_control.regime_version]
        else:
            versions_dict[new_control.regime_version] = {}
            control_dict = versions_dict[new_control.regime_version]

        if new_control.control_id in control_dict.keys():
            return
        else:
            control_dict[new_control.control_id] = new_control

    def get_all_controls(self):
        control_list = []
        for k, v in self.registryHead.items():
            for k1, v1 in v.items():
                for k2, v2 in v1.items():
                    control_list.append(v2)

        return control_list

    def get_control_from_url(self, url):
        # We match greedily at each stage, so first try
        # to match the entire Url and then remove the least most
        # significant url portion until we get a match

        temp_url = url
        temp_url = str.lstrip(temp_url, "/")

        while not temp_url in self.registryHead.keys():
            temp_url = str.rsplit(temp_url, "/", 1)
            if len(temp_url) == 1:
                raise Exception(
                    "Could not find a compliance regime for the Url:  "
                    + url)
            temp_url = temp_url[0]

        version_dict = self.registryHead[temp_url]

        index = len(temp_url) + 1

        sub_url = url[index:]
        temp_url = str.lstrip(sub_url, "/")

        while not temp_url in version_dict.keys():
            temp_url = str.rsplit(temp_url, "/", 1)
            if len(temp_url) == 1:
                raise Exception(
                    "Could not find a control version for the Url:  "
                    + url)
            temp_url = temp_url[0]

        control_dict = version_dict[temp_url]
        index = len(temp_url) + 1
        sub_url = sub_url[index:]
        temp_url = str.lstrip(sub_url, "/")

        while not temp_url in control_dict.keys():
            temp_url = str.rsplit(temp_url, "/", 1)
            if len(temp_url) == 1:
                raise Exception(
                    "Could not find a control id for the Url:  "
                    + url)
            temp_url = temp_url[0]

        control = control_dict[temp_url]
        return control

    def add_maps(self, mapper):

        for k, v in self.registryHead.items():
            for k2, v2 in v.items():
                for k3, v3 in v2.items():
                    str1 = v3.route
                    mapper.connect(None, str1, controller=v3,
                           conditions=dict(method=["GET"]))
                    str1 = str1 + "/{file:.*}"
                    mapper.connect(None, str1, controller=v3,
                           conditions=dict(method=["GET"]))

        return mapper

CONTROL_REGISTRY = ControlRegistry()

from cloudaudit.control.nist import nist_800_53_ac_7
our_control = nist_800_53_ac_7.NIST_800_53_ac7()
CONTROL_REGISTRY.register_control(our_control)

from cloudaudit.control.nist import nist_800_53_ac_9
our_control = nist_800_53_ac_9.NIST_800_53_ac9()
CONTROL_REGISTRY.register_control(our_control)

from cloudaudit.control.nist import nist_800_53_ac_10
our_control = nist_800_53_ac_10.NIST_800_53_ac10()
CONTROL_REGISTRY.register_control(our_control)

from cloudaudit.control.nist import nist_800_53_ac_11
our_control = nist_800_53_ac_11.NIST_800_53_ac11()
CONTROL_REGISTRY.register_control(our_control)