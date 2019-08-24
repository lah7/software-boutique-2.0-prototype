"""
Common functions shared between Software Boutique and the Welcome application.
"""
# Licensed under GPLv3
#
# Copyright 2017-2019 Luke Horwell <code@horwell.me>
#

import os
import gettext
import sys
import inspect
import subprocess

try:
    from pylib.decorators.singleton import singleton
except ImportError:
    from software_boutique.decorators.singleton import singleton

@singleton
class Debugging(object):
    """
    Outputs pretty debugging details to the terminal.

    Verbose Levels:
    0       Only critical errors
    1       Info and debugging info
    2       Info and debugging info + opens web inspector
    """
    def __init__(self):
        self.verbose_level = 0

        # Colours for stdout
        self.error = '\033[91m'
        self.success = '\033[92m'
        self.warning = '\033[93m'
        self.action = '\033[93m'
        self.debug = '\033[96m'
        self.normal = '\033[0m'

    def stdout(self, msg, colour='\033[0m', verbosity=0):
        """
        Params:
            msg         str     String containing message for stdout.
            colour      str     stdout code (e.g. '\033[92m' or dbg.success)
            verbosity   int     0 = Always show
                                1 = -v flag
                                2 = -vv flag
        """
        if self.verbose_level >= verbosity:
            # Only colourise output if running in a real terminal.
            if sys.stdout.isatty():
                print(colour + msg + '\033[0m')
            else:
                print(msg)


def get_data_source():
    """
    Returns the path for the application's UI data files.
    """
    current_folder = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "../data/")
    try:
        snap_folder = os.path.join(os.environ["SNAP"], "usr", "share", "software-boutique")
    except KeyError:
        snap_folder = ""
    system_folder = os.path.join("/", "usr", "share", "software-boutique")

    for folder in [current_folder, snap_folder, system_folder]:
        if os.path.exists(folder):
            return folder


def setup_translations(bin_path, i18n_app, locale_override=None):
    """
    Initalises translations for the application.

    Params:
        bin_path    str     __file__ of the application that is being executed.
        i18n_app    str     Name of the application's locales.

    Returns:
        gettext object (commonly assigned to a _ variable)
    """
    whereami = os.path.abspath(os.path.join(os.path.dirname(bin_path)))

    if os.path.exists(os.path.join(whereami, "locale/")):
        # Using relative path
        locale_path = os.path.join(whereami, "locale/")
    else:
        # Using system path or en_US if none found
        locale_path = "/usr/share/locale/"

    if locale_override:
        t = gettext.translation(i18n_app, localedir=locale_path, fallback=True, languages=[locale_override])
    else:
        t = gettext.translation(i18n_app, localedir=locale_path, fallback=True)

    return t.gettext


def _parse_os_release():
    with open("/etc/os-release") as f:
        d = {}
        for line in f:
            k, v = line.rstrip().split("=")
            d[k] = v
    return d


def get_distro_name():
    d = _parse_os_release()
    return d["ID"].replace("\"", "")


def get_distro_version():
    d = _parse_os_release()
    try:
        return d["VERSION"].replace("\"", "")
    except KeyError:
        return ""


def get_distro_arch():
    return "amd64"
    # FIXME: Needs to be distro agnostic.
    # return str(subprocess.Popen(["dpkg", "--print-architecture"], stdout=subprocess.PIPE).communicate()[0]).strip('\\nb\'')


def spawn_thread(target, daemon=True, args=[]):
    """
    Creates another thread to run a function in the background.
    """
    newthread = Thread(target=target, args=(args))
    if daemon:
        newthread.daemon = True
    newthread.start()
