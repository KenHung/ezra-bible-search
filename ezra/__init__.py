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
        query = request.args.get('q')
        top_k = request.args.get('top', 10, type=int)
        invalid_args_msg = validate_search_args(query, top_k)
        if invalid_args_msg:
            return make_fail_response(invalid_args_msg)

        results = ezra_engine.search(query, zh_cn=False, top_k=top_k)
        return {
            'status': 'success',
            'data': [match.to_dict() for match in results]
        }

    def validate_search_args(q, top):
        invalid_args_msg = {}
        if not q:
            invalid_args_msg['q'] = 'Missing argument'
        if not 1 <= top <= 100:
            invalid_args_msg['top'] = 'Must be within 1 and 100'
        return invalid_args_msg

    def make_fail_response(data):
        return {
            'status': 'fail',
            'data': data
        }, 400

    return app
