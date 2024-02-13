from unittest import TestCase
from src.app import create_app
from src.models.db import db

class TestFlaskBase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.app_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

    def tearDown(self):
        # self.app_context.pop()
        self.app.db.drop_all()
