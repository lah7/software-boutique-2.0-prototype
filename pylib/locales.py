"""
A dictionary containing all of the locales that are used in the view.

The view will store locales as a JSON object under the 'LOCALE' variable
when the application starts.
"""

import gettext
from . import common

_ = common.setup_translations(__file__, "software-boutique")

LOCALES = {
    # General
    "title": _("Software Boutique"),

    # Header Buttons
    "browse": _("Browse"),
    "queue": _("Queue (0)"), # 0
    "installed": _("Installed"),
    "news": _("News"),
    "search": _("Search"),
    "settings": _("Settings"),

    # Titles for pages
    "title_browse": _("Browse for Applications"),
    "title_queue": _("Queued Changes"),
    "title_installed": _("Installed Software"),
    "title_news": _("What's New?"),
    "title_search": _("Search"),
    "title_settings": _("Boutique Settings"),

    # Header Tooltips
    "tooltip_browse": _("View curated software or list applications by category"),
    "tooltip_queue": _("View pending software operations"),
    "tooltip_installed": _("View software currently installed on this system"),
    "tooltip_news": _("See the latest changes to the curated software picks"),
    "tooltip_search": _("Look for software available for your system"),
    "tooltip_settings": _("Change options related to Software Boutique"),
    "tooltip_back": _("Go back to the previous page"),

    # Footer
    "queue_ready": _("Ready."),
    "queue_ready_state": _("Installation progress will appear here."),
    "queue_downloading": _("Downloading XXX (1 of 2)..."), # XXX, 1, 2
    "queue_installing": _("Installing XXX (1 of 2)..."), # XXX, 1, 2
    "queue_progress": _("1 MB of 2 MB"), # 1, 2
    "queue_success": _("Finished."),
    "queue_success_state": _("1 installed, 2 updated, 3 removed."), # 1, 2, 3
    "queue_error": _("There were problems completing your request."), # XXX
    "queue_error_state": _("1 succeeded, 2 failed."), # 1, 2

    # Queue page
    "queue_list_title_processing": _("In Progress"),
    "queue_list_title_processed": _("Completed"),
    "queue_list_title_pending": _("Queued"),
    "queue_list_success_install": "", # Unused, 'Launch' button only.
    "queue_list_success_remove": _("Successfully removed"),
    "queue_list_failed_install": _("Failed to install"),
    "queue_list_failed_remove": _("Failed to remove"),
    "queue_list_clear": _("Clear List"),
    "queue_list_pending_install": _("Waiting for installation"),
    "queue_list_pending_remove": _("Waiting for removal"),
    "queue_list_empty": _("Progress for your software installations will appear here."),

    # General Actions
    "launch": _("Launch"),
    "view_details": _("View Details"),
    "info": _("Details"),
    "install": _("Install"),
    "reinstall": _("Reinstall"),
    "remove": _("Remove"),

    # Categories
    "accessibility": _("Universal Access"),
    "accessories": _("Accessories"),
    "development": _("Development"),
    "education": _("Education"),
    "games": _("Games"),
    "graphics": _("Graphics"),
    "internet": _("Internet"),
    "multimedia": _("Sound & Video"),
    "office": _("Office"),
    "server": _("Server"),
    "system": _("System Tools"),
    "themes": _("Themes"),

    # Settings
    "about": _("About"),
    "ver_software": _("Software Boutique 2.0"), # 2.0
    "ver_index": _("Index Revision 123"), # 123
    "last_updated": _("Last Updated: []"), # []
    "backend": _("Backends"),
    "backend_curated": _("Software Boutique Curated Index"),
    "backend_apt": _("PackageKit (Apt)"),
    "backend_snap": _("Snapd (Snapcraft)"),
    "backend_appstream": _("AppStream (Metadata)"),
    "backend_working": _("Enabled"),
    "backend_not_working": _("Unavailable"),
    "interface": _("Interface"),
    "hide_proprietary": _("Hide proprietary applications"),
    "hide_proprietary_help": _("Omit non-free software from being shown in Browse or Search."),
    "show_advanced": _("Show technical details for applications"),
    "show_advanced_help": _("Display additional details like sources and package names when viewing an application's details."),
    "precise_time": _("Prefer precise times"),
    "precise_time_help": _("Present exact date/time stamps instead of relative, for example '2 days ago'."),
    "compact_list": _("Compact view for application listings"),
    "compact_list_help": _("Show less detail so more applications appear on-screen at once."),
    "misc": _("Miscellaneous"),
    "show_intro": _("Show Introduction Screen"),

    # Browse
    "browse_welcome": _("What type of application are you looking for?"),
    "group_curated_title": _("Best in Class"),
    "group_curated_text": _("Tried and tested applications that integrate well with the MATE Desktop. Recommended by the Ubuntu MATE Team."),
    "group_snap_title": _("Snaps"),
    "group_snap_text": _("Applications that are sandboxed with tight security enhancements, in addition to being automatically updated."),
    "group_apt_title": _("Packages"),
    "group_apt_text": _("Available from the Ubuntu archives, or an external repository installed on your system."),

    # Application Details
    "no_screenshot": _("No screenshot available"),
    "version": _("Version"),
    "install_date": _("Installed"),
    "license": _("License"),
    "supported_arch": _("Supported Architectures"),
    "launch_cmd": _("Launch Command"),
    "tags": _("Tags"),
    "website": _("Website"),
    "support": _("Support"),
    "type": _("Type"),
    "source": _("Source"),
    "packages": _("Packages"),
    "snap_name": _("Snap Name"),
    "unknown": _("Unknown"),

    # App Types
    "apt": _("Debian Packaged Application (Apt)"),
    "snap": _("Universal Linux Package (Snapcraft)"),

    # App Sources
    "main": _("Canonical supported free and open source software"),
    "universe": _("Community-maintained free and open source software"),
    "restricted": _("Proprietary drivers for devices"),
    "multiverse": _("Software restricted by copyright or legal issues"),

    # Licenses
    "nonfree": _("Proprietary"),
    "free": _("Open Source or Free Software (FOSS)"),

    # End
    "": ""
}
