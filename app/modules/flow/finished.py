from typing import Union, Dict

from modules.base.model import Model


class FinishedFlow(Model):
    def __init__(self, psid: str, day: str):
        super().__init__()

        self.id = 'Finished'
        self.psid = psid
        self.days = {day: 'finished'}

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
        return self._client \
            .collection(f'Users/{self.psid}/Flow') \
            .document(self.id) \
            .get() \
            .to_dict()
