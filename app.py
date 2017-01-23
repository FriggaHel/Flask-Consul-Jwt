#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Manage root libs
import random, os, signal, sys, yaml
import logging, logging.config

# Registration to Consul
from consul import Consul

# Flask Stuff
from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT

# Tornado WebServer
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets

# Conf Loader
from urllib.request import urlopen
from urllib.error import HTTPError

# Load db connector
from Models import db

# Loading blueprints
from Views import health

# Loading Authentication tools
from Utils.auth import authenticate
from Utils.auth import identity
from Utils import errors

# Setup logging
logging.config.fileConfig('logging.conf')

# Override
APP_IP_ADDR = os.getenv('EXPOSED_ADDRESS', '127.0.0.1')
APP_CONSUL_ADDR = os.getenv('CONSUL_ADDRESS', '127.0.0.1')
APP_NAME = os.getenv('APP_NAME', 'app')

# Boostrap flask app
app = Flask(APP_NAME)
app.uniq_id = "".join(random.choice("abcdef0123456789") for x in range(16))
app.service_id = '%s-%s' % (app.name, app.uniq_id)

# Default config
app.config.update(
    DEBUG=True,
    UPLOAD_FOLDER='/tmp/',
    SECRET_KEY='changeme',
    JSONIFY_PRETTYPRINT_REGULAR=False,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Init DB Stuff
db.init_app(app)

# Init CORS
cors = CORS()
cors.init_app(app)

# Init JWT Secure layer
jwt = JWT()
jwt.authentication_callback = authenticate
jwt.identity_callback = identity
jwt.init_app(app)

# Errors Init
errors.init_app(app)

# Registering pages
app.register_blueprint(health)

#############################################

def __register_to_consul():
    global app

    tags = app.config['consul']['tags'] if 'consul' in app.config and 'tags' in app.config['consul'] else []
    csl = Consul(token="", host=APP_CONSUL_ADDR)
    agent = Consul.Agent.Service(csl)
    agent.register(name=app.name,
                   service_id=app.service_id,
                   port=app.app_port,
                   tags=tags,
                   check={
                       "id": "health-%s" % app.name,
                       "name": "Health %s" % app.name,
                       "http": "http://%s:%s/health/" % (APP_IP_ADDR, app.app_port),
                       "interval": "15s",
                       "timeout": "1s"
                   })

def __unregister_from_consul():
    global app

    csl = Consul(token="", host=APP_CONSUL_ADDR)
    agent = Consul.Agent.Service(csl)
    agent.deregister(service_id=app.service_id)

# Prevent zombies on Consul whn signaled
def __signaled_unregister_from_consul(signum, frame):
    __unregister_from_consul()
    sys.exit(0)

if __name__ == '__main__':
    # Create application
    tr = Application([
        (r".*", FallbackHandler, dict(fallback=WSGIContainer(app)))
    ])

    # Load Config
    csl = Consul(token="", host=APP_CONSUL_ADDR)
    _, cfgs = csl.catalog.service('config')
    try:
        with urlopen("http://%s:%s/resources/support/config.yml" % (cfgs[0]['Address'], cfgs[0]['ServicePort'])) as f:
            conf = yaml.load(f)
            app.config.update(conf)
    except HTTPError as e:
        logging.getLogger(__name__).error("Unable to find config file")
        sys.exit(1)
    finally:
        csl = None

    # Bind to Random socket
    sockets = bind_sockets(0, '')
    server = HTTPServer(tr)
    server.add_sockets(sockets)

    # Save port
    for s in sockets:
        app.app_port = s.getsockname()[:2][1]

    # Register to consul & run !
    try:
        __register_to_consul()
        signal.signal(signal.SIGTERM, __signaled_unregister_from_consul)
        signal.signal(signal.SIGINT, __signaled_unregister_from_consul)
        IOLoop.instance().start()
    except KeyboardInterrupt:
        __unregister_from_consul(None, None)
        csl = Consul(token="")
        agent = Consul.Agent.Service(csl)
        agent.deregister(service_id=app.service_id)
        IOLoop.instance().stop()
