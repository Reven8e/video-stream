from src.CodeManage import CodeManage

from datetime import datetime, timedelta
import unittest, json


class TestCodeManage(unittest.TestCase):
    """
    A test case class for testing the functionality of the CodeManage class.
    """
    def __init__(self, methodName: str = "TestCodeManage") -> None:
        super().__init__(methodName)

        self.test_settings = json.load(open("tests/unittest_settings.json", "r"))

    def test_generate_access_code_true(self):
        """
        Test case for the generate_access_code method of the CodeManage class.

        Steps:
        1. Create an instance of the CodeManage class.
        2. Set the user_id to a real user ID.
        3. Set the movie_id to a real movie ID.
        4. Set the expiration_date to the current date and time plus one day.
        5. Generate an access code using the generate_access_code method.
        6. Assert that the access code is an instance of a string.
        7. Assert that the length of the access code is 10.
        """
        code_manager = CodeManage()

        user_id =self.test_settings['test_user']["user_id"]  # Real User ID.
        movie_id = self.test_settings['test_movie']["movie_id"]  # Real Movie ID.
        expiration_date = datetime.utcnow() + timedelta(days=1)

        access_code = code_manager.generate_access_code(user_id, movie_id, expiration_date)

        self.assertIsInstance(access_code, str)
        self.assertEqual(len(access_code), 10)
    
    def test_generate_access_code_false(self):
        """
        Test case for the generate_access_code method when the access code is not generated successfully.
        
        Steps:
        1. Create an instance of the CodeManage class.
        2. Set a fake user ID and a real movie ID.
        3. Set the expiration date to be one day from the current UTC datetime.
        4. Call the generate_access_code method with the user ID, movie ID, and expiration date.
        5. Assert that the generated access code is None.
        """
        code_manager = CodeManage()

        user_id = "58d3c9da-748E-40df-bde9-29179b400f8F"  # Fake user ID
        movie_id = self.test_settings['test_movie']["movie_id"]  # Real Movie ID.
        expiration_date = datetime.utcnow() + timedelta(days=1)

        access_code = code_manager.generate_access_code(user_id, movie_id, expiration_date)

        self.assertEqual(access_code, None)

    def test_check_access_code_false(self):
        """
        Test case to check the behavior of the check_access_code method when the access code is expired.
        
        Steps:
        1. Create an instance of the CodeManage class.
        2. Call the check_access_code method with an expired access code.
        3. Verify that the statement returned is False.
        4. Verify that the data returned is "Access code has expired."
        """
        code_manager = CodeManage()
        statement, data = code_manager.check_access_code(self.test_settings['test_access_code']["code_id"])  # Expired access code.
        self.assertEqual(statement, False)
        self.assertEqual(data, "Access code has expired.")

if __name__ == '__main__':
    unittest.main()
