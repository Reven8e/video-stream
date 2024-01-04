from src.DBMS import DBMS

from datetime import datetime, timedelta
import unittest, uuid

class TestDBMS(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_check_username_none(self):
        dbms = DBMS()
        data = dbms.check_username("testtesto")
        self.assertEqual(data, None)
        dbms.close_connection()

    def test_check_username(self):
        dbms = DBMS()
        data = dbms.check_username("bogan")
        self.assertEqual(data[1], "bogan")
        dbms.close_connection()

    def test_login_user_true(self):
        dbms = DBMS()
        statement, data = dbms.login_user("bogan", "123")
        self.assertEqual(statement, True)
        dbms.close_connection()

    def test_login_user_false(self):
        dbms = DBMS()
        statement, data = dbms.login_user("bogan", "1234")
        self.assertEqual(statement, False)
        dbms.close_connection()

    def test_register_user_false(self):
        dbms = DBMS()
        statement, data = dbms.register_user("bogan", "123")
        self.assertEqual(statement, False)
        self.assertEqual(data, "Username already exists.")
        dbms.close_connection()
    
    def test_insert_access_code_false(self):
        dbms = DBMS()
        expiration_date = datetime.utcnow() + timedelta(days=1)
        random_uuid = uuid.uuid4()

        statement = dbms.insert_access_code("test", 1, random_uuid, expiration_date)
        self.assertEqual(statement, False)
        dbms.close_connection()

    def test_check_access_code_false(self):
        dbms = DBMS()
        statement, _ = dbms.check_access_code("test")
        self.assertEqual(statement, False)

        statement2, data2 = dbms.check_access_code("iVZJ6M9bMg")  # Check for expiration.
        self.assertEqual(statement2, False)
        self.assertEqual(data2, "Access code has expired.")
        dbms.close_connection()

    def test_fetch_movies(self):
        dbms = DBMS()
        statement, data = dbms.fetch_movies()
        self.assertEqual(statement, True)
        self.assertIsInstance(data, list)
        dbms.close_connection()


    def test_fetch_movie(self):
        dbms = DBMS()
        statement, data = dbms.fetch_movie(1)
        self.assertEqual(statement, True)
        self.assertIsInstance(data, tuple)
        dbms.close_connection()

    def test_fetch_movie_false(self):
        dbms = DBMS()
        statement, data = dbms.fetch_movie(385237432432)
        self.assertEqual(statement, False)
        self.assertEqual(data, "Movie does not exist.")
        dbms.close_connection()

    def test_close_connection(self):
        dbms = DBMS()
        statement = dbms.close_connection()
        self.assertEqual(statement, None)
        dbms.close_connection()

if __name__ == '__main__':
    unittest.main()
