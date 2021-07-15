from typing import Union, Dict, List

from modules.base.model import Model


class SentTriggers(Model):
    def __init__(self, psid: str, day: str, message_results: Union[List, Dict]):
        super().__init__()

        self.id = 'SentTriggers'
        self.psid = psid
        self.days = {
            day: {
                'sent': True,
                'message_results': message_results
            }
        }

    def __get(self):
        return self._client \
            .collection(f'Users/{self.psid}/Flow') \
            .document(self.id) \
            .get() \
            .to_dict()

    def save(self) -> bool:
        existing_data = self.__get()

        if not existing_data:
            self._client \
                .collection(f'Users/{self.psid}/Flow') \
                .add(self.model_properties, document_id=self.id)

            return True

        existing_data['days'].update(self.days)

        current_time, current_time_str = self._generate_datetime_now()
        existing_data['updated_on'] = current_time_str
        existing_data['updated_on_timestamp'] = current_time

        self._client \
            .collection(f'Users/{self.psid}/Flow') \
            .document(self.id) \
            .set(existing_data, merge=True)

        return True

    def get(self) -> Union[None, Dict]:
        sent_triggers = self._client \
            .collection(f'Users/{self.psid}/Flow') \
            .document(self.id) \
            .get() \
            .to_dict()

        if not sent_triggers:
            return sent_triggers

        for key, value in sent_triggers.items():
            setattr(self, key, value)

        return sent_triggers

