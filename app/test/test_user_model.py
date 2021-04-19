import unittest

from app.main import db
from app.main.models.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_create_user(self):
        user = User(
            id=2000,
            username="test_user",
            image_url="test_image",
            type="User",
            profile_url="test_link",
        )

        db.session.add(user)
        db.session.commit()

        self.assertTrue(isinstance(user, User))


if __name__ == "__main__":
    unittest.main()