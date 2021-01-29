from flask import Flask, request, render_template

from .lang import to_simplified
from .search import BibleSearchEngine, BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize


def create_app():
    app = Flask(__name__,
                static_folder='../frontend',
                static_url_path='/static',
                template_folder='../frontend')

    from .conceptnet_strategy import ConceptNetStrategy
    strategy = ConceptNetStrategy.from_pickle()
    ezra_engine = BibleSearchEngine(strategy)

    @app.route('/')
    def index():
        data = {
            'keyword': request.args.get('q'),
            'query_string': request.query_string.decode('utf-8')
        }
        return render_template("index.html", data=data)

    @app.route('/api')
    def search():
        query = request.args['q']
        results = ezra_engine.search(query, zh_cn=False)
        return {
            'status': 'success',
            'data': [match.to_dict() for match in results]
        }

    return app
