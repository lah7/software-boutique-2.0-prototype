"""
Assembles the 'view' aspect of the application, which consists of a GTK window,
WebKitGTK and sending notifications.
"""

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gdk, Gtk, GLib, WebKit2


class ApplicationWindow(object):
    """
    Main thread for building and interacting with the application.
    """
    def __init__(self):
        pass

    def build(self):
        title = _("Software Boutique")
        width = 900
        height = 600
        html_file = "boutique.html"

        # Nice process name
        if proctitle_available:
            setproctitle.setproctitle("software-boutique")

        w = Gtk.Window()
        w.set_position(Gtk.WindowPosition.CENTER)
        w.set_wmclass("software-boutique", "software-boutique")
        w.set_title(title)
        w.set_icon_from_file(os.path.join(data_source, "img", "boutique-icon.svg"))

        # http://askubuntu.com/questions/153549/how-to-detect-a-computers-physical-screen-size-in-gtk
        s = Gdk.Screen.get_default()
        if s.get_height() <= 600:
            w.set_size_request(768, 528)
        else:
            w.set_size_request(width, height)

        webview = WebView()

        # Load the starting page
        html_path = "file://" + os.path.abspath(os.path.join(data_source, html_file))
        webview.load_uri(html_path)

        # Build scrolled window widget and add our appview container
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.add(webview)

        # Build an autoexpanding box and add our scrolled window
        b = Gtk.VBox(homogeneous=False, spacing=0)
        b.pack_start(sw, expand=True, fill=True, padding=0)

        # Add the box to the parent window
        w.add(b)
        w.connect("delete-event", self._close)
        w.show_all()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def _close(self, window, event):
        shutdown()


class WebView(WebKit2.WebView):
    """
    Setting up the program's web browser and processing WebKit operations
    """
    def __init__(self, dbg):
        self.webkit = WebKit2
        self.webkit.WebView.__init__(self)
        self.dbg = dbg

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

    def on_finish_load(self, view, frame):
        """
        Callback: On page change. There is only boutique.html.
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
        """
        Callback: Returns True, as the context menu is disabled.
        """
        return True

    def make_html_safe(string):
        """
        Returns a string that is HTML safe that won't cause interference.
        For example, when used in JavaScript attributes.
        """
        return string.replace("'", "&#145;")


class Notification():
    """
    Enables sending of desktop notifications.
    """
    def send():
        pass


    def send_desktop_notification(self, app_obj, operation, successful):
        """
        Shows a notification on the user's desktop.

        app_obj     obj     ApplicationData() object
        operation   str     Operation name
                              - "install"
                              - "remove"
        successful  bln     True/False
        """
        def notify_send(title, subtitle):
            title = title.replace("{0}", app_obj.name)
            subtitle = subtitle.replace("{0}", app_obj.name)
            icon_path = os.path.join(data_source, app_obj.icon_path)
            try:
                Notify.init(title)
                notification = Notify.Notification.new(title, subtitle, icon_path)
                notification.show()
            except Exception as e:
                dbg.stdout("Could not send notification: " + str(e), dbg.error, 1)

        if operation == "install":
            if successful:
                notify_send(_("{0} successfully installed"), _("This application is ready to use."))
            else:
                notify_send(_("{0} failed to install"), _("There was a problem installing this application."))

        elif operation == "remove":
            if successful:
                notify_send(_("{0} removed"), _("This application has been uninstalled."))
            else:
                notify_send(_("{0} failed to remove"), _("There was a problem removing this application."))
