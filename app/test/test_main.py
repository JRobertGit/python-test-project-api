import unittest

import json
from app.test.base import BaseTestCase


class TestAPI(BaseTestCase):
    def test_users_api(self):
        with self.client:
            response = self.client.get("/api/users/profiles")
            data = json.loads(response.data.decode())
            self.assertTrue(data["has_next"] == False)
            self.assertTrue(data["has_prev"] == False)
            self.assertTrue(data["next_num"] == None)
            self.assertTrue(data["prev_num"] == None)
            self.assertTrue(data["users"] == [])
            self.assertEqual(response.status_code, 200)


class TestView(BaseTestCase):
    def test_users_view(self):
        with self.client:
            response = self.client.get("/")
            self.assertTrue(b"<title>Python Test GitHub Users</title>" in response.data)
            self.assertEqual(response.status_code, 200)

            response = self.client.get("/users")
            self.assertTrue(b"<title>Python Test GitHub Users</title>" in response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()