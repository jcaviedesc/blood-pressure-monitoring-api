
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


class AndroidLaunchActivityFlag(IntEnum):
    """
    * See [FLAG_ACTIVITY_NO_HISTORY](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_NO_HISTORY) on the official Android documentation for more information.
    """
    NO_HISTORY = 0,
    """
     * See [FLAG_ACTIVITY_SINGLE_TOP](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_SINGLE_TOP) on the official Android documentation for more information.
    """
    SINGLE_TOP = 1,
    """
     * See [FLAG_ACTIVITY_NEW_TASK](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_NEW_TASK) on the official Android documentation for more information.
    """
    NEW_TASK = 2,
    """
     * See [FLAG_ACTIVITY_MULTIPLE_TASK](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_MULTIPLE_TASK) on the official Android documentation for more information.
     """
    MULTIPLE_TASK = 3,
    """
     * See [FLAG_ACTIVITY_CLEAR_TOP](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_CLEAR_TOP) on the official Android documentation for more information.
    """
    CLEAR_TOP = 4,
    """
     * See [FLAG_ACTIVITY_FORWARD_RESULT](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_FORWARD_RESULT) on the official Android documentation for more information.
    """
    FORWARD_RESULT = 5,
    """
     * See [FLAG_ACTIVITY_PREVIOUS_IS_TOP](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_PREVIOUS_IS_TOP) on the official Android documentation for more information.
    """
    PREVIOUS_IS_TOP = 6,
    """
     * See [FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS) on the official Android documentation for more information.
    """
    EXCLUDE_FROM_RECENTS = 7,
    """
     * See [FLAG_ACTIVITY_BROUGHT_TO_FRONT](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_BROUGHT_TO_FRONT) on the official Android documentation for more information.
    """
    BROUGHT_TO_FRONT = 8,
    """
     * See [FLAG_ACTIVITY_RESET_TASK_IF_NEEDED](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_RESET_TASK_IF_NEEDED) on the official Android documentation for more information.
    """
    RESET_TASK_IF_NEEDED = 9,
    """
     * See [FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY) on the official Android documentation for more information.
    """
    LAUNCHED_FROM_HISTORY = 10,
    """
     * See [FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET) on the official Android documentation for more information.
    """
    CLEAR_WHEN_TASK_RESET = 11,
    """
     * See [FLAG_ACTIVITY_NEW_DOCUMENT](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_NEW_DOCUMENT) on the official Android documentation for more information.
    """
    NEW_DOCUMENT = 12,
    """
     * See [FLAG_ACTIVITY_NO_USER_ACTION](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_NO_USER_ACTION) on the official Android documentation for more information.
    """
    NO_USER_ACTION = 13,
    """
     * See [FLAG_ACTIVITY_REORDER_TO_FRONT](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_REORDER_TO_FRONT) on the official Android documentation for more information.
    """
    REORDER_TO_FRONT = 14,
    """
     * See [FLAG_ACTIVITY_NO_ANIMATION](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_NO_ANIMATION) on the official Android documentation for more information.
    """
    NO_ANIMATION = 15,
    """
     * See [FLAG_ACTIVITY_CLEAR_TASK](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_CLEAR_TASK) on the official Android documentation for more information.
    """
    CLEAR_TASK = 16,
    """
     * See [FLAG_ACTIVITY_TASK_ON_HOME](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_TASK_ON_HOME) on the official Android documentation for more information.
    """
    TASK_ON_HOME = 17,
    """
     * See [FLAG_ACTIVITY_RETAIN_IN_RECENTS](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_RETAIN_IN_RECENTS) on the official Android documentation for more information.
    """
    RETAIN_IN_RECENTS = 18,
    """
     * See [FLAG_ACTIVITY_LAUNCH_ADJACENT](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_LAUNCH_ADJACENT) on the official Android documentation for more information.
    """
    LAUNCH_ADJACENT = 19,
    """
     * See [FLAG_ACTIVITY_MATCH_EXTERNAL](https://developer.android.com/reference/android/content/Intent.html#FLAG_ACTIVITY_MATCH_EXTERNAL) on the official Android documentation for more information.
    """
    MATCH_EXTERNAL = 20


class NotificationPressAction:
    """The interface used to describe a press action for a notification.

    There are various ways a user can interact with a notification, the most common being pressing the notification,
    pressing an action or providing text input.This interface defines what happens when a user performs such interaction.
    On Android; when provided to a notification action, the action will only open you application if a launchActivity
    and/or a mainComponent is provided.

    Args:
        id: The unique ID for the action. The id property is used to differentiate between user press actions.
            When listening to notification events, the ID can be read from the event.detail.pressAction object.
        launch_activity: The custom Android Activity to launch on a press action (optional)[android only].
        launch_activity_flags: List of instances of ``notifee.AndroidLaunchActivityFlag`` (optional)[android only].
            Custom flags that are added to the Android Intent that launches your Activity.
        main_component: A custom registered React component to launch on press action (optional)[android only].
    """

    def __init__(self, id: str, launch_activity: Optional[str] = None, launch_activity_flags: Optional[list[AndroidLaunchActivityFlag]] = None, main_component: Optional[str] = None):
        self.id = id
        self.launch_activity = launch_activity
        self.launch_activity_flags = launch_activity_flags
        self.main_component = main_component


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
        press_action: An instance of ``nofifee.NotificationPressAction`` describing what happens when an action completes.
            Note; unlike the pressAction in the notification body, an action does not need to open the application
            and can perform background tasks. See the [AndroidPressAction](https://notifee.app/react-native/reference/androidpressaction)
            reference or Quick Actions documentation to learn more.
        title: The title of the action, e.g. "Reply", "Mark as read" etc.
    """

    def __init__(self, title, press_action: NotificationPressAction, icon: Optional[str] = None, input=None) -> None:
        self.icon = icon
        self.input = input
        self.press_action = press_action
        self.title = title


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
        actions: An list of ``AndroidAction`` class (optional). ver https://notifee.app/react-native/reference/androidaction
    """
    # TODO cambiar a Optional y a camel_case

    def __init__(
        self,
        channel_id: Optional[str] = 'default',
        large_icon: Optional[str] = None,
        color: Optional[str] = None,
        importance: Optional[AndroidImportance] = AndroidImportance.DEFAULT,
        actions: Optional[list[AndroidAction]] = None,
        small_icon: Optional[str] = None
    ) -> None:
        self.channelId = channel_id
        self.largeIcon = large_icon
        self.color = color
        self.importance = importance
        self.actions = actions
        self.smallIcon = small_icon
