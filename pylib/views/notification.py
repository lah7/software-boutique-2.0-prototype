"""
Handles the desktop popup notifications.
"""

import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify


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
