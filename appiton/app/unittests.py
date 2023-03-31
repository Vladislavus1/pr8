import unittest
import requests
import json
class TestCalendarAPI(unittest.TestCase):
    global token

    def setUp(self) -> None:
        self.url = "http://127.0.0.1:5000"
        self.header = {"Content-type": "Application/json"}
        self.login_data = {
            "nickname": "test_nickname",
            "password": "test_pwd",
            "email": "email@ema.com"
        }
        self.event_data = {
            "date": "15-03-2023",
            "time": "12:12",
            "header": "header",
            "description": "description"
        }

    def test1_signup(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isRegistered"])

    def test2_signup_with_same_data(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["isRegistered"], False)
        self.assertEqual(response.json()["reason"], "userExists")

    def test3_login_with_correct_data(self):
        global token
        response = requests.post(f"{self.url}/login.html", json=self.login_data, headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.json())
        self.assertTrue(response.json()["isLogged"])

        token = response.json()["token"]

    def test4_delete_created_user(self):
        response = requests.get(f"{self.url}/delete_user_by/{self.login_data['nickname']}", headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isDeleted"])

    def test5_create_events(self):
        response = requests.post(f"{self.url}/create_event", json=self.event_data, headers=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isAdded"])

    def test6_check_events(self):
        response = requests.get(f"{self.url}/get_events_by_date/{self.event_data['date']}", headers=self.header)

        self.assertEqual(response.status_code, 200)
        print(json.loads(response.json()["data"][0]))
        self.assertEqual(json.loads(response.json()["data"][0])['time'], self.event_data['time'])



if __name__ == "__main__":
    unittest.main()