
from datetime import datetime


class DatabaseCore:

    @staticmethod
    def time_stamp(name: str):
        return {name: datetime.utcnow()}
