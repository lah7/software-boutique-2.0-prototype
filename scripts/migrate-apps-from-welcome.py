#!/usr/bin/python3
#
# For testing (and migrating) apps to the new Software Boutique from Welcome.
#

import os
import inspect
import sys
import shutil
import json
import glob
from collections import OrderedDict

repo_root = os.path.abspath(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/../") + "/"
welcome_path = os.path.join(repo_root, "../", "ubuntu-mate-welcome") + "/"
old_index_path = os.path.join(welcome_path + "/data/js/applications.json")

print("Software Boutique path: " + repo_root)
print("Welcome path: " + welcome_path)

# Load old index.
if not os.path.exists(old_index_path):
    print("Index can't be loaded.\nThis script assumes ubuntu-mate-welcome repo is cloned alongside software-boutique.")
    exit(1)
else:
    try:
        with open(old_index_path) as f:
            old_index = json.load(f)
    except Exception as e:
        print("Failed to read old index:" + str(e))
        exit(1)

# Functions for saving new data
def write_metadata(data, path):
    f = open(path, "w")
    f.write(json.dumps(data, indent=4))
    f.close()

def write_file(data, path):
    f = open(path, "w")
    f.write(data)
    f.close()

# Wipe folders and create new ones.
categories = ["accessibility", "education", "internet", "office", "unlisted", "accessories", "games", "more-software", "server", "development", "graphics", "multimedia", "system"]
old_to_new_bindings = {
    "accessories": "Accessories",
    "education": "Education",
    "games": "Games",
    "graphics": "Graphics",
    "internet": "Internet",
    "office": "Office",
    "development": "Programming",
    "multimedia": "Media",
    "system": "SysTools",
    "accessibility": "UnivAccess",
    "server": "Servers",
    "more-software": "MoreApps",
    "unlisted": "Unlisted"
}
new_apps_folder = repo_root + "sources/apps/"
old_icons_folder = welcome_path + "data/img/applications/"
old_screenshots_folder = welcome_path + "data/img/applications/screenshots/"

if os.path.exists(new_apps_folder):
    shutil.rmtree(new_apps_folder)
os.makedirs(new_apps_folder)

new_structure = '{' + \
'    "listed": true,\n' + \
'    "name": "",\n' + \
'    "summary": "",\n' + \
'    "developer-name": "",\n' + \
'    "developer-url": "",\n' + \
'    "description": "",\n' + \
'    "tags": "",\n' + \
'    "launch-cmd": "",\n' + \
'    "proprietary": false,\n' + \
'    "alternate-to": null,\n' + \
'    "urls": {\n' + \
'        "info": "",\n' + \
'        "android-app": "",\n' + \
'        "ios-app": ""\n' + \
'    },\n' + \
'    "arch": [],\n' + \
'    "releases": [],\n' + \
'    "method": "apt",\n' + \
'    "installation": {\n' + \
'         "all": {}\n' + \
'    },\n' + \
'    "post-install": [],\n' + \
'    "post-remove": []\n' + \
'}'

for category in categories:
    print("Processing: " + category)
    os.makedirs(new_apps_folder + category)
    old_data = old_index[old_to_new_bindings[category]]
    apps = old_data.keys()

    for appid in apps:
        old_appdata = old_data[appid]
        target_folder = os.path.join(new_apps_folder, category, appid)
        os.makedirs(target_folder)

        shutil.copy(old_icons_folder + old_appdata["img"] + ".png", target_folder + "/icon.png")
        old_screenshots = glob.glob(old_screenshots_folder + old_appdata["img"] + "*")
        shotno = 0
        for path in old_screenshots:
            shotno += 1
            shutil.copy(path, target_folder + "/screenshot-" + str(shotno) + ".jpg")

        metadata_json = json.loads(new_structure, object_pairs_hook=OrderedDict)
        metadata_json["listed"] = old_appdata["working"]
        metadata_json["name"] = old_appdata["name"]
        for line in old_appdata["description"]:
            metadata_json["description"] += line + " "
        metadata_json["launch-cmd"] = old_appdata["launch-command"]
        metadata_json["alternate-to"] = old_appdata["alternate-to"]
        metadata_json["urls"]["info"] = old_appdata["url-info"]
        metadata_json["urls"]["android-app"] = old_appdata["url-android"]
        metadata_json["urls"]["ios-app"] = old_appdata["url-ios"]
        metadata_json["tags"] = old_appdata["subcategory"]

        if old_appdata["open-source"] == True:
            metadata_json["proprietary"] = False
        else:
            metadata_json["proprietary"] = True

        for arch in old_appdata["arch"].split(","):
            metadata_json["arch"].append(arch)

        for release in old_appdata["releases"].split(","):
            metadata_json["releases"].append(release)

        metadata_json["method"] = "apt"
        metadata_json["installation"]["all"]["main-package"] = old_appdata["main-package"]
        metadata_json["installation"]["all"]["install-packages"] = []
        metadata_json["installation"]["all"]["remove-packages"] = []

        # For upgradable
        if "upgrade-packages" in old_appdata:
            metadata_json["installation"]["all"]["install-packages"] = []
            metadata_json["installation"]["all"]["remove-packages"] = []
            for package in old_appdata["install-packages"].split(","):
                # Remove packages should be ignored for upgrades.
                metadata_json["installation"]["all"]["install-packages"].append(package)

        else:
            try:
                for package in old_appdata["install-packages"].split(","):
                    metadata_json["installation"]["all"]["install-packages"].append(package)

                for package in old_appdata["remove-packages"].split(","):
                    metadata_json["installation"]["all"]["remove-packages"].append(package)
            except Exception as e:
                print("Invalid key for '{0}' in '{1}': {2}".format(appid, category, str(e)))

        # FIXME: EARLY UI TESTING ONLY -- These fields are not properly migrated.
        # "pre-install" => "installation"... individual data not migrated, including upgrade data.
        # Sources (e.g. multiverse/universe/main) need to be explictly specified now.
        # Does not write source list files.

        metadata_json["method"] = "dummy"   # Testing UI only.
        metadata_json["installation"]["all"]["source"] = "main"    # That's a lie. Sources are explictly set now.
        metadata_json["summary"] = old_appdata["description"][0] + "..."       # New, each apps needs to write this.
        metadata_json["developer-name"] = "Developer Name"       # New, each apps needs to write this.
        metadata_json["developer-url"] = "http://example.com"       # New, each apps needs to write this.

        write_metadata(metadata_json, target_folder + "/metadata.json")
        write_metadata(old_appdata, target_folder + "/app-data.json.old")

# Now build the index.
print("Finished migration. Now running build...\n")
os.system(repo_root + "scripts/compile-app-index.py")
