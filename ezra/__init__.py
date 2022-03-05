import json

from flask import Flask, redirect, render_template, request

from .conceptnet_strategy import ConceptNetStrategy
from .lang import to_simplified  # noqa: F401
from .resources import abbr
from .search import BibleSearchEngine, BibleSearchStrategy, Match  # noqa: F401
from .word_tokenizer import word_tokenize  # noqa: F401

strategy = ConceptNetStrategy.from_pickle()
ezra_engine = BibleSearchEngine(strategy)

search = ezra_engine.search
related_keywords = ezra_engine.related_keywords


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", version=get_version())

    @app.route("/search")
    def search_page():
        keyword = request.args.get("q", "")
        if not keyword:
            return redirect("/")
        else:
            return render_template(
                "search.html", version=get_version(), keyword=keyword
            )

    @app.route("/api")
    def api():
        return redirect("/static/api/index.html")

    @app.route("/api/search")
    def search():
        query = request.args.get("q")
        book = request.args.get("book", "").lower()
        top_k = request.args.get("top", 10, type=int)
        invalid_args_msg = validate_search_args(query, book, top_k)
        if invalid_args_msg:
            return make_fail_response(invalid_args_msg)

        results = ezra_engine.search(query, zh_cn=False, in_book=book, top_k=top_k)
        return {"status": "success", "data": [match.to_dict() for match in results]}

    @app.route("/api/related-keywords")
    def related_keywords():
        keyword = request.args.get("q")
        return {"status": "success", "data": ezra_engine.related_keywords(keyword)}

    def get_version():
        try:
            with open("source-context.json") as f:
                version = json.load(f)["git"]["revisionId"][:7]
        except FileNotFoundError:
            version = ""
        return version

    def validate_search_args(q, book, top):
        invalid_args_msg = {}
        if not q:
            invalid_args_msg["q"] = "Missing argument"
        if book and book not in abbr.all and book not in abbr.ranges:
            all_options = list(abbr.ranges) + abbr.all
            invalid_args_msg["book"] = f"Must be one of the following: {all_options}"
        if not 1 <= top <= 100:
            invalid_args_msg["top"] = "Must be within 1 and 100"
        return invalid_args_msg

    def make_fail_response(data):
        return {"status": "fail", "data": data}, 400

    return app
