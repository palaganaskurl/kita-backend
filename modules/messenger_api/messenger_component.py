from abc import abstractmethod
from typing import Dict


class MessengerComponent:
    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError()
