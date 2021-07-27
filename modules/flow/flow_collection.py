from google.cloud import firestore
from google.oauth2 import service_account

from settings import APP_ROOT


class FlowCollection:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(f'{APP_ROOT}/credentials/kita-backend.json')

        self.__client = firestore.Client(credentials=credentials)

    def get_all_users_finished_flow(self):
        return self.__client.collection_group('Flow'). \
            where('id', '==', 'Finished') \
            .stream()
