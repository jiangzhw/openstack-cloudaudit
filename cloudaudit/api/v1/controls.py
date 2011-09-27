# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 OpenStack LLC.
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
/cloudaudit endpoint for CloudAudit v1 API
"""

import httplib
import json
import logging
import sys
import traceback

import webob
from webob.exc import (HTTPNotFound,
                       HTTPConflict,
                       HTTPBadRequest,
                       HTTPForbidden,
                       HTTPUnauthorized)

from cloudaudit import api
from openstack.common import exception
from openstack.common import notifier
from openstack.common import wsgi
#from cloudaudit import utils


logger = logging.getLogger('cloudaudit.api.v1.controls')

SUPPORTED_FILTERS = [ ]

SUPPORTED_PARAMS = ()


class Controller(api.BaseController):
    """
    WSGI controller for cloudaudit resource in CloudAudit v1 API

REPLACE ALL THIS WITH CLOUDAUDIT COMMENTS
    The images resource API is a RESTful web service for image data. The API
    is as follows::

        GET /images -- Returns a set of brief metadata about images
        GET /images/detail -- Returns a set of detailed metadata about
                              images
        HEAD /images/<ID> -- Return metadata about an image with id <ID>
        GET /images/<ID> -- Return image data for image with id <ID>
        POST /images -- Store image data and return metadata about the
                        newly-stored image
        PUT /images/<ID> -- Update image metadata and/or upload image
                            data for a previously-reserved image
        DELETE /images/<ID> -- Delete the image with id <ID>
    """

    def __init__(self, options):
        self.options = options
        self.notifier = notifier.Notifier(options)

    def index(self, req):
        """
        Returns the following information for all public, available images:

            * id -- The opaque image identifier
            * name -- The name of the image
            * disk_format -- The disk image format
            * container_format -- The "container" format of the image
            * checksum -- MD5 checksum of the image data
            * size -- Size of image data in bytes

        :param req: The WSGI/Webob Request object
        :retval The response body is a mapping of the following form::

            {'images': [
                {'id': <ID>,
                 'name': <NAME>,
                 'disk_format': <DISK_FORMAT>,
                 'container_format': <DISK_FORMAT>,
                 'checksum': <CHECKSUM>
                 'size': <SIZE>}, ...
            ]}
        """
        params = self._get_query_params(req)
#        try:
        time = 1
# TODO -- create a listing here
#        except exception.Invalid, e:
        #    raise HTTPBadRequest(explanation="%s" % e)

        return dict(time=time)

    def detail(self, req):
        """
        Returns detailed information for all public, available images

        :param req: The WSGI/Webob Request object
        :retval The response body is a mapping of the following form::

            {'images': [
                {'id': <ID>,
                 'name': <NAME>,
                 'size': <SIZE>,
                 'disk_format': <DISK_FORMAT>,
                 'container_format': <CONTAINER_FORMAT>,
                 'checksum': <CHECKSUM>,
                 'store': <STORE>,
                 'status': <STATUS>,
                 'created_at': <TIMESTAMP>,
                 'updated_at': <TIMESTAMP>,
                 'deleted_at': <TIMESTAMP>|<NONE>,
                 'properties': {'distro': 'Ubuntu 10.04 LTS', ...}}, ...
            ]}
        """
        params = self._get_query_params(req)
#        try:
#            images = registry.get_images_detail(self.options, req.context,
#                                                **params)
#        except exception.Invalid, e:
        raise HTTPBadRequest(explanation="%s" % e)
#        return dict(images=images)

    def _get_query_params(self, req):
        """
        Extracts necessary query params from request.

        :param req: the WSGI Request object
        :retval dict of parameters that can be used by registry client
        """
        params = {'filters': self._get_filters(req)}
        for PARAM in SUPPORTED_PARAMS:
            if PARAM in req.str_params:
                params[PARAM] = req.str_params.get(PARAM)
        return params

    def _get_filters(self, req):
        """
        Return a dictionary of query param filters from the request

        :param req: the Request object coming from the wsgi layer
        :retval a dict of key/value filters
        """
        filters = {}
        for param in req.str_params:
            if param in SUPPORTED_FILTERS or param.startswith('property-'):
                filters[param] = req.str_params.get(param)

        return filters

#    def meta(self, req, id):
        """
        Returns metadata about an image in the HTTP headers of the
        response object

        :param req: The WSGI/Webob Request object
        :param id: The opaque image identifier
        :retval similar to 'show' method but without image_data

        :raises HTTPNotFound if image metadata is not available to user
        """
#        return {
#            'image_meta': self.get_image_meta_or_404(req, id),
#        }

#    def show(self, req, id):
        """
        Returns an iterator that can be used to retrieve an image's
        data along with the image metadata.

        :param req: The WSGI/Webob Request object
        :param id: The opaque image identifier

        :raises HTTPNotFound if image is not available to user
        """
#        image = self.get_active_image_meta_or_404(req, id)

#        def get_from_store(image):
#            """Called if caching disabled"""
#            try:
#                image = get_from_backend(image['location'])
#            except exception.NotFound, e:
#                raise HTTPNotFound(explanation="%s" % e)
#            return image

#        def get_from_cache(image, cache):
#            """Called if cache hit"""
#            with cache.open(image, "rb") as cache_file:
#                chunks = utils.chunkiter(cache_file)
#                for chunk in chunks:
#                    yield chunk

class ImageDeserializer(wsgi.JSONRequestDeserializer):
    """Handles deserialization of specific controller method requests."""

    def _deserialize(self, request):
        result = {}
        result['control_name'] = 'baseControl'
        result['control_data'] = None
        return result

    def create(self, request):
        return self._deserialize(request)

    def update(self, request):
        return self._deserialize(request)

class ImageSerializer(wsgi.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def _inject_location_header(self, response, image_meta):
        location = 'default'
        response.headers['Location'] = location

    def _inject_checksum_header(self, response, image_meta):
        response.headers['ETag'] = image_meta['checksum']

    def _inject_image_meta_headers(self, response, image_meta):
        """
        Given a response and mapping of image metadata, injects
        the Response with a set of HTTP headers for the image
        metadata. Each main image metadata field is injected
        as a HTTP header with key 'x-image-meta-<FIELD>' except
        for the properties field, which is further broken out
        into a set of 'x-image-meta-property-<KEY>' headers

        :param response: The Webob Response object
        :param image_meta: Mapping of image metadata
        """
        headers = { }

        for k, v in headers.items():
            response.headers[k] = v


def create_resource(options):
    """Controls resource factory method"""
    deserializer = ImageDeserializer()
    serializer = ImageSerializer()
    return wsgi.Resource(Controller(options), deserializer, serializer)

