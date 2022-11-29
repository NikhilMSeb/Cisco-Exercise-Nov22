from app import app
import json
import unittest         # Python standard package 


class FlaskUnitTest(unittest.TestCase):

    # Testcase: ensuring basic API landing point works no matter what 
    def test_welcome(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)


    # Testcase: ensuring that the 4 endpoints that need authorization are blocked before login
    def test_all_access(self):          # GET request for all available malware URL database data
        tester = app.test_client()
        response = tester.get("/v1/urlinfo/all")
        self.assertIn(b'Authentication token missing', response.data)

    def test_lookup_access(self):       # GET request for a specific URL's malware status
        tester = app.test_client()
        response = tester.get("/v1/urlinfo/url")
        self.assertIn(b'Authentication token missing', response.data)


    # Testcase: verifying complete login functionality 
    def test_login(self):               # Verifying that using valid credentials does log you in 
        tester = app.test_client()
        response = tester.post(
            "/login",
            data='{"username" : "admin", "password" : "admin"}', 
            content_type='application/json'
        )
        self.assertIn(b'Logged in successfully', response.data)

    def test_wrong_login(self):         # Verifying that using incorrect credentials throws an error 
        tester = app.test_client()
        response = tester.post(
            "/login",
            data='{"username" : "wrong", "password" : "wrong"}',
            content_type='application/json'
        )
        self.assertIn(b'Incorrect Username and/or Password', response.data)

    
    # Testcase: ensuring that the listing of all database data is available as expected after login 
    def test_api_all(self):
        tester = app.test_client()
        response_1 = tester.post(
            "/login",
            data='{"username" : "admin", "password" : "admin"}', 
            content_type='application/json'
        )
        resp_data = json.loads((response_1.data))
        resp_json = json.loads(json.dumps(resp_data, indent=4, sort_keys=True))
        access_token = resp_json['api-access-token']

        response_2 = tester.get("/v1/urlinfo/all", headers={'api-access-token' : access_token})
        # Ensuring that all of the dummy data is displayed (edit as needed)
        with self.subTest():
            self.assertIn(b'cisco.com', response_2.data)
        with self.subTest():
            self.assertIn(b'google.com', response_2.data)
        with self.subTest():
            self.assertIn(b'nikhil.accept', response_2.data)
        with self.subTest():
            self.assertIn(b'evil.com', response_2.data)
        with self.subTest():
            self.assertIn(b'criminal.com', response_2.data)
        with self.subTest():
            self.assertIn(b'nikhil.reject', response_2.data)

    
    # Testcase: ensuring that the URL malware lookup is available as expected after login
    def test_api_lookup(self): 
        tester = app.test_client()
        response_1 = tester.post(
            "/login",
            data='{"username" : "admin", "password" : "admin"}', 
            content_type='application/json'
        )
        resp_data = json.loads((response_1.data))
        resp_json = json.loads(json.dumps(resp_data, indent=4, sort_keys=True))
        access_token = resp_json['api-access-token']

        response = tester.get("/v1/urlinfo/cisco.com", headers={'api-access-token' : access_token})
        # Ensuring that the response matches the test route 
        with self.subTest():
            self.assertIn(b'GOOD', response.data)
        with self.subTest():
            self.assertIn(b'cisco.com', response.data)
    
    def test_lookup_error(self):        # Verifying that incorrect lookup access does cause the expected error message
        tester = app.test_client()
        response_1 = tester.post(
            "/login",
            data='{"username" : "admin", "password" : "admin"}', 
            content_type='application/json'
        )
        resp_data = json.loads((response_1.data))
        resp_json = json.loads(json.dumps(resp_data, indent=4, sort_keys=True))
        access_token = resp_json['api-access-token']

        response = tester.get("/v1/urlinfo/random", headers={'api-access-token' : access_token})
        self.assertIn(b'URL NOT FOUND IN DATABASE', response.data)


if __name__ == '__main__':
    unittest.main()
