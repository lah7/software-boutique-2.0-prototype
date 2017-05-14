#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2016-2017 Luke Horwell <luke@ubuntu-mate.org>
#
# Software Boutique is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Software Boutique is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Software Boutique. If not, see <http://www.gnu.org/licenses/>.
#

import os
import json
import platform
import subprocess
import requests

# Apt Imports
#~ from gi.repository import PackageKitGlib as packagekit

verbose = False

# Paths
cache_path = os.path.join(os.path.expanduser('~'), ".cache", "software-boutique")
installed_index = os.path.join(os.path.expanduser('~'), ".config", "software-boutique", "installed.json")
data_source = "/usr/share/ubuntu-mate-welcome/"

# Session Details
force_dummy = False
dbg = object() # Until main runtime replaces this.
system_arch = str(subprocess.Popen(["dpkg", "--print-architecture"], stdout=subprocess.PIPE).communicate()[0]).strip('\\nb\'')
system_locale = "en"
current_os_version = platform.dist()[1] # E.g. 16.04
current_os_codename = platform.dist()[2] # E.g. xenial


# Application Data
def read_index(json_path):
    """
    Reads the specified JSON path and returns it as a dictonary.
    """
    with open(json_path) as f:
        data = json.load(f)
    return(data)


def get_application_details(backend, index_data, category, appid):
    """
    Returns an object holding the details about the application.

    backend         = Object containing the SoftwareInstallation.Backend() class.
                      This main application will initialise this class.
    index_data      = Data from index_data[category][appid]
    category        = ID of category from index.
    appid           = ID of application from index.
    """
    app = ApplicationData()
    data = index_data[category][appid]

    app.appid = appid
    app.categoryid = category
    app.uuid = app.categoryid + "-" + app.appid

    app.name = data.get("name")
    app.summary = data.get("summary")
    app.description = data.get("description")
    app.tags = data.get("tags")
    app.launch_cmd = data.get("launch-cmd")
    app.proprietary = data.get("proprietary")
    app.urls = data.get("urls")
    app.arch = data.get("arch")
    app.releases = data.get("releases")
    app.method = data.get("method")
    app.post_install = data.get("post-install")
    app.post_remove = data.get("post-remove")

    app.icon_path = os.path.join("apps", "icons", appid + ".png")

    app.screenshot_filenames = []
    for filename in screenshot_file_listing:
        if filename.startswith(appid + "-"):
            app.screenshot_filenames.append(filename)

    installation_data = data.get("installation")
    if app.method == "dummy" or force_dummy:
        app.installation = SoftwareInstallation.Dummy(installation_data, backend)
    elif app.method == "apt":
        app.installation = SoftwareInstallation.PackageKit(installation_data, backend)
    elif app.method == "snap":
        app.installation = SoftwareInstallation.Snappy(installation_data, backend)
    else:
        print(app.installation + " is not supported!")
        return None

    app.is_installed = app.installation.is_installed

    return app


class ApplicationData():
    """
    Object that holds details about an application.

    The object is expected to be manipulated outside this class.
    """
    # IDs
    appid = ""
    categoryid = ""
    uuid = ""

    # Holds raw dictonary data
    data = {}

    # Variables from index
    name = ""
    summary = ""
    description = ""
    developer_name = ""
    developer_url = ""
    tags = []
    launch_cmd = None
    proprietary = False
    alternate_to = None
    urls = {}
    arch = []
    releases = []
    method = "dummy"
    post_install = None
    post_remove = None

    # Variables Computed
    icon_path = ""
    screenshot_filenames = []
    install_date = 0
    install_date_string = ""

    # On-demand classes
    installation = None   # SoftwareInstallation.subclass()

    # On-demand functions
    is_installed = None   # Alias installation.is_installed function


