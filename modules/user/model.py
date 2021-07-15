from typing import Union, Dict

from google.api_core.exceptions import AlreadyExists

from modules.base.model import Model


class User(Model):
    def __init__(self, psid: str):
        super().__init__()

        self.psid = psid

    def save(self) -> bool:
        try:
            self._client \
                .collection('Users') \
                .add(self.model_properties, document_id=self.psid)

            return True
        except AlreadyExists:
            return False

    def get(self) -> Union[None, Dict]:
        user_data = self._client \
            .collection('Users') \
            .document(self.psid) \
            .get() \
            .to_dict()

        if not user_data:
            return user_data

        for key, value in user_data.items():
            setattr(self, key, value)

        return user_data
