from pylib.common import Debugging

from gi.repository import GLib, WebKit2

class WebView(WebKit2.WebView):
    """
    Setting up the program's web browser and processing WebKit operations
    """
    def __init__(self, software_boutique_app):
        """__init__

        :param software_boutique_app: SoftwareBoutique instance
        """
        self.dbg = Debugging()
        self.webkit = WebKit2
        self.webkit.WebView.__init__(self)
        self.software_boutique_app = software_boutique_app

        # Python <--> WebView communication
        self.connect("notify::title", self._on_title_change)
        self.connect("context-menu", self._on_context_menu)
        self.connect("load-changed", self.on_finish_load)

        # Enable keyboard navigation
        self.get_settings().set_enable_spatial_navigation(True)
        self.get_settings().set_enable_caret_browsing(True)

        # Show console messages in stdout if we're debugging.
        if self.dbg.verbose_level >= 2:
            self.get_settings().set_enable_write_console_messages_to_stdout(True)


        # Enable web inspector for debugging
        if self.dbg.verbose_level == 3:
            self.get_settings().set_property("enable-developer-extras", True)
            inspector = self.get_inspector()
            inspector.show()

        self.dbg.stdout("Finished webkit2 initalisation.", self.dbg.success, 1)

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

    def update_page(self, element, function, parm1=None, parm2=None):
        """
        Runs a JavaScript jQuery function on the page, ensuring correctly parsed quotes.
        """
        if parm1 and parm2:
            self.run_js('$("' + element + '").' + function + "('" + parm1.replace("'", '\\\'') + "', '" + parm2.replace("'", '\\\'') + "')")
        if parm1:
            self.run_js('$("' + element + '").' + function + "('" + parm1.replace("'", '\\\'') + "')")
        else:
            self.run_js('$("' + element + '").' + function + '()')

    def on_finish_load(self, view, frame):
        """
        Callback: On page change.
        """
        if not self.is_loading():
            self.dbg.stdout("Finished page initalisation.", self.dbg.success, 1)

    def _on_title_change(self, view, frame):
        """
        Callback: When page title is changed, used for communicating with Python.
        """
        title = self.get_title()
        if title != "null" and title != "" and title != None:
            self.dbg.stdout("Command: '{0}'".format(title), self.dbg.debug, 2)
            self.software_boutique_app.process_command(title)

    def _on_context_menu(self, webview, menu, event, htr, user_data=None):
        # Disable context menu.
        return True
