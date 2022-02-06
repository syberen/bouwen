from calendar import month
from flask import Flask

from services import CBSAggregateService

app = Flask(__name__)


@app.route("/aggregate")
def aggregate():
    aggregate_service = CBSAggregateService()
    amount = aggregate_service.get_aggregate()

    return {"amount": amount}
