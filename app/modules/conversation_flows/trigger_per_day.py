from app.modules.messenger_api.quick_replies import MessengerQuickReplies
from app.modules.messenger_api.text import MessengerTextMessage

TRIGGER_PER_DAY = {
    'day2': [
        MessengerTextMessage(text='O sabi ko babalik ako, diba?? 🤪'),
        MessengerQuickReplies(
            text='Mahilig ka sa chika, noh? Unless... miss mo lang aqu 🥺👉👈',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': '🤫 🤫 🤫',
                    'payload': '🤫 🤫 🤫'
                },
                {
                    'content_type': 'text',
                    'title': 'SHHH so anyare??',
                    'payload': 'SHHH so anyare??'
                },
                {
                    'content_type': 'text',
                    'title': 'Ang feeler mo 😂',
                    'payload': 'Ang feeler mo 😂'
                }
            ]
        )
    ],
    'day3': [
        MessengerQuickReplies(
            text='Goooood dayyy po, mamser! 💁‍♀️G ka na ba for today\'s chika',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': 'Gggg anuna na mars',
                    'payload': 'Gggg anuna na mars'
                },
                {
                    'content_type': 'text',
                    'title': '\'Lang tulog dahil d2',
                    'payload': '\'Lang tulog dahil d2'
                }
            ]
        )
    ]
}
