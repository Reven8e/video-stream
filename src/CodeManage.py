from src.DBMS import DBMS

from datetime import datetime

import random, string


class CodeManage:
    __SIZE: int = 10

    def __init__(self) -> None:
        self.db = DBMS()

    def __del__(self):
        self.db.close_connection()

    def __generate_random_code(self) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(self.__SIZE))
    
    def generate_access_code(self, user_id: str, movie_id: int, expiration_date: datetime) -> str or None:
        random_code = self.__generate_random_code()

        if self.db.insert_access_code(random_code, movie_id, user_id, expiration_date):
            return random_code
        else:
            return
    
    def check_access_code(self, access_code: str) -> bool:
        return self.db.check_access_code(access_code)
