"""
Assembles the GTK window and adds WebKitGTK.
"""

import os
import signal
import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

## FIXME: Temporary workaround to ensure the snap works when proctitle is not available on the host.
try:
    import setproctitle
    proctitle_available = True
except ImportError:
    proctitle_available = False


class ApplicationWindow(object):
    """
    Main thread for building and interacting with the application.
    """
    def __init__(self, controller):
        self.webview = None
        self.controller = controller

    def build(self, webview_obj, data_source, title):
        width = 900
        height = 600

        # Prettier process name
        if proctitle_available:
            setproctitle.setproctitle("software-boutique")

        window = Gtk.Window()
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_wmclass("software-boutique", "software-boutique")
        window.set_title(title)
        window.set_icon_from_file(os.path.join(data_source, "view", "ui", "boutique.svg"))

        # http://askubuntu.com/questions/153549/how-to-detect-a-computers-physical-screen-size-in-gtk
        s = Gdk.Screen.get_default()
        if s.get_height() <= 600:
            window.set_size_request(768, 528)
        else:
            window.set_size_request(width, height)

        self.webkit = webview_obj

        # Load the starting page
        html_path = "file://" + os.path.abspath(os.path.join(data_source, "view", "boutique.html"))
        self.webkit.load_uri(html_path)

        # Create scrolled window (containing WebKit) to be part of a horz. pane
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.add(self.webkit)
        pane = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        pane.modify_bg(Gtk.StateType(0), Gdk.Color(128, 128, 128))

        # GTK Window -> Paned -> ScrolledWindow -> WebKit + Inspector (debugging)
        pane.add(sw)
        window.add(pane)

        # If debugging, open the inspector side-by-side
        if self.webkit.inspector:
            def dummy(webview):
                return True

            inspector = self.webkit.get_inspector()
            inspector.connect("open-window", dummy)
            inspector.show()
            inspector_webview = inspector.get_web_view()
            pane.add(inspector_webview)
            pane.set_position(1000)
            window.set_size_request(1920, 600)
            window.set_position(Gtk.WindowPosition.CENTER)

        window.connect("delete-event", self._close)
        window.show_all()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def _close(self, window, event):
        self.controller.shutdown()


def get_gtk3_theme_colours():
    """
    Returns an array of colours of the user's current theme.

    Expected array:
    Value           | GTK Equivalent
    ----------------|---------------------------
    page_bg           Page background
    page_fg           Page text
    header_bg         Title bar background (or bottom pixel)
    header_fg         Title bar text
    highlight         Menu highlight (e.g. selection colour or button dialog border)
    dark              Boolean to indicate the theme is dark.
    """

    # FIXME: Example only: KDE Breeze-dark theme
    return {
        "page_bg": "#232629",
        "page_fg": "#eff0f1",
        "header_bg": "#31363b",
        "header_fg": "#eff0f1",
        "highlight": "#3daee9",
        "dark": True
    }

