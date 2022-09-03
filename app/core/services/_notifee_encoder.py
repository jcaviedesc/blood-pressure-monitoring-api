import datetime
import json
import numbers
import re

import app.core.services._notifee_utils as _notifee_utils


class Notification():
    """A Notification type Notifee that can be sent via Firebase Cloud Messaging

    Contains payload information as well as recipient information. In particular, the notification must
    contain exactly one title and message to show using Notifee in the app https://notifee.app/react-native/docs/integrations/fcm#integrating-notifee

    Args:
        android: An instance of ``notifee.NotificationAndroid`` (optional).
        body: Body of the notification (optional).
        data: A dictionary of data fields (optional). All keys and values in the dictionary must be
            strings.
        id: A unique identifier for your notification (optional). Must be string.
        ios: An instance of ``notifee.NotificationIOS`` (optional). 
        subtitle: The notification subtitle, which appears on a new line below/next the title.
        title: The notification title which appears above the body text (optional).
    """

    def __init__(self, android={'channelId': 'default'}, body=None, data=None, id=None, ios=None, subtitle=None, title=None):
        self.android = android
        self.body = body
        self.data = data
        self.id = id
        self.ios = ios
        self.subtitle = subtitle
        self.title = title
        self.remote = True

    def __str__(self):
        return json.dumps(self, cls=NotificationEncoder, sort_keys=True)


class _Validators:
    """A collection of data validation utilities.

    Methods provided in this class raise ``ValueErrors`` if any validations fail.
    """

    @classmethod
    def check_string(cls, label, value, non_empty=False):
        """Checks if the given value is a string."""
        if value is None:
            return None
        if not isinstance(value, str):
            if non_empty:
                raise ValueError(
                    '{0} must be a non-empty string.'.format(label))
            raise ValueError('{0} must be a string.'.format(label))
        if non_empty and not value:
            raise ValueError('{0} must be a non-empty string.'.format(label))
        return value

    @classmethod
    def check_number(cls, label, value):
        if value is None:
            return None
        if not isinstance(value, numbers.Number):
            raise ValueError('{0} must be a number.'.format(label))
        return value

    @classmethod
    def check_string_dict(cls, label, value):
        """Checks if the given value is a dictionary comprised only of string keys and values."""
        if value is None or value == {}:
            return None
        if not isinstance(value, dict):
            raise ValueError('{0} must be a dictionary.'.format(label))
        non_str = [k for k in value if not isinstance(k, str)]
        if non_str:
            raise ValueError(
                '{0} must not contain non-string keys.'.format(label))
        non_str = [v for v in value.values() if not isinstance(v, str)]
        if non_str:
            raise ValueError(
                '{0} must not contain non-string values.'.format(label))
        return value

    @classmethod
    def check_string_list(cls, label, value):
        """Checks if the given value is a list comprised only of strings."""
        if value is None or value == []:
            return None
        if not isinstance(value, list):
            raise ValueError('{0} must be a list of strings.'.format(label))
        non_str = [k for k in value if not isinstance(k, str)]
        if non_str:
            raise ValueError(
                '{0} must not contain non-string values.'.format(label))
        return value

    @classmethod
    def check_number_list(cls, label, value):
        """Checks if the given value is a list comprised only of numbers."""
        if value is None or value == []:
            return None
        if not isinstance(value, list):
            raise ValueError('{0} must be a list of numbers.'.format(label))
        non_number = [k for k in value if not isinstance(k, numbers.Number)]
        if non_number:
            raise ValueError(
                '{0} must not contain non-number values.'.format(label))
        return value

    @classmethod
    def check_analytics_label(cls, label, value):
        """Checks if the given value is a valid analytics label."""
        value = _Validators.check_string(label, value)
        if value is not None and not re.match(r'^[a-zA-Z0-9-_.~%]{1,50}$', value):
            raise ValueError('Malformed {}.'.format(label))
        return value

    @classmethod
    def check_datetime(cls, label, value):
        """Checks if the given value is a datetime."""
        if value is None:
            return None
        if not isinstance(value, datetime.datetime):
            raise ValueError('{0} must be a datetime.'.format(label))
        return value


class NotificationEncoder(json.JSONEncoder):
    """A custom ``JSONEncoder`` implementation for serializing Notification instances into JSON."""

    @classmethod
    def remove_null_values(cls, dict_value):
        return {k: v for k, v in dict_value.items() if v not in [None, [], {}]}

    @classmethod
    def encode_android(cls, android):
        """Encodes an ``NotificationAndroid`` instance into JSON."""
        if android is None:
            return None
        if not isinstance(android, _notifee_utils.NotificationAndroid):
            raise ValueError(
                'Notification.android must be an instance of NotificationAndroid class.')
        result = {
            'channelId': _Validators.check_string(
                'AndroidConfig.channel_id', android.channelId),
            'largeIcon': _Validators.check_string(
                'AndroidConfig.largeIcon', android.largeIcon, non_empty=True),
            'color': _Validators.check_string('AndroidConfig.color', android.color, non_empty=True),
            'importance': android.importance,
            'actions': [cls.encode_android_action(android_action) for android_action in android.actions]
        }
        result = cls.remove_null_values(result)
        # priority = result.get('priority')
        # if priority and priority not in ('high', 'normal'):
        #     raise ValueError(
        #         'Notification.importance must be "high" or "normal".')
        return result

    @classmethod
    def encode_android_action(cls, action):
        """Encodes an ``NotificationAndroid.action`` instance into JSON."""
        if action is None:
            return None
        if not isinstance(action, _notifee_utils.AndroidAction):
            raise ValueError('NotificationAndroid.action must be an instance of '
                             'AndroidAction class.')
        result = {
            'icon': action.icon,
            'input': action.input, # TODO add class encoder https://notifee.app/react-native/reference/androidinput 
            'pressAction': action.pressAction, # TODO add class encoder https://notifee.app/react-native/reference/notificationpressaction
            'title': action.title
        }

        result = cls.remove_null_values(result)
        return result

    def default(self, o):  # pylint: disable=method-hidden
        if not isinstance(o, Notification):
            return json.JSONEncoder.default(self, o)
        result = {
            # add encoder
            'android': NotificationEncoder.encode_android(o.android),
            'body': _Validators.check_string('Notification.body', o.body, non_empty=True),
            'data': _Validators.check_string_dict('Notification.data', o.data),
            'id': _Validators.check_string('Notification.id', o.id, non_empty=True),
            # add encoder
            'ios': o.ios,
            'subtitle':  _Validators.check_string('Notification.subtitle', o.subtitle, non_empty=True),
            'title': _Validators.check_string('Notification.title', o.title, non_empty=True),
            'remote': o.remote
        }
        result = NotificationEncoder.remove_null_values(result)
        return result
