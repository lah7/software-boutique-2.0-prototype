"""
Shared variables across modules. Contains configuration and session data.
"""

import os
from . import common as common

# Path to application cache
cache_path = os.path.join(os.path.expanduser('~'), ".cache", "software-boutique")

if not os.path.exists(cache_path):
    os.mkdir(cache_path)

# Path to curated index
index_path = os.path.join(os.path.expanduser('~'), ".config", "software-boutique", "installed.json")
if not os.path.exists(index_path):
    index_path = None

# System information
os_arch = common.get_distro_arch() # amd64
os_version = common.get_distro_version()  # 19.10
os_codename = common.get_distro_name()  # eoan
