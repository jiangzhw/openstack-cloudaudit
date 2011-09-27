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
import json

import webob.dec

from openstack.common import wsgi

from xml.dom.minidom import Document


class InitController(object):

    """
    A controller that produces information on the Glance API versions.
    """

    feed = None

    def __init__(self):
        
        self.doc = Document()
        self.authors = [ ]

        self.evidenceGatherer = None
        self.control_title = "Invalid Control"
        self.regime = "Invalid"
        self.regime_version = "Invalid"
        self.control_id = "Invalid"
        self.control_subtitle = "Invalid"
        self.time_updated = None
        self.regime_str = "None"
        self.entries = None
        self.docEntries = [ ]
        self.rootUrl = "http://www.cloudhosting.com/.well-known/cloudaudit/"


    def getEvidence(self, req):

        return ""

    def getManifest(self, req):
        doc = self.doc
        
        self.feed = doc.createElement("feed")
        self.feed.setAttribute("xmlns", "http://www.w3.org/2005/Atom")
        feed = self.feed
	

        self.title = doc.createElement("title")
        ptext = doc.createTextNode(self.control_title)
        self.title.appendChild(ptext)
        title = self.title

        self.link = doc.createElement("link")
        link = self.link
        link.setAttribute("href", "http://www.cloudhosting.com/.well-known/cloudaudit/" + self.regime + "/" + self.regime_version + "/" + self.control_id  + "/")
        link.setAttribute("rel", "self");

        self.idTag = doc.createElement("id");
        idTag = self.idTag

        ptext = doc.createTextNode("http://www.cloudhosting.com/.well-known/cloudaudit/" + self.regime + "/" + self.regime_version + "/" + self.control_id  + "/")
        idTag.appendChild(ptext)

        self.subtitle = doc.createElement("subtitle")
        ptext = doc.createTextNode(self.control_subtitle)

        self.subtitle.appendChild(ptext)

        self.updated = doc.createElement("updated")
        ptext = doc.createTextNode(self.time_updated)
        self.updated.appendChild(ptext)

        self.generator = doc.createElement("generator")
        self.generator.setAttribute("uri", "www.pistoncloud.com/cloudauditapi")
        self.generator.setAttribute("version", "1.0")
        ptext = doc.createTextNode("Piston CloudAudit API Implementation 1.0")
        self.generator.appendChild(ptext)

        self.addAuthor("John Doe", "jdoe@pistoncloud.com")

        self.rights = doc.createElement("rights")


        self.category = doc.createElement("category")
        self.category.setAttribute("term", self.regime )
        self.category.setAttribute("label", self.regime_str)

        self.docEntries = [ ]

        for entry in self.entries:
            newEntry = doc.createElement("entry")
            self.docEntries.append(newEntry)

            newEntry_title = doc.createElement("title")
            newEntry.appendChild(newEntry_title)

            newEntry_link = doc.createElement("link")
            newEntry.appendChild(newEntry_link)

            newEntry_id = doc.createElement("id")
            newEntry.appendChild(newEntry_id)

            newEntry_updated = doc.createElement("updated")
            newEntry.appendChild(newEntry_updated)

            newEntry_summary = doc.createElement("summary")
            newEntry.appendChild(newEntry_summary)

            ptext = doc.createTextNode(entry['title'])
            newEntry_title.appendChild(ptext)

            ptext = doc.createTextNode(entry['link'])
            newEntry_link.appendChild(ptext)
            newEntry.appendChild(newEntry_title)
            newEntry_link.setAttribute("type", entry['type'])
            newEntry_link.setAttribute("rel", "realated")

            ptext = doc.createTextNode(entry['id'])
            newEntry_id.appendChild(ptext)

            ptext = doc.createTextNode(entry['updated'])
            newEntry_updated.appendChild(ptext)

            ptext = doc.createTextNode(entry['summary'])
            newEntry_summary.appendChild(ptext)

            for author in entry['author']:
                newAuthor = doc.createElement("author")

                newAuthor_name = doc.createElement("name")
                newAuthor.appendChild(newAuthor_name)

                newAuthor_email = doc.createElement("email")
                newAuthor.appendChild(newAuthor_email)

                ptext = doc.createTextNode(author['name'])
                newAuthor_name.appendChild(ptext)

                ptext = doc.createTextNode(author['email'])
                newAuthor_email.appendChild(ptext)


            for contrib in entry['contributor']:
                newContrib = doc.createElement("contributor")

                newContrib_name = doc.createElement("name")
                newContrib.appendChild(newContrib_name)

                newContrib_email = doc.createElement("email")
                newContrib.appendChild(newContrib_email)

                ptext = doc.createTextNode(author['name'])
                newContrib_name.appendChild(ptext)

                ptext = doc.createTextNode(author['email'])
                newContrib_email.appendChild(ptext)


    def addEntries(self, req):
        self.entries = [ ]
        

    def getResponse(self, req):
        self.doc.appendChild(self.feed)
        self.feed.appendChild(self.title)
        self.feed.appendChild(self.link)
        self.feed.appendChild(self.idTag)
        self.feed.appendChild(self.subtitle)
        self.feed.appendChild(self.updated)
        self.feed.appendChild(self.generator)
        for author in self.authors:
            self.feed.appendChild(author)

        for entry in self.docEntries:
            self.feed.appendChild(entry)


        retval = self.doc.toprettyxml(indent="  ")

        
        return retval

    def addAuthor(self, name, email):
        if self.authors == None:
            self.authors = [ ]

        newAuthor = self.doc.createElement("author")
        newName = self.doc.createElement("name")
        newEmail = self.doc.createElement("email")

        ptext = self.doc.createTextNode(name)
        newName.appendChild(ptext)
        ptext = self.doc.createTextNode(email)
        newEmail.appendChild(ptext)

        newAuthor.appendChild(newName)
        newAuthor.appendChild(newEmail)

        self.authors.append(newAuthor)
        

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

        body = req
#        body = json.dumps(dict(req=req))
#        body = json.dumps(dict(versions=version_objs))

        response = webob.Response(request=req,
                                  status=httplib.MULTIPLE_CHOICES,
                                  content_type='application/json')
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
