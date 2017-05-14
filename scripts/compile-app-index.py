#!/usr/bin/python3
#
# Validates and compiles the application index for use with Software Boutique.
#

import os
import glob
import inspect
import json
import shutil
import sys
import time

colours_supported = sys.stdout.isatty()
def print_msg(color, string):
    """
    color
        1 = Error (Red)
        2 = Success (Green)
        3 = Warning (Yellow)
        4 = Info (Blue)
    """
    if colours_supported:
        print("\033[9{0}m{1}\033[0m".format(str(color), string))
    else:
        print(string)


# Paths and Variables
repo_root = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + "/../"))
source_folder = os.path.join(repo_root, "sources/apps/")
compiled_folder = os.path.join(repo_root, "data/apps/")
index_folder = os.path.join(compiled_folder, "index")
localised_folder = os.path.join(repo_root, "sources/locale-metadata/")
known_codenames = ["all", "xenial", "yakkety", "zesty"]
known_arch = ["i386", "amd64", "armhf", "arm64", "powerpc", "ppc64el"]
known_methods = ["dummy", "apt", "snap"]
known_sources = ["main", "universe", "restricted", "multiverse", "partner", "manual"] # and ppa:*

# Locales used - based on main application's translations.
locale_dir = glob.glob(repo_root + "/sources/locale/*.po")
locales = []
for locale in locale_dir:
    locales.append(os.path.basename(locale[:-3]))

# Begin!
print_msg(4, "Compiling index...")
categories = os.listdir(source_folder)
categories.sort()
new_index = {}

# Clear the previous compiled state
if os.path.exists(compiled_folder):
    shutil.rmtree(compiled_folder)
os.mkdir(compiled_folder)
for folder in ["icons", "screenshots", "source-lists", "index"]:
    os.mkdir(compiled_folder + folder)

# Validate and add each application.
faults = False
for category in categories:
    new_index[category] = {}
    apps = os.listdir(os.path.join(source_folder, category))
    apps.sort()

    for appid in apps:
        # Spaces are not allowed in app IDs.
        if appid.find(" ") != -1:
            print_msg(1, "{0}/{1} = Spaces are not allowed in app ID.".format(category, appid))
            continue

        # Is there config stored for this?
        json_path = os.path.join(source_folder, category, appid, "metadata.json")
        if not os.path.exists(json_path):
            print_msg(1, "{0}/{1} = Missing metadata.json!".format(category, appid))
            continue

        # Load JSON Index
        try:
            with open(json_path) as f:
                index = json.load(f)
        except Exception as e:
            print_msg(1, "{0}/{1} = Corrupt metadata.json! (Exception: {2})".format(category, appid, str(e)))
            continue

        # If unlisted, skip this.
        try:
            if index["listed"] == False:
                print_msg(3, "{0}/{1} = Marked as unlisted, skipping...".format(category, appid))
                continue
        except Exception:
            print_msg(1, "{0}/{1} = No 'listed' key. Skipping...".format(category, appid))
            break

        # Check the required fields are present.
        def check_field(key, key_type, is_required, subkey=None):
            global faults
            if is_required:
                if subkey:
                    try:
                        target = index[key][subkey]
                    except KeyError:
                        print_msg(1, "{0}/{1} = Missing required subkey '{2}' for key '{3}'".format(category, appid, subkey, key))
                        faults = True
                        return
                else:
                    try:
                        target = index[key]
                    except KeyError:
                        print_msg(1, "{0}/{1} = Missing required key '{2}'".format(category, appid, key))
                        faults = True
                        return
            else:
                try:
                    if subkey:
                        target = index[key][subkey]
                    else:
                        target = index[key]
                except KeyError:
                    print_msg(3, "{0}/{1} = Optional key missing, consider adding it with null instead: '{2}'".format(category, appid, key))
                    faults = True
                    return

            if target and not type(target) == key_type:
                if subkey:
                    print_msg(1, "{0}/{1} = Wrong key type '{2}' for subkey '{3}' (should be {4})".format(category, appid, key, subkey, str(key_type).split("'")[1]))
                    faults = True
                    return
                else:
                    print_msg(1, "{0}/{1} = Wrong key type '{2}' (should be {3})".format(category, appid, key, str(key_type).split("'")[1]))
                    faults = True
                    return

            # If a required field, check there is actually data there.
            if key_type in [str, list] and is_required:
                try:
                    if len(target) == 0:
                        print_msg(3, "{0}/{1} = Warning: No data for '{2}'. Skipping!".format(category, appid, key))
                except Exception:
                    print_msg(1, "{0}/{1} = Invalid data: '{2}'".format(category, appid, key, target))

        check_field("listed", bool, True)
        check_field("name", str, True)
        check_field("description", str, True)
        check_field("developer-name", str, True)
        check_field("developer-url", str, True)
        check_field("tags", list, True)
        check_field("launch-cmd", str, False)
        check_field("alternate-to", str, False)
        check_field("proprietary", bool, True)
        check_field("urls", dict, True)
        check_field("urls", str, True, "info")
        check_field("arch", list, True)
        check_field("releases", list, True)
        check_field("method", str, True)
        check_field("installation", dict, True)
        check_field("installation", dict, True, "all")
        check_field("post-install", list, False)
        check_field("post-remove", list, False)

        if index.get("method") == "apt":
            codenames = index["installation"].keys()
            for raw_codename in codenames:
                # Checks for typos in every "declared" codename.
                for name in raw_codename.split(','):
                    if name not in known_codenames:
                        print_msg(3, "{0}/{1} = Unrecognised codename '{2}'".format(category, appid, name))

                # Required data
                apt_data = index["installation"][raw_codename]
                try:
                    apt_data["main-package"]
                    apt_data["install-packages"]
                    apt_data["remove-packages"]
                except KeyError:
                    print_msg(1, "{0}/{1} = At least one is missing: main-package, install-packages, remove-packages".format(category, appid))
                    continue

                if not type(apt_data["main-package"]) == str or not type(apt_data["install-packages"]) == list or not type(apt_data["remove-packages"]) == list:
                    print_msg(1, "{0}/{1} = At least one has the wrong data type: main-package, install-packages, remove-packages".format(category, appid))
                    continue

                # Check the Apt source is valid.
                source = apt_data["source"]
                if not source.startswith("ppa:"):
                    if source not in known_sources:
                        print_msg(1, "{0}/{1} = Unrecognised source '{2}'. Installation would fail.".format(category, appid, source))

                # If it's a manual source file, these are required.
                if apt_data["source"] == "manual":
                    try:
                        list_filename = apt_data["list-file"]
                    except KeyError:
                        print_msg(1, "{0}/{1} = Manual source specified, but no list file was specified.".format(category, appid))
                        continue

                    list_pathname = os.path.join(source_folder, category, appid, list_filename)
                    if os.path.exists(list_pathname):
                        shutil.copyfile(list_pathname, os.path.join(compiled_folder, "source-lists", list_filename))
                    else:
                        print_msg(1, "{0}/{1} = Manual source specified, but list file is missing.".format(category, appid))
                        continue

                    if not apt_data.get("list-key-url") and not apt_data.get("list-key-server"):
                        print_msg(1, "{0}/{1} = Manual source specified, but no key server or URL was set.".format(category, appid))
                        continue

        if index.get("method") not in known_methods:
            print_msg(1, "{0}/{1} = Unrecognised method '{2}'".format(category, appid, index.get("method")))
            break

        for arch in index.get("arch"):
            if arch not in known_arch:
                print_msg(3, "{0}/{1} = Unrecognised architecture '{2}'".format(category, appid, arch))

        # Add to compiled index if successful
        if faults:
            continue

        new_index[category][appid] = index
        source_dir = os.path.join(source_folder, category, appid)
        shutil.copyfile(os.path.join(source_dir, "icon.png"), os.path.join(compiled_folder, "icons", appid + ".png"))
        file_list = os.listdir(os.path.join(source_dir))
        for filename in file_list:
            if filename.startswith("screenshot-"):
                screenshot_no = filename.split("-")[1][:1]
                shutil.copyfile(os.path.join(source_dir, filename), os.path.join(compiled_folder, "screenshots", appid + "-" + str(screenshot_no) + ".jpg"))

