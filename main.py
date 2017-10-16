# -*- coding: utf-8 -*-

from eve import Eve
from eve_swagger import swagger, add_documentation
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


DEFAULT_PORT = 8001
HOST = '0.0.0.0'


if __name__ == '__main__':
    app = Eve()
    app.register_blueprint(swagger)
    app.config['SWAGGER_INFO'] = {
        'title': 'My Supercool API',
        'version': '1.0',
        'description': 'an API description',
        'termsOfService': 'my terms of service',
        'contact': {
            'name': 'nicola',
            'url': 'http://nicolaiarocci.com'
        },
        'license': {
            'name': 'BSD',
            'url': 'https://github.com/pyeve/eve-swagger/blob/master/LICENSE',
        },
        'schemes': ['http', 'https'],
    }

    # optional. Will use flask.request.host if missing.
    app.config['SWAGGER_HOST'] = HOST

    # optional. Add/Update elements in the documentation at run-time without deleting subtrees.
    add_documentation({'paths': {'/status': {'get': {'parameters': [
        {
            'in': 'query',
            'name': 'foobar',
            'required': False,
            'description': 'special query parameter',
            'type': 'string'
        }]
    }}}})





    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(DEFAULT_PORT, address=HOST)
    print "running at server: {}:{}".format(HOST, DEFAULT_PORT)
    IOLoop.instance().start()

