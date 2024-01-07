import psycopg2
from flask_bcrypt import Bcrypt

import os, uuid, json


class DBMS:
    """
    A class representing a Database Management System (DBMS).

    Attributes:
        __connection (psycopg2.extensions.connection): The connection to the PostgreSQL database.
        bcrypt (Bcrypt): The Bcrypt object for password hashing.

    Methods:
        __init__: Initializes the DBMS object and establishes a connection to the database.
        __generate_uuid: Generates a UUID string.
        __check_user_id: Checks if a user ID exists in the database.
        check_username: Checks if a username exists in the database.
        login_user: Authenticates a user by checking the username and password.
        register_user: Registers a new user in the database.
        insert_access_code: Inserts an access code into the database.
        check_access_code: Checks if an access code is valid and not expired.
        fetch_movies: Fetches all movies from the database.
        fetch_movie: Fetches a specific movie from the database.
        close_connection: Closes the database connection.
    """

    def __init__(self) -> None:
        """
        Initializes the DBMS object and establishes a connection to the database.
        """
        self.__connection = psycopg2.connect(
            host=os.environ['PSQL_HOST'],
            user=os.environ['PSQL_USER'],
            password=os.environ['PSQL_PASSWORD']
        )

        self.bcrypt = Bcrypt()

    @staticmethod
    def __generate_uuid() -> str:
        """
        Generates a UUID string.

        Returns:
            str: The generated UUID string.
        """
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
            cursor = self.__connection.cursor()

            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            data = cursor.fetchone()

            cursor.close()
            return data
        except Exception as e:
            print(e)
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
            cursor = self.__connection.cursor()

            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchone()

            cursor.close()
            return data
        except Exception as e:
            print(e)
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
            data = self.check_username(username)

            if data is None:
                return False, "Username is incorrect!"

            user_id = data[0]
            sql_password_hash = data[2]

            if not self.bcrypt.check_password_hash(sql_password_hash, password):
                return False, "Password is incorrect!"

            return True, json.dumps({
                "user_id": user_id,
                "user_name": username,
            })

        except ZeroDivisionError:
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
            cursor = self.__connection.cursor()

            user = self.check_username(username)

            if user is not None:
                return False, "Username already exists."

            hashed_password = self.bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')
            user_uuid = DBMS.__generate_uuid()

            query = "INSERT INTO users (user_id, username, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_uuid, username, hashed_password))

            self.__connection.commit()
            cursor.close()

            return True, json.dumps({
                "user_id": user_uuid,
                "user_name": username,
            })

        except Exception as e:
            print(e)
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

            cursor = self.__connection.cursor()

            query = "INSERT INTO access_codes (code_id, movie_id, user_id, expires_at) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (access_code, movie_id, user_id, expiration_date)) 

            self.__connection.commit()
            cursor.close()

            return True

        except Exception as e:
            print(e)
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
            cursor = self.__connection.cursor()

            query = "SELECT * FROM access_codes WHERE code_id = %s"
            cursor.execute(query, (access_code,))
            data = cursor.fetchone()

            cursor.close()

            if data is None:
                return False, "Access code does not exist."

            return True, data

        except Exception as e:
            print(e)
            return False, e
        
    def fetch_movies(self) -> tuple:
        """
        Fetches all movies from the database.

        Returns:
            tuple: A tuple containing a boolean indicating the fetch result and a list of movie data
                   if the fetch is successful, or an error message if not.
        """
        try:
            cursor = self.__connection.cursor()

            query = "SELECT * FROM movies"
            cursor.execute(query)
            data = cursor.fetchall()

            cursor.close()
            return True, data

        except Exception as e:
            print(e)
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
            cursor = self.__connection.cursor()

            query = "SELECT * FROM movies WHERE movie_id = %s"
            cursor.execute(query, (movie_id,))

            data = cursor.fetchone()
            cursor.close()

            if data is None:
                return False, "Movie does not exist."

            return True, data

        except Exception as e:
            print(e)
            return False, e

    def close_connection(self) -> None:
        """
        Closes the database connection.
        """
        self.__connection.close()