# If validation fails, abort compiling.
if faults:
    print_msg(1, "\nIndex validation failed!")
    print_msg(0, "Please fix or unlist the faulty software.\n")
    exit(1)

# Compile statistics
categories_no = 0
apps_no = 0
for category in new_index.keys():
    if category not in ["unlisted", "stats"]:
        categories_no += 1
        category_apps = new_index[category].keys()
        apps_no += len(category_apps)

new_index["stats"] = {
    "categories": categories_no,
    "apps": apps_no,
    "compiled": int(time.time())
}

# Save new index to file
with open(os.path.join(index_folder, "en.json"), 'w') as f:
    json.dump(new_index, f, sort_keys=True)

# Now assemble translatable versions of the index.
print_msg(4, "Compiling localised indexes...")
for locale in locales:
    localised_index = new_index.copy()
    for category in categories:
        apps = os.listdir(os.path.join(source_folder, category))
        for appid in apps:
            try:
                # Only translate the app if a PO file exists for it.
                if os.path.exists(os.path.join(localised_folder, appid, locale + ".po")):
                    temp_json = "/tmp/" + appid + ".json"
                    # po2json "damages" the structure, so just take what we need.
                    os.system("po2json {0}/{1}/{2}.po -t {3}/{4}/{1}/metadata.json -o ".format(localised_folder, appid, locale, source_folder, category) + temp_json + " --progress none")
                    with open(temp_json) as f:
                        index = json.load(f)
                    os.remove(temp_json)
                    localised_index[category][appid]["name"] = index["name"]
                    localised_index[category][appid]["summary"] = index["summary"]
                    localised_index[category][appid]["description"] = index["description"]
                    localised_index[category][appid]["developer-name"] = index["developer-name"]
            except Exception:
                print_msg(1, "{0}/{1} = Failed to translate metadata!".format(category, appid))
                continue

    # Save this localised index
    with open(os.path.join(index_folder, locale + ".json"), 'w') as f:
        json.dump(new_index, f, sort_keys=True)

print_msg(2, "Index ready to go.")
