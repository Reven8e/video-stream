import psycopg2
from flask_bcrypt import Bcrypt

import os, uuid, json


class DBMS:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            host=os.environ['PSQL_HOST'],
            user=os.environ['PSQL_USER'],
            password=os.environ['PSQL_PASSWORD']
        )

        self.bcrypt = Bcrypt()

    @staticmethod
    def __generate_uuid() -> str:
        return str(uuid.uuid4())

    def close_connection(self) -> None:
        self.connection.close()

    def check_username(self, username: str) -> bool:
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchone()

            return data
        except Exception as e:
            print(e)
            return
    
    def login_user(self, username: str, password: str) -> tuple:
        try:
            cursor = self.connection.cursor()

            query = "SELECT user_id, password_hash FROM users WHERE username = %s"
            cursor.execute(query, (username,))

            data = cursor.fetchone()

            if data is None:
                return False, "Username is incorrect!"

            user_id = data[0]
            sql_password_hash = data[1]

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
            cursor = self.connection.cursor()

            user = self.check_username(username)

            if user is not None:
                return False, "Username already exists."

            hashed_password = self.bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')
            user_uuid = DBMS.__generate_uuid()

            query = "INSERT INTO users (user_id, username, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_uuid, username, hashed_password))

            self.connection.commit()
            cursor.close()

            return True, json.dumps({
                "user_id": user_uuid,
                "user_name": username,
            })

        except Exception as e:
            print(e)
            return False, e
