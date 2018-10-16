import json
import unittest

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'generic_user2@guser.org',
                    'password': 'mypass'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            # before calling this code, if 409 user already exists.
            if not response.status_code == 409 and not \
                    response.status_code == 200:
                self.assertEqual(response.status_code, 201)
                self.assertIn(
                    'generic_user@guser.org was added!', data['message'])
                self.assertIn('success', data['status'])
            elif response.status_code == 200:
                self.assertIn(
                    'Sorry. That user already exists.', data['message'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'generic_user@guser.org'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'password': 'mypass',
                    'email': 'generic_user@guser.org'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'password': 'mypass',
                    'email': 'generic_user@guser.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()
