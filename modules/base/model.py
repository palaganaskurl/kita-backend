from abc import abstractmethod
from datetime import datetime
from typing import Union, Dict

import pytz
from google.cloud import firestore
from google.oauth2 import service_account

from settings import APP_ROOT


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class Model:
    def __init__(self):
        current_time, current_time_str = self._generate_datetime_now()

        self.created_on = current_time_str
        self.updated_on = current_time_str
        self.created_on_timestamp = current_time
        self.updated_on_timestamp = current_time

        credentials = service_account.Credentials.from_service_account_file(f'{APP_ROOT}/credentials/kita-backend.json')

        self._client = firestore.Client(credentials=credentials)

    # noinspection PyMethodMayBeStatic
    def _generate_datetime_now(self):
        timezone = pytz.timezone('Asia/Manila')
        utc_now = pytz.utc.localize(datetime.utcnow())
        current_time = utc_now.astimezone(timezone)

        return current_time, current_time.strftime(DATE_FORMAT)

    @property
    def model_properties(self):
        properties = vars(self)
        filtered_properties = {}

        for key, value in properties.items():
            if key.startswith('_'):
                continue

            filtered_properties[key] = value

        return filtered_properties

    @abstractmethod
    def save(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Union[None, Dict]:
        raise NotImplementedError()
