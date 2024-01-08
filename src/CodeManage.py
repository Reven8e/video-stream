from src.DBMS import DBMS

from src.DBInterfaces import PostgresDatabase
from datetime import datetime

import random, string


class CodeManage:
    """
    Class responsible for managing access codes for movies.
    """

    __SIZE: int = 10

    def __init__(self) -> None:
        """
        Constructor for the CodeManage class.
        """
        self.db = DBMS(PostgresDatabase())

    def __del__(self):
        """
        Destructor for the CodeManage class.
        """
        self.db.close_connection()

    def __generate_random_code(self) -> str:
        """
        Generates a random access code.

        Returns:
            str: Randomly generated access code.
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(self.__SIZE))
    
    def generate_access_code(self, user_id: str, movie_id: int, expiration_date: datetime) -> str or None:
        """
        Generates an access code for a specific user and movie.

        Args:
            user_id (str): ID of the user.
            movie_id (int): ID of the movie.
            expiration_date (datetime): Expiration date of the access code.

        Returns:
            str or None: Generated access code if successful, None otherwise.
        """
        random_code = self.__generate_random_code()

        if self.db.insert_access_code(random_code, movie_id, user_id, expiration_date):
            return random_code
        else:
            return
    
    def check_access_code(self, access_code: str) -> bool:
        """
        Checks if an access code is valid.

        Args:
            access_code (str): Access code to check.

        Returns:
            bool: True if the access code is valid, False otherwise.
        """
        statement, data = self.db.fetch_access_code(access_code)

        if statement is False:
            return False, data

        expiration = data[4].replace(tzinfo=None)

        if expiration < datetime.utcnow():
            return False, "Access code has expired."

        return True, data
