"""
Handles the setting up and processing of data sent from WebView (WebKitGTK)
"""

import gi
gi.require_version("WebKit2", "4.0")
from gi.repository import GLib, WebKit2

class WebView(WebKit2.WebView):
    """
    Setting up the program's web browser and processing WebKit operations
    """
    def __init__(self, dbg, app):
        """__init__

        :param dbg: Dbg instance
        :param app: SoftwareBoutique instance
        """
        self.webkit = WebKit2
        self.webkit.WebView.__init__(self)
        self.app = app
        self.inspector = False

        # Python <--> WebView communication
        self.connect("notify::title", self._recv_data)
        self.connect("context-menu", self._on_context_menu)
        self.connect("load-changed", self.on_finish_load)

        # Enable keyboard navigation
        self.get_settings().set_enable_spatial_navigation(True)
        self.get_settings().set_enable_caret_browsing(True)

        # Show console messages in stdout if we're debugging.
        if dbg.verbose_level >= 1:
            self.get_settings().set_enable_write_console_messages_to_stdout(True)

        # Enable web inspector for debugging
        if dbg.verbose_level == 2:
            self.get_settings().set_property("enable-developer-extras", True)
            self.inspector = True

    def run_js(self, function):
        """
        Runs a JavaScript function on the page, regardless of which thread it is called from.
        GTK+ operations must be performed on the same thread to prevent crashes.
        """
        GLib.idle_add(self._run_js, function)

    def _run_js(self, function):
        """
        Runs a JavaScript function on the page when invoked from run_js()
        """
        self.run_javascript(function)
        return GLib.SOURCE_REMOVE

    def on_finish_load(self, view, frame):
        """
        Callback: On page change.
        """
        if not self.is_loading():
            self.app.start()

    def _recv_data(self, view, frame):
        """
        Callback: Used to recieve data from view (JS) to controller (Python)
        """
        title = self.get_title()
        if title not in ["null", "", None]:
            self.app.incoming_request(title)
            # Reset title afterwards so another request can be sent again.
            self.run_js("document.title = ''")

    def send_data(self, function, data):
        """
        Used to communicate from controller (Python) to view (JS).

        :parm function: Name of the JavaScript function to execute, passing this data.
        :parm data: String containing data stream.
        """
        self.run_js("{0}({1})".format(function, str(data)))

    def _on_context_menu(self, webview, menu, event, htr, user_data=None):
        """
        Context menu is disabled as the application masks it's a WebKit browser.
        """
        return True
