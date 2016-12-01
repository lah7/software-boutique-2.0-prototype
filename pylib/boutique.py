#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2016 Luke Horwell <luke@ubuntu-mate.org>
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
#~ from gi.repository import PackageKitGlib as packagekit

class IndexMeta(object):
    """
    Reads the JSON index into memory, and returns
    objects containing details about that application.

    dbg         = Debug object from application.
    index_path  = Path to the JSON (e.g. applications.json)
    """
    def __init__(self, dbg, index_path):
        self.index_path = index_path
        self.dbg = dbg
        self.index_data = None

    def read_index(self):
        self.dbg.stdout("Reading index...", 3, 2)
        try:
            with open(self.index_path) as f:
                self.index_data = json.load(f)
            self.dbg.stdout("Successfully read index: " + self.index_path, 2, 2)
        except Exception as e:
            self.index_data = None
            self.dbg.stdout("Exception reading index: " + str(e), 1, 0)

    def read_info(self, category, app_id):
        try:
            self.dbg.stdout("Reading: {0} --> {1}".format(category, app_id), 3, 2)
            obj = self.AppInfo(self.dbg, self.index_data[category][app_id])
            self.dbg.stdout("     OK: {0} --> {1}".format(category, app_id), 2, 2)
            return(obj)
        except:
            self.dbg.stdout("  ERROR: {0} --> {1}".format(category, app_id), 1, 0)

    class AppInfo(object):
        """
        Object that stores details about the application.

        dbg     = Debug object from application.
        data    = JSON passed from read_info function.
                    This only has condensed data from index_data[category][app_id]
        """
        def __init__(self, dbg, data):
            self.raw = data
            # Required
            try:
                self.name = data["name"]
                self.open_source = data["open-source"]
                self.url_info = data["url-info"]
                self.arch = data["arch"]
                self.releases = data["releases"]
                self.methods = data["methods"]
            except Exception as e:
                dbg.stdout(" -- Missing required data: " + str(e), 1, 0)

            # Optional
            try:
                self.launch_command = data["launch-command"]
            except:
                self.launch_command = None

            try:
                self.description = data["description"]
            except:
                self.description = None

            try:
                self.alternate_to = data["alternate-to"]
            except:
                self.alternate_to = None

            try:
                self.tags = data["tags"]
            except:
                self.tags = None

            try:
                self.url_android = data["url-android"]
            except:
                self.url_android = None

            try:
                self.url_ios = data["url-ios"]
            except:
                self.url_ios = None


class ApplicationMeta(object):
    """
    Fetches metadata about packages.
    """
    def __init__(self):
        return

    def get_metadata_for_package(self, package_name):
        return

    def get_metadata_for_index(self, app_obj):
        return


class SoftwareInstallation():
    """
    Manages software installations with different methods.
    """
    class PackageKit(object):
        def __init__(self):
            return

        def is_installed(self, packages):
            return True

        def do_install(self, packages):
            return 0

        def do_remove(self, packages):
            return 0

        def do_upgrade(self, packages):
            return 0
