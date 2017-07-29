#! /usr/bin/python3
# -*- coding:utf-8 -*-
#
# Copyright 2015-2017 Luke Horwell <luke@ubuntu-mate.org>
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

dbg = object()

class Preferences(object):
    def __init__(self, dbg_obj, config_name):
        global dbg
        dbg = dbg_obj
        self.config_folder = os.path.join(os.path.expanduser('~'), ".config", "software-boutique")
        self.cache_folder = os.path.join(os.path.expanduser('~'), ".cache", "software-boutique")
        self.revision_file = os.path.join(self.cache_folder, "revision")
        self.config_file = os.path.join(self.config_folder, config_name + ".json")
        self.config_data = {}
        self.load_from_disk()

    def load_from_disk(self):
        """
        Loads configuration from disk.
        Initialises the folder structure and file if necessary.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file) as stream:
                    self.config_data = json.load(stream)
            except Exception as e:
                dbg.stdout("Failed to read preferences file. Re-creating.", 1, 1)
                self.init_config()
        else:
            self.init_config()

    def save_to_disk(self):
        """
        Commit the data from memory to disk.
        Returns True or False depending on success/failure.
        """
        # Create file if it doesn't exist.
        if not os.path.exists(self.config_file):
            open(self.config_file, 'w').close()

        # Write new data to specified file.
        if os.access(self.config_file, os.W_OK):
            f = open(self.config_file, "w+")
            f.write(json.dumps(self.config_data))
            f.close()
            return True
        else:
            return False

    def write(self, setting, value):
        """
        Write new data to memory.
        """
        try:
            self.config_data[setting] = value
            self.save_to_disk()
        except:
            dbg.stdout("Failed to write '{0}' = '{1}'.".format(setting, value), 1, 1)

    def read(self, setting, default_value=None):
        """
        Read data from memory.
        """
        try:
            value = self.config_data[setting]
            return value
        except:
            # Should it be non-existent, use the default value instead.
            dbg.stdout("No value exists for '{0}'. Writing '{1}'.".format(setting, default_value), 1, 2)
            self.write(setting, default_value)
            return default_value

    def init_config(self):
        try:
            os.makedirs(self.config_folder)
        except FileExistsError:
            pass
        self.config_data = {}
        if self.save_to_disk():
            dbg.stdout(("Successfully created new preferences file: " + self.config_file), 1, 3)
            return True
        else:
            dbg.stdout("Failed to create new preferences file:" + self.config_file, 1, 1)
            return False

    def init_cache(self):
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)
            os.makedirs(self.cache_folder + "metadata")

    def get_index_revision(self):
        if not os.path.exists(self.revision_file):
            return 0
        else:
            with open(self.revision_file, "r") as f:
                return int(f.readline())

    def set_index_revision(self, new_rev):
        f = open(self.revision_file, "w")
        f.write(str(new_rev))
        f.close()
