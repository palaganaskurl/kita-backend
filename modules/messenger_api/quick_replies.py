from typing import List, Dict

from app.modules.messenger_api.messenger_component import MessengerComponent


class MessengerQuickReplies(MessengerComponent):
    def __init__(self, text: str, quick_replies: List[Dict]):
        self.text = text
        self.quick_replies = quick_replies

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'quick_replies': self.quick_replies
        }
