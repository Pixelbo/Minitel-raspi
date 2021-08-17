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

        self.nameLunch = None
        self.extraParams = None
        self.Recipe = None

        self.Menu()

    # Extras list presentation in json: {"diet": "low-fat"}
    def request(self, param, extra, type="Search"):

        param = urllib.parse.quote(param)

        if type == "Search":
            Base_url = "https://api.edamam.com/api/recipes/v2?type=public" \
                       "&q={_query}" \
                       "&app_id={id}" \
                       "&app_key={key}" \
                       "{extra}" \
                       "&field=label&field=source&field=url&field=shareAs&field=yield&field=dietLabels&field=healthLabels&field=cautions&field=ingredientLines&field=calories&field=totalTime&field=cuisineType&field=mealType&field=dishType&field=totalNutrients"

            if extra is not None:
                extra_dict = json.loads(extra)

                extra_str = ""
                for extra in extra_dict:
                    extra_str += "&" + urllib.parse.quote(extra) + "=" + urllib.parse.quote(extra_dict[extra])
            else:
                extra_str = ""

            URL = Base_url.format(_query=param, id=self.ID, key=self.KEY, extra=extra_str)

        elif type == "withID":
            Base_url = "https://api.edamam.com/api/recipes/v2/{recipeID}?type=public" \
                       "&app_id={id}" \
                       "&app_key={key}"

            URL = Base_url.format(recipeID=param, id=self.ID, key=self.KEY)

        else:
            return

        request = requests.get(URL)

        if request.status_code != 200:
            self.whip("Erreur WEB!, Erreur: {}".format(request.status_code))

        request_JSON = request.json()

        return request_JSON

    def Menu(self):

        choix_menuFood = ("Nom de la recette", "Parametres extras",
                          "----------------",
                          "Documentation pour les parametres extras",
                          "----------------",
                          "Favoris!",
                          "Recherche!",
                          "----------------",
                          "Quitter")

        choix_menuFood = text_utils.center_list(choix_menuFood)  # Center the menu

        selection = self.whip.menu("", choix_menuFood).decode("UTF-8")

        if selection == choix_menuFood[0]:
            self.nameLunch = self.Query_entry()
        if selection == choix_menuFood[1]:
            self.extraParams = self.Extra_params()
        if selection == choix_menuFood[3]:
            # TODO: do the file
            pass
        if selection == choix_menuFood[5]:
            # TODO: do the favs
            pass
        if selection == choix_menuFood[6]:
            if self.nameLunch is not None:
                self.Search(self.nameLunch, self.extraParams)  # TODO: get that self out of there!
            else:
                self.whip.alert("Vous n'avez pas mis de repas!")

        if selection == (choix_menuFood[2] or choix_menuFood[4] or choix_menuFood[7]): self.Menu()
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

    def Search(self, name_lunch, extra_params=None, overdrive=None):
        reponse = self.request(name_lunch, extra_params)

        fromToCount = [reponse["from"], reponse["to"], reponse["count"]]

        if fromToCount[2] == 0:
            self.whip.alert("Mauvaise recherche!")
            return

        recipeArray = []
        recipeLabels = ["Quitter"]

        for i in reponse["hits"]:
            recipeArray.append(i["recipe"])
            recipeLabels.append(i["recipe"]["label"])

        recipeLabels = text_utils.center_list(recipeLabels)

        if overdrive is None:
            selected_recipe = self.whip.menu("Here are the results; there are {} results, this is from {} to {}"
                                             .format(fromToCount[2], fromToCount[0], fromToCount[1]),
                                             recipeLabels, extras=()).decode("UTF-8")
        else:
            selected_recipe = recipeLabels[overdrive + 1]

        if selected_recipe == recipeLabels[0]:  # Next page
            return  # TODO: better function

        if selected_recipe == recipeLabels[1]:  # Quitter
            return  # TODO: better function

        self.Recipe = recipeArray[recipeLabels.index(selected_recipe) - 1]  # -1 for the quitter
        index = recipeLabels.index(selected_recipe) - 1

        recipeID = reponse["hits"][index]["_links"]["self"]["href"]
        recipeID = recipeID[38:recipeID.index("?")]

        choix_menuRecipe = (
            "Voir les ingrédients", "Voir les détails de la recette", "Voir les nutrimetns de la recette",
            "----------------",
            "Ajouter la recette au favoris",
            "----------------",
            "Generer un qr code !",
            "----------------",
            "Retour")

        choix_menuRecipe = text_utils.center_list(choix_menuRecipe)

        result = self.whip.menu(
            "Voici les options pour la recette: {} ".format(text_utils.decenter_text(selected_recipe)),
            choix_menuRecipe).decode("UTF-8")

        if result == choix_menuRecipe[0]: self.look_ingredients(name_lunch, extra_params, index)
        if result == choix_menuRecipe[1]: self.look_details(name_lunch, extra_params, index)
        if result == choix_menuRecipe[2]: self.look_nutriments(name_lunch, extra_params, index)
        if result == choix_menuRecipe[4]: self.add_fav(name_lunch, extra_params, index, recipeID)
        if result == choix_menuRecipe[6]: self.generate_qrcode(name_lunch, extra_params, index)
        if result == (choix_menuRecipe[3] or choix_menuRecipe[5] or choix_menuRecipe[7]): self.Search(name_lunch,
                                                                                                      extra_params)
        if result == choix_menuRecipe[-1]: self.Search(name_lunch, extra_params)

    def look_ingredients(self, return_name_lunch, return_extra_params, index):
        ingredients = []

        for i in self.Recipe["ingredientLines"]:
            ingredients.append(i)

        ingredients = text_utils.center_list(ingredients)

        self.whip.menu("Voici la liste des ingredients, faites enter pour faire retour", ingredients)

        self.Search(return_name_lunch, return_extra_params, index)

    def look_details(self, return_name_lunch, return_extra_params, index):
        label = self.Recipe["label"]
        source = self.Recipe["source"]

        cuisineType = self.Recipe["cuisineType"]
        mealType = self.Recipe["mealType"]
        dishType = self.Recipe["dishType"]
        people = self.Recipe["yield"]

        message = (
            "",
            "",
            text_utils.center_text("{}".format(label), 76, True),
            text_utils.center_text("Un repas pour {} personnes".format(int(people)), 76, True),
            "",
            "",
            text_utils.center_text("Type de cuisine: {}".format(" ".join(cuisineType)), 76, True),
            "",
            text_utils.center_text("Type de repas: {}".format(" ".join(mealType)), 76, True),
            "",
            text_utils.center_text("Type d'assiette: {}".format(" ".join(dishType)), 76, True),
            "",
            "",
            "",
            "",
            text_utils.center_text("Source: {}".format(source), 76, True),
            "",
            ""
        )

        self.whip.confirm("\n".join(message), extras=("Quit", "Quit"))

        self.Search(return_name_lunch, return_extra_params, index)

    def look_nutriments(self, return_name_lunch, return_extra_params, index):
        nutriments = []
        for i in self.Recipe["totalNutrients"]:
            nutriments.append("{} ou {} : {} {}".format(i,
                                                        self.Recipe["totalNutrients"][i]["label"],
                                                        round(int(self.Recipe["totalNutrients"][i]["quantity"])),
                                                        self.Recipe["totalNutrients"][i]["unit"]))

        self.whip.menu("Voici les nutriments, faites enter pour faire retour", nutriments)

        self.Search(return_name_lunch, return_extra_params, index)

    def add_fav(self, return_name_lunch, return_extra_params, index, ID):
        with open('favFood.json', 'r+') as file:
            json_file = json.load(file)
            data = json_file["favs"]

            for i in data:
                if i["ID"] == ID:
                    self.whip.alert("Vous avez deja ce favoris!")
                    self.Search(return_name_lunch, return_extra_params, index)

            data2 = {
                "label": self.Recipe["label"],
                "ID": ID
            }

            json_file["favs"].append(data2)

            file.seek(0)

            json.dump(json_file, file, indent=4)
            file.close()

        self.Search(return_name_lunch, return_extra_params, index)

    def generate_qrcode(self, return_name_lunch, return_extra_params, index):
        # TODO: do it!
        self.Search(return_name_lunch, return_extra_params, index)