class SoftwareInstallation():
    """
    Manages software installations with different methods.

    Required functions:

        __init__(self)
            Prepares that object, e.g. set up Apt.

            installation_data = Raw JSON of the "installation" group.
                                Depending on the class, this data will be handled differently.
            backend           = Object containing the Backend() class.

        is_installed(self, params)
            Returns True or False whether the application is considered installed.

            app_obj = AppInfo() object. Can be used for extracting required data, e.g. snap/package name.

        do_install, do_remove, do_upgrade (self, params)
            Returns True for a successful change, or False is something failed.

            app_obj = AppInfo() object. Can be used for extracting required data, e.g. snap/package name.
            ui_obj  = XXXXXXXX object. Allows functions to be called to indicate progress.

        Functions starting with _ may be used for miscellaneous purposes and can be defined within the class.
            E.g. Apt uses _update_cache() for both on-demand cache refreshing and when installing a new source.
    """
    class Backend(object):
        """
        Stores persistant objects for back-ends, such as the cache for Apt.
        """
        def __init__(self):
            return


    class Dummy(object):
        """
        Dummy implementation for debugging software changes.
        """
        def __init__(self, installation_data, backend):
            self.raw_data = installation_data
            self.backend = backend

            # This dummy pretends to look busy.
            import time
            return

        def is_installed(self):
            return False

        def do_install(self, ui_obj):
            time.sleep(2)
            return True

        def do_remove(self, ui_obj):
            time.sleep(2)
            return True

        def do_upgrade(self, ui_obj):
            time.sleep(1)
            return True


    class PackageKit(object):
        """
        Apt implementation using PackageKit as its back-end.
        """
        def __init__(self, installation_data, backend):
            self.raw_data = installation_data
            self.backend = backend
            return

        def is_installed(self):
            return False

        def do_install(self, ui_obj):
            return True

        def do_remove(self, ui_obj):
            return True

        def do_upgrade(self, ui_obj):
            return True

        def _update_cache(self):
            return True

        @staticmethod
        def _is_running_ubuntu_mate():
            """
            Determines whether the user is actually running Ubuntu MATE determined if the
            2 main metapackages are installed and whether the session is running MATE.

            => Returns bool
            """
            # FIXME: if ubuntu-mate-desktop or ubuntu-mate-core are not installed and not running MATE => return False
            if os.environ.get('DESKTOP_SESSION') != "mate":
                return False
            else:
                return True

        @staticmethod
        def _is_boutique_subscribed():
            """
            Checks whether Welcome/Software Boutique is subscribed for updates.

            => Returns bool
            """
            ppa_file = "/etc/apt/sources.list.d/ubuntu-mate-dev-ubuntu-welcome-" + current_os_codename + ".list"
            if os.path.exists(ppa_file):
                if os.path.getsize(ppa_file) > 0:
                    return True
            return False

        def _is_upgradable(self):
            """
            Checks whether the software is going to be upgraded or not. E.g. LibreOffice PPA.

            => Returns bool
            """
            # FIXME:
            return False

        def _get_instructions_for_this_codename(self):
            """
            Returns the dictonary containing the metadata for the current codename.
            E.g. If we're running 16.04 and there's a "xenial,yakkety" group
                Otherwise, "all" is used.

            => Returns string
            """
            target_key = "all"
            for codenames_raw in self.raw_data.keys():
                codenames = codenames_raw.split(",")
                if current_os_codename in codenames:
                    target_key = codenames_raw
            return(self.raw_data[target_key])

        def _get_package_list(self, install_type):
            """
            Returns a list of packages based on the type of installation.

            install_type    =   Expects "install", "remove", "upgrade".

            => Returns list
            """
            filtered_index = self._get_instructions_for_this_codename()

            if install_type == "install":
                return(filtered_index["install-packages"])

            elif install_type == "remove":
                return(filtered_index["remove-packages"])

            elif install_type == "upgrade":
                return(filtered_index["upgrade-packages"])

            else:
                return([])


    class Snappy(object):
        """
        Snaps implementation.
        """
        def __init__(self, installation_data, backend):
            self.raw_data = installation_data
            self.backend = backend
            return

        def is_installed(self):
            return True

        def do_install(self, ui_obj):
            return True

        def do_remove(self, ui_obj):
            return True

        def do_upgrade(self, ui_obj):
            return True

    #~ class WebApps(object):
        #~ def __init__(self):
            #~ return


def print_app_installation_buttons(app_obj, string_dict, show_details_btn):
    """
    Returns the HTML for the buttons that determines the installation/launch options.

    app_obj     =   ApplicationData() object
    string_dict =   A dictonary of the strings, passed via the main
                    application so they're translated in one place.
                    e.g. {
                        details_text = "Details",
                        details_tooltip = "Learn more about this application",
                        install_text = "Install",
                        install_tooltip = "Install this application on your computer",
                        upgrade_text = "Upgrade",
                        upgrade_tooltip = "Adds a repository which will install a newer version of this software.",
                        reinstall_text = "",
                        reinstall_tooltip = "Reinstall this application",
                        remove_text = "",
                        remove_tooltip = "Remove this application",
                    }
    show_details_btn = True/False whether the details button should be shown here.
    """
    html = ""

    def _generate_button_html(cmd, app_obj, colour_class, fa_icon, text, tooltip):
        if fa_icon:
            icon_html = "<span class='fa {0}'></span>".format(fa_icon)
        else:
            icon_html = "<img src='{0}'/>".format(app_obj.icon_path)

        return "<button class='dialog-theme {2}' onclick='cmd(\"{0}?{1}\")' title='{5}'>{3} {4}</button>".format(
            cmd, app_obj.categoryid + "?" + app_obj.appid, colour_class, icon_html, text, tooltip
        )

    if show_details_btn:
        html += _generate_button_html(
                    "details", app_obj, "white", "fa-info-circle", string_dict["details_text"], string_dict["details_tooltip"]
                )

    if app_obj.is_installed():
        # For detail view, show icon on the far left.
        if not show_details_btn and app_obj.launch_cmd:
            html += _generate_button_html(
                        "launch", app_obj, "inverted", None, string_dict["launch_text"], string_dict["launch_tooltip"]
                    )

        html += _generate_button_html(
                    "install", app_obj, "yellow", "fa-refresh", string_dict["reinstall_text"], string_dict["reinstall_tooltip"]
                )

        html += _generate_button_html(
                    "remove", app_obj, "red", "fa-trash", string_dict["remove_text"], string_dict["remove_tooltip"]
                )

        # For card view, show icon on the far right.
        if show_details_btn and app_obj.launch_cmd:
            html += _generate_button_html(
                        "launch", app_obj, "inverted", None, string_dict["launch_text"], string_dict["launch_tooltip"]
                    )

    else:
        html += _generate_button_html(
                    "install", app_obj, "green", "fa-download", string_dict["install_text"], string_dict["install_tooltip"]
                )

    return(html)

