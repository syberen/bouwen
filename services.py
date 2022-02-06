import requests

from datetime import datetime


class CBSAggregateService:
    current_date = datetime.now()

    month_start = 1
    month_end = current_date.month

    year_start = 2021
    year_end = current_date.year

    base_url = "https://opendata.cbs.nl/ODataApi/odata/81955NED/UntypedDataSet"

    def get_periods(self):
        periods = []

        for year in range(self.year_start, self.year_end + 1):
            start_month = self.month_start if year == self.year_start else 1
            end_month = self.month_end if year == self.year_end else 13

            for month in range(start_month, end_month):
                year_str = str(year)
                month_str = f"{month:02d}"

                period_str = f"(Perioden eq '{year_str}MM{month_str}')"

                periods.append(period_str)

        return " or ".join(periods)

    def fetch_data(self):
        params = {
            "$filter": f"(Gebruiksfunctie eq 'A045364') and ({self.get_periods()}) and (substringof('NL',RegioS))",
            "$select": "Nieuwbouw_2, Perioden",
        }

        res = requests.get(self.base_url, params=params)
        res.raise_for_status()

        return res.json()

    @staticmethod
    def parse_period(period):
        month = int(period[6:8])
        year = int(period[:4])

        return datetime(year, month, 1)

    def get_aggregate_data(self):
        data = self.fetch_data()["value"]

        last_period = data[-1]["Perioden"]
        build_per_month = [int(record["Nieuwbouw_2"]) for record in data]

        return {
            "updated_at": self.parse_period(last_period),
            "amount_built": sum(build_per_month),
        }
