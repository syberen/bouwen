from flask import Flask

from services import CBSAggregateService

app = Flask(__name__)


@app.route("/aggregate")
def aggregate():
    aggregate_service = CBSAggregateService()
    data = aggregate_service.get_aggregate_data()

    return data
