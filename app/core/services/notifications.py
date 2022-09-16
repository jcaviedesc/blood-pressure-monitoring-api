from firebase_admin import messaging
from app.core.services import _notifee_encoder
from app.core.services import _notifee_utils

__all__ = [
    'Notification',
    'AndroidImportance',
    'NotificationAndroid',
    'AndroidAction',
    'NotificationPressAction',

    'send'
]

Notification = _notifee_encoder.Notification
AndroidImportance = _notifee_utils.AndroidImportance
NotificationAndroid = _notifee_utils.NotificationAndroid
AndroidAction = _notifee_utils.AndroidAction
NotificationPressAction = _notifee_utils.NotificationPressAction


def send(*, notifee_message, registration_token: str) -> str:
    """Sends the given notifee_message via Firebase Cloud Messaging (FCM).

    Args:
        notifee_message: An instance of ``notifee.Notification``.
        registration_token: The registration token of the device to which the message should be sent (optional).

    Returns:
        string: A message ID string that uniquely identifies the sent message.

    Raises:
        FirebaseError: If an error occurs while sending the message to the FCM service.
        ValueError: If the input arguments are invalid.
    """
    notification = messaging.Message(
        data={
            'notifee': str(notifee_message)
        },
        token=registration_token)
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(notification)
    # Response is a message ID string.
    return response
