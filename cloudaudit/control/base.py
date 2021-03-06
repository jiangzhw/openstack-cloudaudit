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
Base class for CloudAudit control implementations
"""

from lxml import etree
from lxml.builder import E
import urlparse
from xml.dom.minidom import Document
import cloudaudit.api.wsgi
from cloudaudit.api.middleware import keystone
from webob import Response
import webob


class BaseControl(cloudaudit.api.wsgi.Middleware):

    """
    A controller that produces information on the Glance API versions.
    """
    scheme = "http"
    net_loc = "www.cloudhosting.com"
    base_loc = ".well-known/cloudaudit"
    generated_net_loc = "pistincloud.com"
    generated_base_loc = "CloudauditAPI"
    generated_vers = "1.0"
    api_name = "Piston CloudAudit API Implementation 1.0"

    rights = "Copyright (c) 2009, Piston Cloud Computing Inc."

    def __init__(self):
        self.text_response = None

        self._doc = Document()
        self._authors = []

        regime = self.__class__.regime
        self.control_title = self.__class__.control_title
        self.regime = self.__class__.regime
        self.regime_version = self.__class__.regime_version
        self.control_id = self.__class__.control_id
        self.control_subtitle = self.__class__.control_subtitle
        self.time_updated = self.__class__.time_updated
        self.regime_str = self.__class__.regime_id
        self.entries = []
        self.docEntries = []
        self.scheme = self.__class__.scheme

        self.control_path = str.join("/", (self.__class__.base_loc,
                                           self.__class__.regime,
                                           self.__class__.regime_version,
                                           self.__class__.control_id))

        self.gen_path = str.join("/", (self.__class__.generated_net_loc,
                                           self.__class__.generated_base_loc))

    def get_evidence(self, req):

        return ""

    @property
    def route(self):
        return "/"  + self.control_path
    
    @property
    def url(self):
        return urlparse.urlunsplit((self.scheme, self.__class__.net_loc,
                                    self.control_path, None, None))

    @property
    def id(self):
        return urlparse.urlunsplit((self.scheme, self.__class__.net_loc,
                                    self.control_path, None, None))

    @property
    def generated(self):
        return urlparse.urlunsplit((self.scheme, self.__class__.net_loc,
                                    self.gen_path, None, None))

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
        path = req.path
        if len(path) == len(self.route):
            return self.get_manifest(req)
        else:
            return None

    def get_manifest(self, req):

        self.add_author("jd", "jd@sec")
        self.add_author("jd2", "jdddd@asdf.com")

        temp_xml = \
        recursively_serialize_a_list(self._authors, etree.Element("authors"))

        txml = temp_xml

        for e in self.entries:
            new_xml = e.to_xml()
            txml.append(new_xml)
            txml = new_xml

        self.xml_doc = E.feed({"xmlns": "http://www.w3.org/2005/Atom"},
            E.title(self.control_title),
            E.link({"href": self.url},
                {"rel": "self"}),
            E.id(self.id),
            E.subtitle(self.control_subtitle),
            E.updated(self.time_updated),
            E.generator({"uri": self.generated},
                {"version": self.__class__.generated_vers},
                self.__class__.api_name),
            E.rights({"term": ""}),
            temp_xml,
            E.rights({"type": "text"}, self.__class__.rights),
            E.category({"term": self.__class__.regime_str},
                    {"label": self.__class__.regime_str}),
            temp_xml)

        self.text_response = etree.tostring(self.xml_doc, pretty_print=True)

        self.response = Response()

        self.response.write(self.text_response)
        self.response.headers['content-type'] = 'application/xml'
        
        return self.response

    def add_entries(self, req):
        self.entries = []

    def get_response(self, req):

        if self.text_response is not None:
            return self.text_response

        self.text_response = etree.tostring(self.xml_doc, pretty_print=True)

        return self.text_response

    def add_author(self, name, email):
        if self._authors is None:
            self._authors = []

        self._authors.append({"author": [{"name":  name},
                {"email": email}]})

    def get_xml_inventory_base(self, req, evidence_items, tag1):
        temp_xml = None

        for item in evidence_items.keys():
            if temp_xml is None:
                temp_xml = E.entry(str(evidence_items[item]), {"ip": item})
            else:
                add_xml = E.entry(str(evidence_items[item]), {"ip": item})
                temp_xml.append(add_xml)

        root_xml = etree.Element(tag1)

        if temp_xml is not None:
            self.manifest_xml = etree.SubElement(root_xml, temp_xml)

        self.manifest_response = etree.tostring(root_xml, pretty_print=True)

        self.response = Response()

        self.response.write(self.manifest_response)
        self.response.headers['content-type'] = 'application/xml'

        return self.response

def serialize_a_dict(d, parent):
    for k, v in d.items():
        if isinstance(v, dict):
            if k == "123ATTRIBUTE123":
                for k2, v2 in v:
                    parent.attrib[k2] = v2
            else:
                el = etree.SubElement(parent, k)
                serialize_a_dict(v, el)
        elif isinstance(v, list):
            el = etree.SubElement(parent, k)
            recursively_serialize_a_list(v, el)
        else:
            el = etree.SubElement(parent, k)
            el.text = str(v)
    return parent


def recursively_serialize_a_list(l, parent):
    for v in l:
        try:
            if v.__iter__:
                if isinstance(v, dict):
                    serialize_a_dict(v, parent)
                else:
                    recursively_serialize_a_list(v, parent)
        except AttributeError:
            el = etree.SubElement(parent, parent.tag)
            el.text = str(v)
    return parent
