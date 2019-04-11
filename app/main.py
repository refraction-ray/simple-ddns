from flask import Flask

from .conf import conf
from .api import api


def create_app():
    app = Flask(__name__)
    app.config.update(conf)

    app.logger.warning("app.debug: %s" % app.debug)
    app.register_blueprint(api)

    return app
