
"""Types and utilities used by the messaging (Notifee) module."""
from enum import IntEnum
from typing import Optional


class AndroidImportance(IntEnum):
    """
     * The default importance applied to a channel/notification.
     *
     * The application small icon will show in the device statusbar. When the user pulls down the
     * notification shade, the notification will show in it's expanded state (if applicable).
    """
    DEFAULT = 3,
    """
     * The highest importance level applied to a channel/notification.
     *
     * The notifications will appear on-top of applications, allowing direct interaction without pulling
     * down the notification shade. This level should only be used for urgent notifications, such as
     * incoming phone calls, messages etc, which require immediate attention.
    """
    HIGH = 4,
    """
     * A low importance level applied to a channel/notification.
     *
     * On Android, the application small icon will show in the device statusbar, however the notification will not alert
     * the user (no sound or vibration). The notification will show in it's expanded state when the
     * notification shade is pulled down.
     *
     * On iOS, the notification will not display to the user or alert them. It will still be visible on the devices
     * notification center.
    """
    LOW = 2,
    """
     * The minimum importance level applied to a channel/notification.
     *
     * The application small icon will not show up in the statusbar, or alert the user. The notification
     * will be in a collapsed state in the notification shade and placed at the bottom of the list.
     *
     * This level should be used when the notification requires no immediate attention. An example of this
     * importance level is the Google app providing weather updates and only being visible when the
     * user pulls the notification shade down,
    """
    MIN = 1,
    """
     * The notification will not be shown. This has the same effect as the user disabling notifications
     * in the application settings.
    """
    NONE = 0


class NotificationAndroid:
    """Android specific notification options. See the NotificationAndroid interface
    for more information and default options which are applied to a notification.

    Args:
        channel_id: Specifies the AndroidChannel which the notification will be delivered on (optional).
        large_icon: A local file path using the 'require()' method or a remote http to the picture to display (optional).
        color: Set an custom accent color for the notification. If not provided, the default notification system color will be used.
            View the ``Color`` documentation for more information.  https://notifee.app/react-native/docs/android/appearance#color
        importance: Set a notification importance for devices without channel support (optional). Must be one of ``default``, ``min``, ``low``,
            ``high``, ``max`` or ``normal``.
        actions: An list of ``AndroidAction`` class. ver https://notifee.app/react-native/reference/androidaction
    """

    def __init__(self, channel_id: str | None = 'default', large_icon: str | None = None, color: str | None = None, importance: AndroidImportance | None = AndroidImportance.DEFAULT, actions=[]) -> None:
        self.channelId = channel_id
        self.largeIcon = large_icon
        self.color = color
        self.importance = importance
        self.actions = actions


class AndroidAction:
    """The interface used to describe a notification quick action for Android.
    
    Notification actions allow users to interact with notifications, allowing you to handle events
    within your application. When an action completes (e.g. pressing an action, or filling out an input box)
    an event is sent.

    Args:
        icon: An remote http or local icon path representing the action (optional). Newer devices may not show the icon.
            Recommended icon size is 24x24 px.
        input: If provided, the action accepts user input (optional). If True, the user will be able to provide free
            text input when the action is pressed. This property can be further configured for advanced inputs.
            Must be ``True`` or ``nofifee.AndroidInput``
        pressAction: The press action interface describing what happens when an action completes.
            Note; unlike the pressAction in the notification body, an action does not need to open the application
            and can perform background tasks. See the [AndroidPressAction](https://notifee.app/react-native/reference/androidpressaction)
            reference or Quick Actions documentation to learn more.
        title: The title of the action, e.g. "Reply", "Mark as read" etc.
    """
    def __init__(self, title, press_action, icon: Optional[str] = None, input=None) -> None:
        self.icon = icon
        self.input = input
        self.pressAction = press_action
        self.title = title