import requests
import urllib.parse

import text_utils


class Recipe:
    def __init__(self, whip, app_id, app_key):
        self.whip = whip

        self.ID = app_id
        self.KEY = app_key

        self.request("chicken", "t")

    # Extras list presentation : {"diet": "low-fat"}
    def request(self, query, extra):
        Base_url = "https://api.edamam.com/api/recipes/v2?type=public" \
                   "&q={_query}" \
                   "&app_id={id}" \
                   "&app_key={key}" \
                   "{extra}" \
                   "&field=label&field=source&field=url&field=shareAs&field=yield&field=dietLabels&field=healthLabels&field=cautions&field=ingredientLines&field=ingredients&field=calories&field=totalTime&field=cuisineType&field=mealType&field=dishType&field=totalNutrients"

        query = urllib.parse.quote(query)
