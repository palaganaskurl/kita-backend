from typing import Dict

from app.modules.messenger_api.messenger_component import MessengerComponent


class MessengerTextMessage(MessengerComponent):
    def __init__(self, text):
        self.text = text

    def to_dict(self) -> Dict:
        return {'text': self.text}
