# noinspection PyUnresolvedReferences
import asyncio
import logging
import os

from quart import Quart
from quart import render_template

from sleuthconf.trivia import Trivia

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def create_app(trivial: Trivia):

    app = Quart(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "not-so-secret")

    app.config["QUART_AUTH_COOKIE_SECURE"] = False
    app.config["env"] = "development"
    app.config["QUART_DEBUG"] = True
    app.config["DEBUG"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "not-so-secret")

    # logging.basicConfig()
    log = logging.getLogger(__name__)


    @app.route("/health", methods=["GET"])
    async def health():
        return "UP", 200


    @app.route("/slides/<string:slug>", methods=["GET"])
    async def get_slides(slug):
        log.error("get_slides called: {slug}")
        return await render_template(
            f"slides/{slug}.html",
            autoplay=True,
            questions=trivial.questions,
        )
    return app
