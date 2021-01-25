import unittest
import warnings
import json
from werkzeug.security import generate_password_hash
import uuid
from base64 import b64encode

from number_api import get_dids
from settings import app


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.credentials = b64encode(b"example:justAnExample").decode("utf8")

    def test_signup_user(self):
        password = 'justAnExample'
        hashed_password = generate_password_hash(password, method='sha256')
        with app.test_client() as client:
            response = client.post(
                '/register',
                data=json.dumps(dict(
                    public_id = str(uuid.uuid4()),
                    name = 'example',
                    password = password
                )),
                content_type='application/json'
            )
            response_data = response.get_data()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response_data.decode("utf-8"),
                'registered successfully'
            )

    def test_login_user(self):
        with app.test_client() as client:
            response = client.get(
                "/login",
                headers={
                    "Authorization": f"Basic {self.credentials}".format()
                }
            )
            keys = [key for key in response.json.keys()]

            self.assertEqual("token", keys[0])

    def test_login_empty_user(self):
        self.credentials = b64encode(b":").decode("utf8")
        with app.test_client() as client:
            response = client.get(
                "/login",
                headers={
                    "Authorization": f"Basic {self.credentials}".format()
                }
            )
            self.assertEqual(401, response.status_code)

    def test_login_password_error(self):
        self.credentials = b64encode(b"example:test123").decode("utf8")
        with app.test_client() as client:
            response = client.get(
                "/login",
                headers={
                    "Authorization": f"Basic {self.credentials}".format()
                }
            )
            self.assertEqual(401, response.status_code)

    def test_get_all_users(self):
        with app.test_client() as client:
            response = client.get(
                "/users",
                headers={
                    "Authorization": f"Basic {self.credentials}"
                }
            )
            users = response.json.keys()
            keys = [key for key in users]

            self.assertEqual("users", keys[0])

    def test_remove_user(self):

        with app.test_client() as client:
            response = client.get(
                "/login",
                headers={
                    "Authorization": f"Basic {self.credentials}"
                }
            )
            token = [value for value in response.json.values()]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response_id = client.get(
                    "/users",
                    headers={
                        "Authorization": f"Basic {self.credentials}"
                    }
                )
                first = response_id.get_json()['users'][0]
                response = client.delete(
                    "/remove_user/{first['public_id']}",
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":token[0],
                    }
                )
        self.assertEqual(200, response.status_code)


class TestDIDNumber(unittest.TestCase):
    def setUp(self):
        self.credentials = b64encode(b"example:justAnExample").decode("utf8")
        with app.test_client() as self.client:
            response = self.client.get(
                "/login",
                headers={
                    "Authorization": f"Basic {self.credentials}"
                }
            )
        token = [value for value in response.json.values()]
        self.token = token[0]

    def test_invalid_token(self):
        response = self.client.get('/dids')
        message = response.json['message']

        self.assertEqual('a valid token is missing', message)

    def test_get_dids(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            response = self.client.get(
                "/dids",
                headers={
                    "Content-Type": "application/json",
                    "x-access-tokens":self.token
                }
            )
        self.assertEqual(200, response.status_code)

    def test_get_did_by_id(self):
        id = 2
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            response = self.client.get(
                f'/dids/{id}',
                headers={
                    "Content-Type": "application/json",
                    "x-access-tokens":self.token
                }
            )

        keys = response.json[0]
        self.assertEqual(2, keys['id'])
        self.assertEqual(200, response.status_code)

    def test_add_did(self):
        with app.test_client() as client:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response = client.post(
                    '/dids',
                    data=json.dumps(dict(
                        value = '11987654321',
                        monthyPrice = 1.23,
                        setupPrice = 3.45,
                        currency = 'U$'
                    )),
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":self.token
                    },
                )

            self.assertEqual(response.status_code, 201)

    def test_add_did_negative(self):
        with app.test_client() as client:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response = client.post(
                    '/dids',
                    data=json.dumps(dict(
                        value = '11987654321',
                        monthyPrice = -1.23,
                        setupPrice = 3.45,
                        currency = 'U$'
                    )),
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":self.token
                    },
                )

            self.assertEqual(response.status_code, 400)

    def test_add_did_int_value(self):
        with app.test_client() as client:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response = client.post(
                    '/dids',
                    data=json.dumps(dict(
                        value = 11987654321,
                        monthyPrice = 1.23,
                        setupPrice = 3.45,
                        currency = 'U$'
                    )),
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":self.token
                    },
                )

            self.assertEqual(response.status_code, 201)

    def test_update_did(self):
        id = 1
        with app.test_client() as client:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response = client.put(
                    f'/dids/{id}',
                    data=json.dumps(dict(
                        id = id,
                        value = 11987654321,
                        monthyPrice = 1.23,
                        setupPrice = 3.45,
                        currency = 'U$'
                    )),
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":self.token
                    },
                )

            self.assertEqual(response.status_code, 200)

    def test_delete_did(self):
        id = 5
        with app.test_client() as client:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                response = client.delete(
                    f'/dids/{id}',
                    headers={
                        "Content-Type": "application/json",
                        "x-access-tokens":self.token
                    },
                )

            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
