import psycopg2
from flask_bcrypt import Bcrypt

from datetime import datetime

import os, uuid, json


class DBMS:
    def __init__(self) -> None:
        self.__connection = psycopg2.connect(
            host=os.environ['PSQL_HOST'],
            user=os.environ['PSQL_USER'],
            password=os.environ['PSQL_PASSWORD']
        )

        self.bcrypt = Bcrypt()

    @staticmethod
    def __generate_uuid() -> str:
        return str(uuid.uuid4())
    
    def __check_user_id(self, user_id: str) -> tuple or None:
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
        
    def check_access_code(self, access_code: str) -> tuple:
        try:
            cursor = self.__connection.cursor()

            query = "SELECT * FROM access_codes WHERE code_id = %s"
            cursor.execute(query, (access_code,))
            data = cursor.fetchone()

            cursor.close()
            
            expiration = data[4].replace(tzinfo=None)

            if expiration < datetime.utcnow():
                return False, "Access code has expired."

            return True, data

        except Exception as e:
            print(e)
            return False, e
        
    def fetch_movies(self) -> tuple:
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
        self.__connection.close()
