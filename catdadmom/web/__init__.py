""":mod:`catdadmom.web` --- CatDadMom web
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Flask

from . import main


def create_app(config):
    """The application factory.

    :param config: The instance relative configuration file to use.
    :returns: A CatDadMom Flask app.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config)
    app.register_blueprint(main.bp)
    return app
