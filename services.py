import requests

from datetime import datetime


class CBSAggregateService:
    current_date = datetime.now()

    month_start = 1
    month_end = current_date.month

    year_start = 2022
    year_end = current_date.year

    base_url = "https://opendata.cbs.nl/ODataApi/odata/81955NED/UntypedDataSet"

    def get_utility_type(self):
        return "Gebruiksfunctie eq 'A045364'"

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

    def get_regions(self):
        return "substringof('NL',RegioS)"

    def fetch_data(self):
        params = {
            "$filter": f"({self.get_utility_type()}) and ({self.get_periods()}) and ({self.get_regions()})",
            "$select": "SaldoVoorraad_7",
        }

        res = requests.get(self.base_url, params=params)
        res.raise_for_status()

        return res.json()

    def get_aggregate(self):
        data = self.fetch_data()

        monthly_amounts = [int(record["SaldoVoorraad_7"]) for record in data["value"]]

        return sum(monthly_amounts)
