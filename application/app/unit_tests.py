import unittest
import warnings
import json
from werkzeug.security import generate_password_hash
import uuid
from base64 import b64encode

from number_api import get_dids
from settings import app


class TestAuth(unittest.TestCase):
    """
    This class tests equivalent routes to authentication
    """
    def setUp(self):
        """
        This method sets up a common variable before each test
        """
        self.credentials = b64encode(b"example:justAnExample").decode("utf8")

    def test_signup_user(self):
        """
        This method test a user sign up
        """
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
        """
        This method test a user login
        """
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
        """
        This method test a user login with empty credentials
        """
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
        """
        This method test a user login with wrong password
        """
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
        """
        This method test the users request and verifies if it's response
        has a "users" key
        """
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
        """
        This method tests the delete route and verifies if it's response
        has 200 as status, ensuring it has been removed
        """
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
    """
    This class tests equivalent routes to DID Number
    """
    def setUp(self):
        """
        This method sets up common variables before each test
        """
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
        """
        This method tests attempted tokenless request
        """
        response = self.client.get('/dids')
        message = response.json['message']

        self.assertEqual('a valid token is missing', message)

    def test_get_dids(self):
        """
        This method tests the DIDs request and verifies if it's response
        returns 200 as status
        """
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
        """
        This method tests the specific DID request and verifies if it's response
        returns 200 as status and if the id passed is equal to the response
        """
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
        """
        This method tests adding an DID number and verifies if it returns 201
        as status
        """
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
        """
        This method tests adding an DID number with negative price and verifies
        if it returns 400 as status
        """
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
        """
        This method tests adding an DID number with int value and verifies
        if it returns 201 as status
        """
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
        """
        This method tests updating an DID number and verifies
        if it returns 201 as status
        """
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
        """
        This method tests deleting an DID number by id and verifies
        if it returns 200 as status
        """
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
