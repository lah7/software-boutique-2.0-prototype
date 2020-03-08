"""
Controller layer that interfaces between the backend (libboutique) and
the view.
"""

import os
import json
import webbrowser

from . import common as Common
from . import controller as Controller
from . import locales as Locales
from . import preferences as Preferences

Locales = Locales.LOCALES
dbg = None

# Minimum version of the curated index supported by this version of the program.
__INDEX_MIN_VER__ = 7


class SoftwareBoutiqueController(object):
    """
    The middleman for requests and responses passed between the view and model.
    """
    def __init__(self, app, args):
        """
        Prepare the backend and main application.
        """
        self.app = app
        self.args = args
        self.data_source = Common.get_data_source()
        self.send_data = app.send_data
        self.set_view_variable = app.set_view_variable
        self.dbg = app.dbg
        self.pref = Preferences.Preferences(dbg, "preferences", "software-boutique")
        self.index = None

        # FIXME: libboutique: Get status of apt, snap and appstream.
        self.available_backends = {
            "apt": False,
            "snap": False,
            "appstream": False
        }

        # Is the index working?
        index_available = False
        index_timestamp = None
        index_revision = None
        index_name = None
        index_info_url = None
        index_support_url = None
        index_path = os.path.join(self.data_source, "index", "applications-en.json")
        if os.path.exists(index_path):
            try:
                with open(index_path, "r") as f:
                    self.index = json.load(f)
                index_timestamp = self.index["stats"]["compiled"]
                index_revision = self.index["stats"]["revision"]
                index_name = self.index["distro"]["name"]
                index_info_url = self.index["distro"]["info_url"]
                index_support_url = self.index["distro"]["support_url"]
                index_available = True
                self.dbg.stdout("Index successfully loaded.", self.dbg.success)
            except Exception as e:
                self.dbg.stdout("Failed to load index: " + str(e), self.dbg.error)
        else:
            self.dbg.stdout("Curated index not present.", self.dbg.warning, 1)

        # Define settings
        self.settings = {
            "version": {
                "boutique": app.version
            },
            "index": {
                "available": index_available,
                "name": index_name,
                "info_url": index_info_url,
                "support_url": index_support_url,
                "timestamp": index_timestamp,
                "revision": index_revision
            },
            "backends": {
                "apt": self.available_backends["apt"],
                "snap": self.available_backends["snap"],
                "appstream": self.available_backends["appstream"]
            },
            "hide_proprietary": self.pref.read("hide_proprietary", False),
            "show_advanced": self.pref.read("show_advanced", False),
            "precise_time": self.pref.read("precise_time", False),
            "compact_list": self.pref.read("compact_list", False)
            # add default tab
        }
        self.set_view_variable("SETTINGS", self.settings)


    ##################################################
    def _example(self):
        # Update lower-left current status with Ready status
        self.update_queue_state("ok", Locales["queue_ready"], None, 0, -1)

        # Dummy queue data - stored in the controller. View has copy (used to view page)
        queue = [
            {
                "id": "apt:app1",           # This ID is the view's way of telling the model/controller what the source is.
                "name": "Caja",             # Human name for application
                "icon": "",                 # Path or empty to show generic icon
                "action": "install",        # install, remove
                "state": "pending",         # pending, processing, processed
                "success": False            # If "processed", states whether operation was successful.
            },
            {
                "id": "snap:ubuntu-mate-welcome",
                "name": "Ubuntu MATE Welcome",
                "icon": "",
                "action": "install",
                "state": "processed",
                "success": True
            }
        ]

        # Dummy progress bar
        app_name = "Caja"
        current_MB = 0
        total_MB = 5
        # These strings are human-readable for translators, but are intended to be manipulated, e.g. "XX", "1", "2"
        action_text = locales["queue_downloading"].replace("XX", app_name).replace("1", str(current)).replace("2", str(total))
        details_text = locales["queue_progress"].replace("1", str(current_MB)).replace("2", str(total_MB))

        # Update lower-left current status with new status
        self.update_queue_state("busy", action_text, details_text, str(current_MB), str(total_MB))

        # Update the view when the queue changes. This would update the page.
        self.update_queue_list(data)

    ##################################################

    def process_view_request(self, request_name, data):
        """
        Processes a request sent from the view by matching the request to the
        function and passing the Python dictonary (data).
        """
        bindings = {
            # Callbacks for queued items
            "update_queue_list": self._update_queue_list,
            "update_queue_state": self._update_queue_state,

            # Queue requests
            "queue_clear": self._queue_clear,
            "queue_drop_item": self._queue_drop_item,

            # App requests
            "request_category_list": self._request_category_list,
            "app_info": self._app_info,
            "app_launch": self._app_launch,
            "app_show_error": self._app_show_error,
            "app_reinstall": self._app_reinstall,
            "app_remove": self._app_remove,
            "app_install": self._app_install,

            # General
            "open_uri": self._open_uri,
            "settings_set_key": self._settings_set_key
        }

        try:
            bindings[request_name](data)
        except KeyError as e:
            dbg.stdout("Request failed: " + request_name, dbg.error)
            dbg.stdout("Exception:", dbg.error)
            raise e
            return False

    def shutdown(self):
        """
        The user requested to quit Software Boutique. Gracefully stop all operations
        and threads.

        If it is not possible to stop right now, return False.
        """
        return True

    def _open_uri(self, data):
        """
        Opens a specified URI. Only HTTP/HTTPS is accepted.
        """
        uri = data["uri"]

        if uri[:4] == "http":
            webbrowser.open(uri, new=0, autoraise=True)

    def _settings_set_key(self, data):
        """
        Writes a new value to a key for this application's preferences.
        """
        key = data["key"]
        value = data["value"]
        self.pref.write(key, value)

    def _update_queue_list(self, queue):
        """
        Callback: For when items in the queue has changed.

        Params:
            queue           List containing queue JSON data.
        """
        self.send_data("update_queue_list", queue)

    def _update_queue_state(self, state, action_text, details_text, value, value_end):
        """
        Callback: When the current item in the queue has changed state.

        Params:
            state           String of either: "ok", "busy", "error". Determines icon.
            action_text     String indicating the main operation.
            details_text    Optional string for action text, e.g. download size or verbose progress text.
            value           Value for progress bar, e.g. current download size. Use -1 for indeterminate.
            value_end       Max value for progress bar, e.g. total download size. Use 0 to hide progress.
        """
        self.send_data("update_queue_state", {
            "state": state,
            "action_text": action_text,
            "details_text": details_text,
            "value": value,
            "value_end": value_end
        })

    def _queue_clear(self, data):
        """
        Request: User clears all completed items in the queue.
        """
        pass

    def _queue_drop_item(self, data):
        """
        Request: User drops a specific application from the queue.
        If the item is being processed, the changes should abort (or revert) if possible.
        """
        pass

    def _request_category_list(self, data):
        """
        Request: User is listing all the curated applications in a category.
        """
        category = data["category"]
        element = data["element"]

        # FIXME: Dummy response
        self.send_data("populate_app_list", {
            "category": category,
            "element": element,
            "apps": [
                {
                    "name": "Application 1",
                    "id": "apt:app1",
                    "backend": "apt",
                    "icon": "",
                    "installed": True,
                    "summary": "This is a short line describing this application"
                },
                {
                    "name": "Application 2",
                    "id": "snap:app2",
                    "backend": "snap",
                    "icon": "",
                    "installed": False,
                    "summary": "This is a short line describing this application"
                },
                {
                    "name": "Application 3",
                    "id": "curated:app3",
                    "backend": "curated",
                    "icon": "",
                    "installed": True,
                    "summary": "This is a short line describing this application"
                }
            ]
        })

    def _app_info(self, data):
        """
        Request: User is viewing details for a specific application.
        """
        # FIXME: Dummy response
        self.send_data("open_app_details", {
            "data": {
                "name": "Application 1",
                "id": "apt:app1", # This ID is the view's way of telling the model/controller what the source is.
                "backend": "apt",
                "icon": "", # Path to icon, or blank for generic icon.
                "summary": "Calculator for the GTK desktop",
                "description": "This is line 1.\nThis is line 2.\nThis is line 3.",
                "nonfree": False,
                "free_license": "GNU General Public License",
                "arch": ["i386", "amd64", "armhf", "arm64", "powerpc"],
                "developer": "Developer Name",
                "developer_url": "https://developer.example.com",
                "website_url": "https://example.com",
                "support_url": "https://support.example.com",
                "apt_source": "ppa:org/name", # "main", "universe", "multiverse", "restricted", "partner", "ppa:org/name", "https://repo.example.com"
                "apt_packages": ["app1", "app1-data", "app1-doc"],
                "snap_name": "nameofsnap",
                "launch_cmd": "app1",
                "tags": [], # TODO: Curated only? may be unused
                "screenshots": [
                    "/path/to/screenshot-1.jpg",
                    "/path/to/screenshot-2.jpg"
                ],
                "version": "20.04.1-ubuntu0",
                "installed": True,
                "install_date": [2019, 12, 31, 23, 59] # [YYYY, MM, DD, HH, MM]
            }
        })

    def _app_launch(self, data):
        """
        Request: User would like to run an application, if it has an executable to launch.
        """
        pass

    def _app_show_error(self, data):
        """
        Callback: One of the items in the queue encountered an error.
        """
        pass

    def _app_reinstall(self, data):
        """
        Request: User would like to re-install this application.
        """
        pass

    def _app_remove(self, data):
        """
        Request: User would like to remove this application.
        """
        pass

    def _app_install(self, data):
        """
        Request: User would like to install this application.
        """
        pass
