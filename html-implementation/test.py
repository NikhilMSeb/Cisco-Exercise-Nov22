from app import app
import unittest         # Python standard package 


class FlaskUnitTest(unittest.TestCase):

    # Testcase: ensuring basic API landing point works no matter what 
    def test_welcome(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)


    # Testcase: ensuring that the 4 endpoints that need authorization are blocked before login
    def test_home_access(self):         # Post log in landing page 
        tester = app.test_client()
        response = tester.get("/home", follow_redirects=True)
        self.assertIn(b'LOG IN REQUIRED TO ACCESS', response.data)

    def test_all_access(self):          # GET request for all available malware URL database data
        tester = app.test_client()
        response = tester.get("/v1/urlinfo/all", follow_redirects=True)
        self.assertIn(b'LOG IN REQUIRED TO ACCESS', response.data)

    def test_lookup_access(self):       # GET request for a specific URL's malware status
        tester = app.test_client()
        response = tester.get("/v1/urlinfo/url", follow_redirects=True)
        self.assertIn(b'LOG IN REQUIRED TO ACCESS', response.data)

    def test_logout_access(self):       # Log out request 
        tester = app.test_client()
        response = tester.get("/logout", follow_redirects=True)
        self.assertIn(b'LOG IN REQUIRED TO ACCESS', response.data)


    # Testcase: verifying complete login functionality 
    def test_login_view(self):          # Ensuring that login page prompts to the main requirement for access - logging in
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertIn(b'Please login', response.data)
    
    def test_login(self):               # Verifying that using valid credentials does log you in (redirect takes you to home page)
        tester = app.test_client()
        response = tester.post(
            "/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You are logged in', response.data)

    def test_wrong_login(self):         # Verifying that using incorrect credentials throws an error 
        tester = app.test_client()
        response = tester.post(
            "/login",
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Incorrect Username and/or Password', response.data)

    
    # Testcase: verifying logout functionality 
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            "/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get("/logout", follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)


    # Testcase: ensuring that the listing of all database data is available as expected after login 
    def test_api_all(self):
        tester = app.test_client()
        tester.post(
            "/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get("/v1/urlinfo/all", follow_redirects=True)
        # Ensuring that all of the dummy data is displayed (edit as needed)
        with self.subTest():
            self.assertIn(b'cisco.com', response.data)
        with self.subTest():
            self.assertIn(b'google.com', response.data)
        with self.subTest():
            self.assertIn(b'nikhil.accept', response.data)
        with self.subTest():
            self.assertIn(b'evil.com', response.data)
        with self.subTest():
            self.assertIn(b'criminal.com', response.data)
        with self.subTest():
            self.assertIn(b'nikhil.reject', response.data)

    
    # Testcase: ensuring that the URL malware lookup is available as expected after login
    def test_api_lookup(self): 
        tester = app.test_client()
        tester.post(
            "/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get("/v1/urlinfo/cisco.com", follow_redirects=True)
        # Ensuring that the response matches the test route 
        with self.subTest():
            self.assertIn(b'GOOD', response.data)
        with self.subTest():
            self.assertIn(b'cisco.com', response.data)
    
    def test_lookup_error(self):        # Verifying that incorrect lookup access does cause the expected error message
        tester = app.test_client()
        tester.post(
            "/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get("/v1/urlinfo/random", follow_redirects=True)
        self.assertIn(b'URL NOT FOUND IN DATABASE', response.data)


if __name__ == '__main__':
    unittest.main()
