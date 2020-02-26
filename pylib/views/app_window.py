"""
Assembles the GTK window and adds WebKitGTK.
"""

import os
import signal
import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gdk, Gtk

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
    def __init__(self, app):
        self.webview = None
        self.app = app

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
        self.window = window

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def show_window(self):
        """
        Opens the GTK+ window after the runtime has initialised. This is to prevent
        the window flashing colours as the window and WebKit initialises.
        """
        GLib.idle_add(self._show_window)

    def _show_window(self):
        """
        Private function to actually show the window.
        """
        self.window.show_all()
        return GLib.SOURCE_REMOVE

    def _close(self, window, event):
        self.app.shutdown()


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
    # Code adapted from:
    # https://github.com/ubuntu-mate/mate-hud/blob/master/usr/lib/mate-hud/mate-hud#L175

    window = Gtk.Window()
    style_context = window.get_style_context()

    def _rgba_to_hex(color):
       """
       Return hexadecimal string for :class:`Gdk.RGBA` `color`.
       """
       return "#{0:02x}{1:02x}{2:02x}".format(
                                        int(color.red   * 255),
                                        int(color.green * 255),
                                        int(color.blue  * 255))

    def _get_color(style_context, preferred_color, fallback_color):
        color = _rgba_to_hex(style_context.lookup_color(preferred_color)[1])
        if color == "#000000":
            color = _rgba_to_hex(style_context.lookup_color(fallback_color)[1])
        return color

    bg_color = _get_color(style_context, "base_color", "theme_bg_color")
    bg_color_dark = _get_color(style_context, "dark_bg_color", "theme_bg_color")
    fg_color = _get_color(style_context, "fg_color", "theme_fg_color")
    fg_color_dark = _get_color(style_context, "dark_fg_color", "theme_fg_color")
    selected_bg_color = _rgba_to_hex(style_context.lookup_color("theme_selected_bg_color")[1])
    selected_fg_color = _rgba_to_hex(style_context.lookup_color("theme_selected_fg_color")[1])
    text_color = _rgba_to_hex(style_context.lookup_color("theme_text_color")[1])

    return {
        "page_bg": bg_color,
        "page_fg": fg_color,
        "header_bg": bg_color_dark,
        "header_fg": fg_color_dark,
        "highlight_bg": selected_bg_color,
        "highlight_fg": selected_fg_color,
        "dark": True
    }


def get_gtk_icon_path(icon_name, size, fallback_path):
    """
    Returns a path to a GTK icon.

    Params:
        name            GTK name, e.g. applications-accessories
        size            Requested size, e.g. 24
        fallback_path   Return this path if icon could not be found in current theme.
    """
    theme = Gtk.IconTheme.get_default()
    info = theme.lookup_icon(icon_name, size, 0)
    filename = None

    if info:
        filename = info.get_filename()

    if filename:
        return filename
    else:
        return fallback_path

