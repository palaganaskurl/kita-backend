from modules.messenger_api.quick_replies import MessengerQuickReplies
from modules.messenger_api.text import MessengerTextMessage

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
    ],
    'day4': [
        MessengerTextMessage(text='Kamusta naman diyan?'),
        MessengerTextMessage(text='So eto...Pinili ni Tia K. yung 15K na apartment.'),
        MessengerQuickReplies(
            text='"Yung rent difference naman ay parang like I\'m paying for a better quality of life." 💁‍♀️',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': 'Tru thoooo 👏',
                    'payload': 'Tru thoooo 👏'
                },
                {
                    'content_type': 'text',
                    'title': 'Haist di nakikinig',
                    'payload': 'Haist di nakikinig'
                }
            ]
        )
    ],
    'day5': [
        MessengerTextMessage(text='Heeelllooo, may update ulet ako kay Tia K.!!! 👋'),
        MessengerTextMessage(text='Fighter talaga yung babae na \'to. 💪'),
        MessengerQuickReplies(
            text='"OK," ang sinabi niya, "I have to pick myself up and make desisyon about what to do sa susunod."',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': 'GO GURL! 👏',
                    'payload': 'GO GURL! 👏'
                },
                {
                    'content_type': 'text',
                    'title': '🤡',
                    'payload': '🤡'
                }
            ]
        )
    ],
    'day6': [
        MessengerTextMessage(text='Hai mamser!!! What can I serve you today? 😗🍵🫖🧋'),
        MessengerTextMessage(text='FAST FORWARD! Zoom zoom zoom beep beep. ⏭\nAfter 3 months, mukhang wala pang nakita ng trabaho si Tia K. habang lumiliit lang yung savings niya. 😔'),
        MessengerQuickReplies(
            text='So nag-decide siya na lumipat ulit sa bahay ng mga magulang niya.',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': '3 months na agad???',
                    'payload': '3 months na agad???'
                },
                {
                    'content_type': 'text',
                    'title': 'Noooo 😭',
                    'payload': 'Noooo 😭'
                },
                {
                    'content_type': 'text',
                    'title': 'Tama lang 🤷‍♀️',
                    'payload': 'Tama lang 🤷‍♀️'
                }
            ]
        )
    ],
    'day7': [
        MessengerTextMessage(text='Bilib mo, isang linggo na kami nagkukuwentuhan! 😗✌️ Saya, noh? 🤪'),
        MessengerQuickReplies(
            text='Wala akong news today, may tanong lang... May idea ka pa kung paano pa kumita si Tia K.? 👀 Para sa she can pursue her passion and be independent, diba!!! 👏👏👏',
            quick_replies=[
                {
                    'content_type': 'text',
                    'title': 'Yisss, may idea ako!',
                    'payload': 'Yisss, may idea ako!'
                },
                {
                    'content_type': 'text',
                    'title': 'Pass muna 😅😂',
                    'payload': 'Pass muna 😅😂'
                }
            ]
        )
    ]
}
