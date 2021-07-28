import os
from datetime import datetime, timedelta
from typing import Dict

import pytz
from dialogflow_fulfillment import WebhookClient, Text
from fastapi import FastAPI, BackgroundTasks

from modules.conversation_flows.trigger_per_day import TRIGGER_PER_DAY, TRIGGER_PER_DAY_FULFILLMENT
from modules.flow.answer import Answer
from modules.flow.answer_collection import AnswerCollection
from modules.flow.answers_controller import AnswersController
from modules.flow.finished import FinishedFlow
from modules.flow.flow_collection import FlowCollection
from modules.flow.sent_triggers import SentTriggers
from modules.messenger_api.api import MessengerAPI
from modules.user.model import User

app = FastAPI()


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


def handler(agent: WebhookClient) -> None:
    """Handle the webhook request.."""
    pass


@app.post('/webhook')
async def post_test(json_data: Dict):
    facebook_payload = json_data['originalDetectIntentRequest']
    psid = facebook_payload['payload']['data']['sender']['id']

    user = User(psid)

    user_existing_data = user.get()

    if not user_existing_data:
        user.save()

    query_result = json_data['queryResult']

    # Check if from persistent menu
    from_persistent_menu = query_result['parameters'].get('from_persistent_menu')

    if from_persistent_menu:
        finished_flow = FinishedFlow(psid, '')
        finished_flow_dict = finished_flow.get()
        agent = WebhookClient(json_data)
        agent.handle_request(handler)

        if not finished_flow_dict:
            messages = TRIGGER_PER_DAY_FULFILLMENT['day1']

            for message in messages:
                agent.add(message)

            return agent.response

        days_finished = finished_flow_dict.get('days')

        timezone = pytz.timezone('Asia/Manila')
        last_finished = finished_flow_dict.get('updated_on_timestamp')
        last_finished = last_finished.astimezone(timezone)
        utc_now = pytz.utc.localize(datetime.utcnow())
        current_time = utc_now.astimezone(timezone)

        if last_finished.day == current_time.day:
            default_text = Text('Ops, wait ka lang muna! Patience is da 🔑 Balik ka bukas para sa next story. 🤪')
            agent.add(default_text)

            return agent.response

        days_finished = list(days_finished.keys())
        days_finished = [int(day) for day in days_finished]
        max_days_finished = max(days_finished)
        next_day = max_days_finished + 1

        # TODO: Add images on day 6 and day 7
        try:
            messages = TRIGGER_PER_DAY_FULFILLMENT[f'day{next_day}']
        except KeyError:
            print(f'day{next_day} not supported')

            return json_data

        default_text = Text('Ayernnn \'yan ang gusto ko sayo e! 😉 Heto, tuloy na natin ang drama:')
        agent.add(default_text)

        for message in messages:
            agent.add(message)

        return agent.response

    # Checking if dialog is in dialogs for end of day

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


@app.get('/message/cron')
async def cron_send_messages(background_tasks: BackgroundTasks):
    answer_collection = FlowCollection()
    users_finished_flow = answer_collection.get_all_users_finished_flow()
    access_token = os.environ.get('ACCESS_TOKEN')
    messenger_api = MessengerAPI(access_token)

    if not access_token:
        raise ValueError('No access token!')

    # Kurl PSID = 4101076556625537

    def send(__user_finished_flow):
        user_finished_flow_dict = __user_finished_flow.to_dict()
        timezone = pytz.timezone('Asia/Manila')

        last_user_message_timestamp = user_finished_flow_dict['updated_on_timestamp']
        last_user_message_timestamp = last_user_message_timestamp.astimezone(timezone)
        last_user_message_timestamp_plus_23_hours = last_user_message_timestamp + timedelta(hours=23)

        utc_now = pytz.utc.localize(datetime.utcnow())
        current_time = utc_now.astimezone(timezone)

        last_user_message_timestamp_plus_23_hours = last_user_message_timestamp_plus_23_hours.replace(
            minute=0,
            second=0,
            microsecond=0
        )
        current_time = current_time.replace(
            minute=0,
            second=0,
            microsecond=0
        )

        if last_user_message_timestamp_plus_23_hours != current_time:
            return

        days_finished = user_finished_flow_dict['days']
        days_finished = list(days_finished.keys())
        days_finished = [int(day) for day in days_finished]
        max_days_finished = max(days_finished)
        next_day = max_days_finished + 1

        psid = user_finished_flow_dict['psid']
        sent_triggers = SentTriggers(psid, str(next_day), [])
        sent_triggers_exist = sent_triggers.get()

        if sent_triggers_exist and sent_triggers_exist.get('days').get(str(next_day)):
            return

        try:
            messages = TRIGGER_PER_DAY[f'day{next_day}']
        except KeyError:
            print(f'day{next_day} not supported')

            return

        print('Sending message to', psid, 'Day', next_day)

        results = messenger_api.send_messages(messages, psid)

        has_message_ids = all([res.get('message_id')] for res in results)

        if has_message_ids:
            sent_triggers = SentTriggers(psid, str(next_day), results)
            sent_triggers.save()

    for user_finished_flow in users_finished_flow:
        background_tasks.add_task(send, user_finished_flow)

    return 'OK'


@app.get('/answers/analytics')
async def get_answers_analytics():
    answer_collection = AnswerCollection()

    all_answers = answer_collection.get_all_user_answers()

    grouped_answers_by_psid = AnswersController.group_answers_by_psid(all_answers)
    grouped_by_day = AnswersController.grouped_answers_by_day(grouped_answers_by_psid)
    final_data = AnswersController.get_date_started_ended_per_day_per_psid(grouped_by_day)

    AnswersController.generate_excel(final_data)

    return final_data
