from typing import Union, Dict

from app.modules.base.model import Model


class Answer(Model):
    def __init__(self, psid: str, question_code: str, answer: str):
        super().__init__()

        self.psid = psid
        self.question_code = question_code
        self.answer = answer

    def save(self) -> bool:
        self._client \
            .collection(f'Users/{self.psid}/Answers') \
            .document(self.question_code) \
            .set(self.model_properties)

        return True

    def get(self) -> Union[None, Dict]:
        pass
