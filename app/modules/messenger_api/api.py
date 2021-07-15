from typing import Dict, List

from requests import Session, HTTPError

from modules.messenger_api.messenger_component import MessengerComponent
from modules.messenger_api.quick_replies import MessengerQuickReplies


class MessengerAPI:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = Session()
        self.graph_fb_url = 'https://graph.facebook.com/v11.0/me/messages'

    def send_message(self, message: MessengerComponent, messaging_type: str, recipient_id: str):
        data = {
            'recipient': {
                'id': recipient_id
            },
            'messaging_type': messaging_type,
            'message': message.to_dict()
        }
        result = self.session.post(
            self.graph_fb_url,
            params={'access_token': self.access_token},
            json=data
        )

        return result.json()

    def send_messages(self, messages: List[MessengerComponent], recipient_id: str) -> List[Dict]:
        results = []

        for message in messages:
            # TODO: MESSAGE_TAG
            if isinstance(message, MessengerQuickReplies):
                messaging_type = 'RESPONSE'
            else:
                messaging_type = 'UPDATE'

            result = self.send_message(message, messaging_type, recipient_id)
            results.append(result)

        return results
