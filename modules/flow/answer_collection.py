from google.cloud import firestore
from google.oauth2 import service_account

from settings import APP_ROOT


class AnswerCollection:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(f'{APP_ROOT}/credentials/kita-backend.json')

        self.__client = firestore.Client(credentials=credentials)

    def get_all_user_answers(self):
        answers = self.__client.collection_group('Answers').stream()

        return [answer.to_dict() for answer in answers]
