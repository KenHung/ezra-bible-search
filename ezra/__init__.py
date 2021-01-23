from flask import Flask, request

from .conceptnet_strategy import ConceptNetStrategy
from .lang import to_simplified
from .search import BibleSearchEngine, BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        app.logger.info("Hello Log")
        return 'Hello, World!'

    return app
