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


from xml.dom.minidom import Document


class BaseControl(object):

    """
    A controller that produces information on the Glance API versions.
    """

    def __init__(self, evidence_gatherer=None, control_title="Not Set",
                 regime="Not Set",
                 regime_version="Not Set",
                 control_id="Not Set",
                 control_subtitle="Not Set",
                 time_updated="Never",
                 regime_str="Not Set",
                 entries=None,
                 docEntries=[],
                 root_url="http://localhost/.well-known/cloudaudit"):
        self._doc = Document()
        self._authors = []

        self.evidence_gatherer = evidence_gatherer
        self.control_title = control_title
        self.regime = regime
        self.regime_version = regime_version
        self.control_id = control_id
        self.control_subtitle = control_subtitle
        self.time_updated = time_updated
        self.regime_str = regime_str
        self.entries = entries
        self.docEntries = docEntries
        self.root_url = root_url

    def get_evidence(self, req):

        return ""

    def get_manifest(self, req):
        doc = self._doc

        self._feed = doc.createElement("feed")
        self._feed.setAttribute("xmlns", "http://www.w3.org/2005/Atom")

        self._title = doc.createElement("title")
        ptext = doc.createTextNode(self.control_title)
        self._title.appendChild(ptext)

        self._link = doc.createElement("link")
        link = self._link
        link.setAttribute("href",
                          "http://www.cloudhosting.com/.well-known/cloudaudit/"
                                  + self.regime + "/" +
                                  self.regime_version + "/"
                                  + self.control_id + "/")
        link.setAttribute("rel", "self")

        self._idTag = doc.createElement("id")
        idTag = self._idTag

        ptext = doc.createTextNode(
            "http://www.cloudhosting.com/.well-known/cloudaudit/"
            + self.regime + "/" + self.regime_version + "/" +
            self.control_id + "/")
        idTag.appendChild(ptext)

        self._subtitle = doc.createElement("subtitle")
        ptext = doc.createTextNode(self.control_subtitle)

        self._subtitle.appendChild(ptext)

        self._updated = doc.createElement("updated")
        ptext = doc.createTextNode(self.time_updated)
        self._updated.appendChild(ptext)

        self._generator = doc.createElement("generator")
        self._generator.setAttribute("uri",
                                     "www.pistoncloud.com/cloudauditapi")
        self._generator.setAttribute("version", "1.0")
        ptext = doc.createTextNode("Piston CloudAudit API Implementation 1.0")
        self._generator.appendChild(ptext)

        self.add_author("John Doe", "jdoe@pistoncloud.com")

        self._rights = doc.createElement("rights")

        self._category = doc.createElement("category")
        self._category.setAttribute("term", self.regime)
        self._category.setAttribute("label", self.regime_str)

        self._docEntries = []

        for entry in self.entries:
            new_entry = doc.createElement("entry")
            self._docEntries.append(new_entry)

            new_entry_title = doc.createElement("title")
            new_entry.appendChild(new_entry_title)

            new_entry_link = doc.createElement("link")
            new_entry.appendChild(new_entry_link)

            new_entry_id = doc.createElement("id")
            new_entry.appendChild(new_entry_id)

            new_entry_updated = doc.createElement("updated")
            new_entry.appendChild(new_entry_updated)

            new_entry_summary = doc.createElement("summary")
            new_entry.appendChild(new_entry_summary)

            ptext = doc.createTextNode(entry['title'])
            new_entry_title.appendChild(ptext)

            ptext = doc.createTextNode(entry['link'])
            new_entry_link.appendChild(ptext)
            new_entry.appendChild(new_entry_title)
            new_entry_link.setAttribute("type", entry['type'])
            new_entry_link.setAttribute("rel", "realated")

            ptext = doc.createTextNode(entry['id'])
            new_entry_id.appendChild(ptext)

            ptext = doc.createTextNode(entry['updated'])
            new_entry_updated.appendChild(ptext)

            ptext = doc.createTextNode(entry['summary'])
            new_entry_summary.appendChild(ptext)

            for author in entry['author']:
                new_author = doc.createElement("author")

                new_author_name = doc.createElement("name")
                new_author.appendChild(new_author_name)

                new_author_email = doc.createElement("email")
                new_author.appendChild(new_author_email)

                ptext = doc.createTextNode(author['name'])
                new_author_name.appendChild(ptext)

                ptext = doc.createTextNode(author['email'])
                new_author_email.appendChild(ptext)

            for contrib in entry['contributor']:
                new_contrib = doc.createElement("contributor")

                new_contrib_name = doc.createElement("name")
                new_contrib.appendChild(new_contrib_name)

                newContrib_email = doc.createElement("email")
                new_contrib.appendChild(newContrib_email)

                ptext = doc.createTextNode(contrib['name'])
                new_contrib_name.appendChild(ptext)

                ptext = doc.createTextNode(contrib['email'])
                newContrib_email.appendChild(ptext)

    def add_entries(self, req):
        self.entries = []

    def get_response(self, req):
        self._doc.appendChild(self._feed)
        self._feed.appendChild(self._title)
        self._feed.appendChild(self._link)
        self._feed.appendChild(self._idTag)
        self._feed.appendChild(self._subtitle)
        self._feed.appendChild(self._updated)
        self._feed.appendChild(self._generator)
        for author in self._authors:
            self._feed.appendChild(author)

        for entry in self._docEntries:
            self._feed.appendChild(entry)

        retval = self._doc.toprettyxml(indent="  ")

        return retval

    def add_author(self, name, email):
        if self._authors is None:
            self._authors = []

        new_author = self._doc.createElement("author")
        new_name = self._doc.createElement("name")
        new_email = self._doc.createElement("email")

        ptext = self._doc.createTextNode(name)
        new_name.appendChild(ptext)
        ptext = self._doc.createTextNode(email)
        new_email.appendChild(ptext)

        new_author.appendChild(new_name)
        new_author.appendChild(new_email)

        self._authors.append(new_author)
