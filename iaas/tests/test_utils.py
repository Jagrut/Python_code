import unittest
from mock import MagicMock
from mock import patch

from iaas.utils import Utils

class TestUtils(unittest.TestCase):
    @patch('iaas.utils.base64')
    def test_get_b64_colon_secret(self, b64):
        b64.b64encode.return_value = "encoded"
        result = Utils.get_b64_colon_secret("1", "we")
        self.assertEqual(result, "encoded")

    def test_result_success(self):
        result = Utils.result_success(201)
        self.assertEqual(result, True)

        result = Utils.result_success(401)
        self.assertEqual(result, False)

    def test_result_redirect(self):
        result = Utils.result_redirect(300)
        self.assertEqual(result, True)

        result = Utils.result_redirect(401)
        self.assertEqual(result, False)

    @patch('iaas.utils.requests')
    def test_make_get_request(self, request_mock):
        response_instance = MagicMock()
        response_instance.status_code = 200
        request_mock.get.return_value = response_instance

        result = Utils.make_get_request("example.com")
        self.assertEqual(result.status_code, 200)

    @patch('iaas.utils.requests')
    def test_make_post_request(self, request_mock):
        response_instance = MagicMock()
        response_instance.status_code = 200
        request_mock.post.return_value = response_instance
        result = Utils.make_post_request("example.com", json_data={"name": "xyz"})

        self.assertEqual(result.status_code, 200)

    @patch('iaas.utils.Utils.make_post_request')
    def test_post_JSON(self, make_post_request_mock):
        response_instance = MagicMock()
        response_instance.status_code = 200
        make_post_request_mock.return_value = response_instance
        result = Utils.post_JSON("example.com", {"name": "xyz"}, {"name": "abc"}, "task")
        self.assertEqual(result.status_code, 200)

    @patch('iaas.utils.Utils.make_post_request')
    def test_post_form(self, make_post_request_mock):
        response_instance = MagicMock()
        response_instance.status_code = 200
        make_post_request_mock.return_value = response_instance
        result = Utils.post_form("example.com", {"name": "xyz"}, {"name": "abc"}, "task")
        self.assertEqual(result.status_code, 200)
