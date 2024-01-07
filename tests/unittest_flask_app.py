from app import app

import unittest, json, random, string

class FlaskIntegrationTesting(unittest.TestCase):

    def __init__(self, methodName: str = "FlaskIntegrationTesting") -> None:
        super().__init__(methodName)

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_user_true(self):
        """
        Test case to verify successful login of a user.
        
        Steps:
        1. Send a POST request to '/login' endpoint with valid username and password.
        2. Verify that the response is a redirect.
        3. Access the session and verify that 'logged_in' key is set to True.
        4. Access the session and verify that 'user' key contains the expected user information.
        """
        self.app.post('/login', data=dict(
            username="bogan",
            password="123"
        ), follow_redirects=True)

        with self.app.session_transaction() as session:
            self.assertEqual(session['logged_in'], True)
            self.assertEqual(json.loads(session['user'])['user_name'], "bogan")

    def test_login_user_false(self):
        """
        Test case for logging in with incorrect credentials.
        
        Steps:
        1. Send a POST request to '/login' with incorrect username and password.
        2. Follow the redirects.
        3. Assert that the 'logged_in' session variable is None.
        4. Assert that the 'user' session variable is None.
        """
        self.app.post('/login', data=dict(
            username="bogan123",
            password="1234erer"
        ), follow_redirects=True)

        with self.app.session_transaction() as session:
            self.assertEqual(session.get('logged_in'), None)
            self.assertEqual(session.get('user'), None)

    def test_register_user_true(self):
        """
        Test case to verify the registration of a user with valid credentials.

        Steps:
        1. Generate a random username and password.
        2. Send a POST request to the '/signup' endpoint with the random username and password.
        3. Verify that the request is successful and the user is redirected.
        4. Access the session and verify that the user is logged in.
        5. Verify that the username stored in the session matches the random username.
        """
        random_username = 'test-' + ''.join(random.choice(string.ascii_letters) for i in range(6))
        random_password = ''.join(random.choice(string.ascii_letters) for i in range(10))

        self.app.post('/signup', data=dict(
            username=random_username,
            password1=random_password,
            password2=random_password
        ), follow_redirects=True)

        with self.app.session_transaction() as session:
            self.assertEqual(session['logged_in'], True)
            self.assertEqual(json.loads(session['user'])['user_name'], random_username)

    def test_register_user_false(self):
        """
        Test case for registering a user with incorrect credentials.

        Steps:
        1. Send a POST request to '/signup' with the used username and password.
        2. Follow the redirects.
        3. Assert that the 'logged_in' session variable is None.
        4. Assert that the 'user' session variable is None.
        """
        self.app.post('/signup', data=dict(
            username="bogan",
            password1="123",
            password2="123"
        ), follow_redirects=True)

        with self.app.session_transaction() as session:
            self.assertEqual(session.get('logged_in'), None)
            self.assertEqual(session.get('user'), None)

    def test_fetch_movies_true(self):
            """
            Test case to verify the successful fetching of available movies.
            
            Steps:
            1. Login to the application.
            2. Send a GET request to the '/videostream/available_movies' endpoint.
            3. Verify that the response status code is 200.
            """
            self.app.post('/login', data=dict(  # Login
                username="bogan",
                password="123"
            ), follow_redirects=True)

            response = self.app.get('/videostream/available_movies', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_create_watch_stream_true(self):
        """
        Test case for creating a watch stream with valid credentials.
        
        Steps:
        1. Login with username and password.
        2. Send a POST request to '/videostream/available_movies' endpoint with movie_id and expiration_date.
        3. Assert that the response status code is 200.
        """
        self.app.post('/login', data=dict(  # Login
            username="bogan",
            password="123"
        ), follow_redirects=True)

        response = self.app.post('/videostream/available_movies', data=dict(
            movie_id=1,
            expiration_date=1
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
