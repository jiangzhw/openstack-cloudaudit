# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Fourth Paradigm Development, Inc.
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

import openstackx
from openstackx.api import base
import openstackx.auth
import openstack


class User(object):
    def __init__(self, token, user, tenant, admin, service_catalog):
        self.token = token
        self.username = user
        self.tenant = tenant
        self.admin = admin
        self.service_catalog = service_catalog

    def is_authenticated(self):
        # TODO: deal with token expiration
        return self.token

    def is_admin(self):
        return self.admin


def get_user_from_request(request):
    if 'user' not in request.session:
        return User(None, None, None, None, None)
    return User(request.session['token'],
                request.session['user'],
                request.session['tenant'],
                request.session['admin'],
                request.session['serviceCatalog'])


class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user_from_request(request)
        return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()

    def process_exception(self, request, exception):
        if type(exception) in [openstack.compute.exceptions.Forbidden,
                               openstackx.api.exceptions.Forbidden]:
            # flush other error messages, which are collateral damage
            # when our token expires
            for message in messages.get_messages(request):
                pass
            messages.error(request, 'Your token has expired.\
                                     Please log in again')
            return shortcuts.redirect('/auth/logout')


def token_create(request, tenant, username, password):
    return Token(auth_api().tokens.create(tenant, username, password))


def auth_api():
#    LOG.debug('auth_api connection created using url "%s"' %
#                   settings.OPENSTACK_KEYSTONE_URL)
    return openstackx.auth.Auth(
            management_url='http://localhost:5000/v2.0/')


class APIResourceWrapper(object):
    """ Simple wrapper for api objects

        Define _attrs on the child class and pass in the
        api object as the only argument to the constructor
    """
    _attrs = []

    def __init__(self, apiresource):
        self._apiresource = apiresource

    def __getattr__(self, attr):
        if attr in self._attrs:
            # __getattr__ won't find properties
            return self._apiresource.__getattribute__(attr)
        else:
            LOG.debug('Attempted to access unknown attribute "%s" on'
                      ' APIResource object of type "%s" wrapping resource of'
                      ' type "%s"' % (attr, self.__class__,
                                      self._apiresource.__class__))
            raise AttributeError(attr)


class Token(APIResourceWrapper):
    """Simple wrapper around openstackx.auth.tokens.Token"""
    _attrs = ['id', 'serviceCatalog', 'tenant_id', 'username']
