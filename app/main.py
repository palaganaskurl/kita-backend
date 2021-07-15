import os
from datetime import datetime, timedelta
from typing import Dict

import pytz
from fastapi import FastAPI

from app.modules.conversation_flows.trigger_per_day import TRIGGER_PER_DAY
from app.modules.flow.answer import Answer
from app.modules.flow.answer_collection import FlowCollection
from app.modules import FinishedFlow
from app.modules.flow.sent_triggers import SentTriggers
from app.modules import MessengerAPI
from app.modules import User

app = FastAPI()


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


@app.post('/webhook')
async def post_test(json_data: Dict):
    facebook_payload = json_data['originalDetectIntentRequest']
    psid = facebook_payload['payload']['data']['sender']['id']

    user = User(psid)

    user_existing_data = user.get()

    if not user_existing_data:
        user.save()

    # Checking if dialog is in dialogs for end of day
    query_result = json_data['queryResult']
    end_of_day = query_result['parameters'].get('end_of_day')

    if end_of_day:
        finished_flow = FinishedFlow(psid, end_of_day)
        finished_flow.save()

    # Checking if is an answer to a question
    question = query_result['parameters'].get('question')

    if question:
        user_answer = facebook_payload['payload']['data']['message']['text']
        answer_model = Answer(psid, question, user_answer)
        answer_model.save()

    return json_data


@app.post('/message/cron')
async def cron_send_messages():
    answer_collection = FlowCollection()
    users_finished_flow = answer_collection.get_all_users_finished_flow()
    access_token = os.environ.get('ACCESS_TOKEN')
    messenger_api = MessengerAPI(access_token)

    if not access_token:
        raise ValueError('No access token!')

    for user_finished_flow in users_finished_flow:
        user_finished_flow_dict = user_finished_flow.to_dict()

        last_user_message_timestamp = user_finished_flow_dict['updated_on_timestamp']

        timezone = pytz.timezone('Asia/Manila')
        utc_now = pytz.utc.localize(datetime.utcnow())
        current_time = utc_now.astimezone(timezone)
        current_time_plus_24_hours = current_time + timedelta(hours=23, minutes=50)

        if last_user_message_timestamp > current_time_plus_24_hours:
            continue

        days_finished = user_finished_flow_dict['days']
        days_finished = list(days_finished.keys())
        days_finished = [int(day) for day in days_finished]
        max_days_finished = max(days_finished)
        next_day = max_days_finished + 1

        psid = user_finished_flow_dict['psid']
        sent_triggers = SentTriggers(psid, str(next_day), [])
        sent_triggers_exist = sent_triggers.get()

        if sent_triggers_exist and sent_triggers_exist.get('days').get(str(next_day)):
            continue

        messages = TRIGGER_PER_DAY[f'day{next_day}']

        results = messenger_api.send_messages(messages, psid)

        sent_triggers = SentTriggers(psid, str(next_day), results)
        sent_triggers.save()

    return 'OK'
