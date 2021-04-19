import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.main.config import basedir


class TestDEVConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.DEV")
        return app

    def test_app_in_dev_env(self):
        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "sqlite:///" + os.path.join(basedir, "database/github_users.db")
        )


class TestTESTConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.TEST")
        return app

    def test_app_in_test_env(self):
        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(app.config["PRESERVE_CONTEXT_ON_EXCEPTION"])
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "sqlite:///" + os.path.join(basedir, "database/github_users.db")
        )
        self.assertFalse(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertTrue(app.config["TESTING"])


class TestPRODConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.PROD")
        return app

    def test_app_in_prod_env(self):
        self.assertTrue(app.config["DEBUG"] is False)


if __name__ == "__main__":
    unittest.main()