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
import cloudaudit.control.base


class BaseEntry(object):

    """
    A helper class for tracking evidence entries.
    """

    def __init__(self):

        self.link = ""
        self.link_type = ""
        self.link_rel = ""

        self.id = ""

        self.title = ""

        self.updated = ""

        self.summary = ""

        self.content = ""
        self.content_type = "text"
        self.content_lang = "en"

        self._authors = []

    def add_author(self, name, email):
        if self._authors is None:
            self._authors = []

        self._authors.\
        append({"author": [{"name":  name}, {"email": email}]})

    def to_xml(self):

        author_xml = cloudaudit.control.base.\
        recursively_serialize_a_list(self._authors, etree.Element("authors"))

        ret_xml = E.entry(E.title(self.title),
            E.link({"href": self.link}, {"type": self.link_type},
                    {"rel": self.link_rel}),
            E.id(self.id),
            E.updated(self.updated),
            E.content({"type": self.content_type},
                    {"lang": self.content_lang}, self.content),
            author_xml)

        return ret_xml
