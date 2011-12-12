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

from cloudaudit.control import nist
import cloudaudit.api.ControlRegistry


class GlossaryController(cloudaudit.api.wsgi.Middleware):

    """
        This class interrogates the registry to list out what regimes/controls
        are available for this cloudaudit implementation

    """

    # We override this primarily to add keystone authorization enforcement
    # subclasses should not override this method or if they do they
    # should always check keystone auth
    @webob.dec.wsgify
    def __call__(self, req):
        token = keystone.token_create(
                req, 'admin', req.str_GET['User'], req.str_GET['Password'])

        response = self.process_request(req)
        if response:
            return response
        response = req.get_response(self.application)
        return self.process_response(response)

    def process_request(self, req):
        control_registry = cloudaudit.api.ControlRegistry.CONTROL_REGISTRY
        controls = control_registry.get_all_controls()

        path = req.path

        for control in controls:
            # if control.route begins with path
            # then print out the control title
#            if control.route
            pass

        if len(path) == len(self.route):
            return self.get_manifest(req)
        else:
            return None
