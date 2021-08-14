import requests

import text_utils


class Recipe:
    def __init__(self, whip, app_id, app_key):
        self.whip = whip

        self.ID = app_id
        self.KEY = app_key

        self.whip.alert("ok")