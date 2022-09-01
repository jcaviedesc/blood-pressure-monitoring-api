from typing import Dict, TypedDict
from firebase_admin import messaging
import json

class AndroidNotifee(TypedDict):
    channelId: str  # optional, defaults to 'default'.
    smallIcon: str  # optional, defaults to 'ic_launcher'.
    # actions is needed if you want the notification to open the app when pressed
    """
    {
        title: 'Mark as Read',
        pressAction: {
            id: 'read',
        }
    }
    """
    actions: list[dict]


class NotifyPayload(TypedDict, total=False):
    title: str
    body: str
    android: AndroidNotifee


def send_message(*, registration_token: str, payload: NotifyPayload) -> str:

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'notifee': json.dumps(payload, separators=(',', ':'))
        },
        token=registration_token)
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    return response
