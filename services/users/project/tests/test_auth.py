import json
from project.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post('/auth/register', data=json.dumps(
                {
                    'email': 'generic_user@guser.org',
                    'password': 'mypass'
                }),
                content_type='application/json')
        data = json.loads(response.data.decode())
        # before calling this code, if 409 or 200 user already exists.
        if not response.status_code == 409 and not \
                        response.status_code == 200:
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'generic_user@guser.org was added!', data['message'])
            self.assertIn('success', data['status'])
        elif response.status_code == 200:
            self.assertIn(
                'Sorry. That user already exists.', data['message'])

    def test_user_registration_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object does not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({'email': 'generic_user@guser.org'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_email(self):
        """
        Ensure error is thrown if the JSON object does not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({'password': 'mypass'}),
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
                '/auth/register',
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

    def test_user_login(self):
        with self.client:
            response = self.client.post('/auth/login', data=json.dumps(
                {
                    'email': 'generic_user@guser.org',
                    'password': 'mypass'
                }),
                content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', data['status'])
        self.assertIn(
            'Successfully logged in.', data['message'])
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')

    def test_user_login_not_exist(self):
        with self.client:
            response = self.client.post('/auth/login', data=json.dumps(
                {
                    'email': 'generic_user2100@guser.org',
                    'password': 'mypass'
                }),
                                        content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Sorry. That user does not exist.', data['message'])
        self.assertIn('fail', data['status'])

