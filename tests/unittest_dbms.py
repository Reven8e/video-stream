from src.DBMS import DBMS

from datetime import datetime, timedelta
import unittest, uuid, json

class TestDBMS(unittest.TestCase):
    """
    A test case class for testing the functionality of the DBMS class.
    """
    def __init__(self, methodName: str = "TestDBMS") -> None:
        super().__init__(methodName)

        self.test_settings = json.load(open("tests/unittest_settings.json", "r"))

    def test_check_username_none(self):
        """
        Test case to check if the username is None.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the check_username method with a test username.
        3. Assert that the returned data is None.
        4. Close the database connection.
        """
        dbms = DBMS()
        data = dbms.check_username("testtesto")
        self.assertEqual(data, None)
        dbms.close_connection()

    def test_check_username(self):
        """
        Test the check_username method of the DBMS class.

        Steps:
        1. Create an instance of the DBMS class.
        2. Call the check_username method with the username "bogan".
        3. Verify that the statement returned by the method is True.
        4. Verify that the data returned by the method is "bogan".
        5. Close the database connection.
        """
        dbms = DBMS()
        data = dbms.check_username(self.test_settings['test_user']["username"])

        self.assertEqual(data[1], self.test_settings['test_user']["username"])

        dbms.close_connection()

    def test_login_user_true(self):
        """
        Test case for the login_user method when the user credentials are valid.

        Steps:
        1. Create an instance of the DBMS class.
        2. Call the login_user method with valid username and password.
        3. Retrieve the statement and data returned by the method.
        4. Assert that the statement is True.
        5. Close the database connection.
        """
        dbms = DBMS()
        statement, data = dbms.login_user(self.test_settings['test_user']["username"], self.test_settings['test_user']["password"])
        self.assertEqual(statement, True)
        dbms.close_connection()

    def test_login_user_false(self):
        """
        Test case to verify the login_user method returns False when invalid credentials are provided.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the login_user method with invalid credentials ("bogan", "1234").
        3. Retrieve the statement returned by the login_user method.
        4. Assert that the statement is False.
        5. Close the database connection.
        """
        dbms = DBMS()
        statement, _ = dbms.login_user("testosfogdsfg", "1234")
        self.assertEqual(statement, False)
        dbms.close_connection()

    def test_register_user_false(self):
        """
        Test case to verify the register_user method when registering a user with an existing username.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the register_user method with a username and password.
        3. Verify that the statement returned is False.
        4. Verify that the data returned is "Username already exists."
        5. Close the database connection.
        """
        dbms = DBMS()
        statement, data = dbms.register_user(self.test_settings['test_user']["username"], self.test_settings['test_user']["password"])
        self.assertEqual(statement, False)
        self.assertEqual(data, "Username already exists.")
        dbms.close_connection()
    
    def test_insert_access_code_false(self):
        """
        Test case for the 'insert_access_code' method of the DBMS class when the statement returns False.

        This test verifies that the 'insert_access_code' method returns False when attempting to insert an access code into the database.

        Steps:
        1. Create an instance of the DBMS class.
        2. Generate a random UUID and an expiration date.
        3. Call the 'insert_access_code' method with the necessary parameters.
        4. Assert that the returned statement is False.
        5. Close the database connection.
        """
        dbms = DBMS()
        expiration_date = datetime.utcnow() + timedelta(days=1)
        random_uuid = str(uuid.uuid4())

        statement = dbms.insert_access_code("egdsfvdsgewc", 1, random_uuid, expiration_date)
        self.assertEqual(statement, False)
        dbms.close_connection()

    def test_check_access_code_false(self):
        """
        Test case to verify the 'fetch_access_code' method when the access code is invalid.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the 'fetch_access_code' method with an invalid access code.
        3. Retrieve the statement returned by the method.
        4. Assert that the statement is False.
        """
        dbms = DBMS()
        statement, _ = dbms.fetch_access_code("sfhsdgfasdasfafgdswgw")
        self.assertEqual(statement, False)

    def test_fetch_movies(self):
        """
        Test case for the fetch_movies method of the DBMS class.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the fetch_movies method to retrieve movies from the database.
        3. Check if the statement returned by fetch_movies is True.
        4. Check if the data returned by fetch_movies is a list.
        5. Close the database connection.
        """

        dbms = DBMS()
        statement, data = dbms.fetch_movies()
        self.assertEqual(statement, True)
        self.assertIsInstance(data, list)
        dbms.close_connection()

    def test_fetch_movie(self):
        """
        Test case for the fetch_movie method of the DBMS class.

        Steps:
        1. Create an instance of the DBMS class.
        2. Call the fetch_movie method with the movie ID as an argument.
        3. Assert that the statement returned by the method is True.
        4. Assert that the data returned by the method is an instance of tuple.
        5. Close the database connection.
        """
        dbms = DBMS()
        statement, data = dbms.fetch_movie(self.test_settings['test_movie']["movie_id"])
        self.assertEqual(statement, True)
        self.assertIsInstance(data, tuple)
        dbms.close_connection()

    def test_fetch_movie_false(self):
        """
        Test case to verify the fetch_movie method when the movie does not exist.
        
        Steps:
        1. Create an instance of the DBMS class.
        2. Call the fetch_movie method with a non-existent movie ID.
        3. Verify that the statement returned is False.
        4. Verify that the data returned is "Movie does not exist."
        5. Close the database connection.
        """
        dbms = DBMS()
        statement, data = dbms.fetch_movie(385237432432)
        self.assertEqual(statement, False)
        self.assertEqual(data, "Movie does not exist.")
        dbms.close_connection()

    def test_close_connection(self):
        """
        Test case for the close_connection method of the DBMS class.

        Steps:
        1. Create an instance of the DBMS class.
        2. Call the close_connection method.
        3. Assert that the return value is None.
        4. Call the close_connection method again.
        """
        dbms = DBMS()
        statement = dbms.close_connection()
        self.assertEqual(statement, None)
        dbms.close_connection()


if __name__ == '__main__':
    unittest.main()
