import requests
import urllib.parse
import json
#import qrcode

import text_utils


class Recipe:
    def __init__(self, whip, app_id, app_key):
        self.whip = whip

        self.ID = app_id
        self.KEY = app_key

        self.request("chicken soup", '{"diet": "low-fat"}')

    # Extras list presentation in json: {"diet": "low-fat"}
    def request(self, query, extra):
        Base_url = "https://api.edamam.com/api/recipes/v2?type=public" \
                   "&q={_query}" \
                   "&app_id={id}" \
                   "&app_key={key}" \
                   "{extra}" \
                   "&field=label&field=source&field=url&field=shareAs&field=yield&field=dietLabels&field=healthLabels&field=cautions&field=ingredientLines&field=ingredients&field=calories&field=totalTime&field=cuisineType&field=mealType&field=dishType&field=totalNutrients"

        query = urllib.parse.quote(query)
        extra_dict = json.loads(extra)

        extra_str = ""
        for extra in extra_dict:
            extra_str += "&" + extra + "=" + extra_dict[extra]

        URL = Base_url.format(_query=query, id=self.ID, key=self.KEY, extra=extra_str)

        request = requests.get(URL)

        if request.status_code != 200:
            self.whip("Erreur WEB!, Erreur: {}".format(request.status_code))

        request_JSON = json.loads(request.json())

        return request_JSON

    