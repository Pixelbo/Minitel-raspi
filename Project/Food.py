import json
import urllib.parse

import requests
import text_utils


# import qrcode


class Recipe:
    def __init__(self, whip, app_id, app_key):
        self.whip = whip

        self.ID = app_id
        self.KEY = app_key

        self.name_lunch = None
        self.extra_params = None

        # self.request("chicken soup", '{"diet": "low-fat"}')
        self.Menu()

    # Extras list presentation in json: {"diet": "low-fat"}
    def request(self, query, extra):
        Base_url = "https://api.edamam.com/api/recipes/v2?type=public" \
                   "&q={_query}" \
                   "&app_id={id}" \
                   "&app_key={key}" \
                   "{extra}" \
                   "&field=label&field=source&field=url&field=shareAs&field=yield&field=dietLabels&field=healthLabels&field=cautions&field=ingredientLines&field=ingredients&field=calories&field=totalTime&field=cuisineType&field=mealType&field=dishType&field=totalNutrients"

        query = urllib.parse.quote(query)

        if extra is not None:
            extra_dict = json.loads(extra)

            extra_str = ""
            for extra in extra_dict:
                extra_str += "&" + urllib.parse.quote(extra) + "=" + urllib.parse.quote(extra_dict[extra])
        else:
            extra_str = ""

        URL = Base_url.format(_query=query, id=self.ID, key=self.KEY, extra=extra_str)

        request = requests.get(URL)

        if request.status_code != 200:
            self.whip("Erreur WEB!, Erreur: {}".format(request.status_code))

        request_JSON = json.dumps(request.json())

        return request_JSON

    def Menu(self):
        choix_menuFood = ("Nom de la recette", "Parametres extras",
                          "----------------",
                          "Documentation pour les parametres extras",
                          "----------------",
                          "Recherche!",
                          "----------------",
                          "Quitter")

        choix_menuFood = text_utils.center_list(choix_menuFood)  # Center the menu

        selection = self.whip.menu("", choix_menuFood).decode("UTF-8")

        if selection == choix_menuFood[0]:
            self.name_lunch = self.Query_entry()
        if selection == choix_menuFood[1]:
            self.extra_params = self.Extra_params()
        if selection == choix_menuFood[3]: pass
        if selection == choix_menuFood[5]:
            if (self.name_lunch == None):
                self.whip.alert("Vous n'avez pas mis de repas!")
            else:
                self.Search()
        if selection == (choix_menuFood[2] or choix_menuFood[4] or choix_menuFood[6]): self.Menu()
        if selection == choix_menuFood[-1]: return

        self.Menu()

    def Query_entry(self):
        reponse = self.whip.prompt("Veuillez mettre le nom de la recette: ").decode("UTF-8")
        return reponse

    def Extra_params(self):
        reponse = self.whip.prompt("Veuillez mettre les paramètres extras; \n"
                                   "Vous devez les écrire comme ça:  KEY:VALUE ; séparé par une virgule").decode(
            "UTF-8")

        reponse = reponse.split(",")

        for i in reponse:
            reponse[reponse.index(i)] = i.split(":")

        return json.dumps(dict(reponse))

    def Search(self):
        print(self.request(self.name_lunch, self.extra_params))
