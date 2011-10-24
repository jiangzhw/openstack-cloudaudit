# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
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

"""
Controller that returns information on the Glance API versions
"""

import httplib
import webob
import cloudaudit.api.ControlRegistry

from cloudaudit import local_settings

from  cloudaudit.api.middleware import keystone


class Controller(object):

    """
    A controller that produces information on the Glance API versions.
    """

    def __init__(self, options):
        self.options = options

    @webob.dec.wsgify
    def __call__(self, req):
        """Respond to a request for all OpenStack API versions."""
        version_objs = [
#            {
#                "id": "v1.1",
#                "status": "CURRENT",
#                "links": [
#                    {
#                        "rel": "self",
#                        "href": self.get_href()}]},
            {
                "id": "v1.0",
                "status": "SUPPORTED",
                "links": [
                    {
                        "rel": "self",
                        "href": self.get_href()}]}]
        token = keystone.token_create(
            req, 'admin', req.str_GET['User'], req.str_GET['Password'])

        url_tail = str.split(req.url, "/.wellknown/cloudaudit", 1)

        if len(url_tail) != 2:
            raise Exception("Malformed URL: " + req.url)

        url_tail = url_tail[1]

        url_tail = str.split(url_tail, "?", 1)

        if len(url_tail) != 2:
            raise Exception("Malformed URL: " + req.url)

        url_tail = url_tail[0]

        reg = cloudaudit.api.ControlRegistry.ControlRegistry()
        ic = reg.get_control_from_url(url_tail)

        ic.get_evidence(req)

        ic.get_manifest()

        body = ic.get_response(req)
#        body = json.dumps(dict(req=req))
#        body = json.dumps(dict(versions=version_objs))

        response = webob.Response(request=req,
                                  status=httplib.MULTIPLE_CHOICES,
                                  content_type='application/xml')
        response.body = body

        return response

    def get_href(self):
        return "http://%s:%s/v1/" % (self.options['bind_host'],
                                      self.options['bind_port'])


def app_factory(global_conf, **local_conf):
    """paste.deploy app factory for creating Glance API versions apps"""
    conf = global_conf.copy()
    conf.update(local_conf)
    return Controller(conf)
