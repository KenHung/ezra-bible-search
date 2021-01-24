from flask import Flask, request

from .conceptnet_strategy import ConceptNetStrategy
from .lang import to_simplified
from .search import BibleSearchEngine, BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize

print('Ezra initializing...')
strategy = ConceptNetStrategy.from_pickle()
ezra_engine = BibleSearchEngine(strategy)


def create_app():
    app = Flask(__name__)
    app.logger.info('Creating new app...')

    @app.route('/')
    def hello_world():
        app.logger.info("Hello Log")
        return 'Hello, World!'

    @app.route('/api')
    def search():
        query = request.args['q']
        results = ezra_engine.search(query, zh_cn=False)
        return {
            'status': 'success',
            'data': [match.to_dict() for match in results]
        }

    return app
