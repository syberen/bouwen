from flask import Flask

from flask_caching import Cache

from services import CBSAggregateService

four_hours = 60 * 60 * 4
config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": four_hours,
}
app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)


@app.route("/aggregate")
@cache.cached()
def aggregate():
    aggregate_service = CBSAggregateService()
    data = aggregate_service.get_aggregate_data()

    return data
