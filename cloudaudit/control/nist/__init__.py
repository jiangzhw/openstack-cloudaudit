# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Piston Cloud Computing, Inc.
#
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


from cloudaudit.control import base


class NIST_800_53_Control(base.BaseControl):
    """Base control for NIST 800-53 Regime."""

    regime_id = "NIST 800-53"
    regime = "gov/nist/crc/sp800-53"
    regime_str = "NIST 800-53 sp3"
    regime_version = "r3"
