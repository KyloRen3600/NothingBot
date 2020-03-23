import os
import json
import importlib
import NothingAPI

class Addon():
    def __init__(self, client, file):
        self.client = client
        self.json = file

        with open(file, 'r') as f:
            self.data = json.load(f)

        self.name = self.data["name"]
        self.description = self.data["description"]
        self.version = self.data["version"]

        self.commands = self.data["commands"]
        self.help_command = self.data["help_command"]
        self.help_description = self.data["help_description"]

        self.script = self.data["script"]
        self.enabled = self.data["enabled"]
        self.developer = self.data["developer"]
        self.icon = self.data["icon"]
        self.link = self.data["link"]


    def import_script(self):
        self.module = importlib.import_module(self.script)
        self.module.__main__(self.client, self)

def get_addons_list(client):
    addons_list = {}
    for script in os.listdir("addons/"):
        if script.endswith(".json"):
            addon = Addon(client, "addons/{0}".format(script))
            if addon.enabled:
                addons_list["{0}".format(addon.name.lower())] = addon
    return addons_list

def load_addons(client):
    addons = get_addons_list(client)
    for addon in addons:
        addon = addons[addon.lower()]
        NothingAPI.log("INFO", "Loading Addon {0} {1}...".format(addon.name, addon.version))
        if addon.enabled:
            addon.import_script()
    return addons
