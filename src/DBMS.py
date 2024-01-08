from flask_bcrypt import Bcrypt

from src.DBInterfaces import DatabaseInterface

import uuid, json


class DBMS:
    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.bcrypt = Bcrypt()

    @staticmethod
    def __generate_uuid() -> str:
        return str(uuid.uuid4())

    def __check_user_id(self, user_id: str) -> tuple or None:
        """
        Checks if a user ID exists in the database.

        Args:
            user_id (str): The user ID to check.

        Returns:
            tuple or None: The user data if the user ID exists, None otherwise.
        """
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            return self.database.execute_query(query, (user_id,), fetch='one')
        except Exception as e:
            print('[__check_user_id]', e)
            return

    def check_username(self, username: str) -> tuple or None:
        """
        Checks if a username exists in the database.

        Args:
            username (str): The username to check.

        Returns:
            tuple or None: The user data if the username exists, None otherwise.
        """
        try:
            query = "SELECT * FROM users WHERE username = %s"
            return self.database.execute_query(query, (username,), fetch='one')
        except Exception as e:
            print('[check_username]', e)
            return
        
    def login_user(self, username: str, password: str) -> tuple:
        """
        Authenticates a user by checking the username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            tuple: A tuple containing a boolean indicating the authentication result and a JSON string
                   containing the user ID and username if authentication is successful, or an error message if not.
        """
        try:
            check_username = self.check_username(username)

            if check_username is None:
                return False, "Username is incorrect!"
            
            user_id, sql_password_hash = check_username[0], check_username[2]

            if not self.bcrypt.check_password_hash(sql_password_hash, password):
                return False, "Password is incorrect!"

            return True, json.dumps({
                "user_id": user_id,
                "user_name": username,
            })

        except Exception as e:
            print('[login_user]', e)
            return False, 'e'
        
    def register_user(self, username: str, password: str) -> tuple:
        """
        Registers a new user in the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            tuple: A tuple containing a boolean indicating the registration result and a JSON string
                   containing the user ID and username if registration is successful, or an error message if not.
        """
        try:
            check_username = self.check_username(username)

            if check_username is not None:
                return False, "Username already exists."

            user_id = self.__generate_uuid()
            password_hash = self.bcrypt.generate_password_hash(password).decode('utf-8')

            query = "INSERT INTO users (user_id, username, password_hash) VALUES (%s, %s, %s)"
            self.database.execute_query(query, (user_id, username, password_hash), fetch=None)
            self.database.commit()

            return True, json.dumps({
                "user_id": user_id,
                "user_name": username,
            })

        except Exception as e:
            print('[register_user]', e)
            return False, e
        
    def insert_access_code(self, access_code: str, movie_id: int, user_id: str, expiration_date) -> bool:
        """
        Inserts an access code into the database.

        Args:
            access_code (str): The access code to insert.
            movie_id (int): The ID of the movie associated with the access code.
            user_id (str): The ID of the user associated with the access code.
            expiration_date: The expiration date of the access code.

        Returns:
            bool: True if the access code is successfully inserted, False otherwise.
        """
        try:
            check_user = self.__check_user_id(user_id)

            if check_user is None:
                return False
            
            query = "INSERT INTO access_codes (code_id, movie_id, user_id, expires_at) VALUES (%s, %s, %s, %s)"
            self.database.execute_query(query, (access_code, movie_id, user_id, expiration_date), fetch=None)
            self.database.commit()

            return True
        
        except Exception as e:
            print('[insert_access_code]', e)
            return False

    def fetch_access_code(self, access_code: str) -> tuple:
        """
        Fetches the access code from the database.

        Args:
            access_code (str): The access code to fetch.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the access code exists and the fetched data.
                   If the access code does not exist, the boolean value will be False and an error message will be returned.
        """
        try:
            query = "SELECT * FROM access_codes WHERE code_id = %s"
            sql = self.database.execute_query(query, (access_code,), fetch='one')

            if sql is None:
                return False, "Access code does not exist!"

            return True, sql

        except Exception as e:
            print('[fetch_access_code]', e)
            return False, e

    def fetch_movies(self):
        try:
            query = "SELECT * FROM movies"
            sql = self.database.execute_query(query)
            if sql:
                return True, sql
            else:
                return False, sql

        except Exception as e:
            print('[fetch_movies]', e)
            return False, e
        
    def fetch_movie(self, movie_id: int) -> tuple:
        """
        Fetches a specific movie from the database.

        Args:
            movie_id (int): The ID of the movie to fetch.

        Returns:
            tuple: A tuple containing a boolean indicating the fetch result and the movie data
                   if the fetch is successful, or an error message if not.
        """
        try:
            query = "SELECT * FROM movies WHERE movie_id = %s"
            sql = self.database.execute_query(query, (movie_id,), fetch='one')
            if sql:
                return True, sql
            else:
                return False, "Movie does not exist."

        except Exception as e:
            print('[fetch_movie]', e)
            return False, e

    def close_connection(self):
        self.database.close()
