import logging

import routes

from openstack.common import wsgi
from cloudaudit.api.v1 import controls


class API(wsgi.Router):

    """WSGI router for Glance v1 API requests."""

    def __init__(self, options):
        self.options = options
        mapper = routes.Mapper()
        resource = controls.create_resource(options)
#        resource = images.create_resource(options)
#        mapper.resource("image", "images", controller=resource,
#                        collection={'detail': 'GET'})
        mapper.connect("/.well_known/cloudaudit/glossary/{controlid}",
                       controller=resource, action="index")
        super(API, self).__init__(mapper)


def app_factory(global_conf, **local_conf):
    """paste.deploy app factory for creating Glance API server apps"""
    conf = global_conf.copy()
    conf.update(local_conf)
    return API(conf)
