import unittest
from mock import MagicMock
from mock import patch

from iaas.platformb_entitya import EntityA
from iaas.platformb import PlatformBManager

def mock_get_config(key, attribute):
    data_dict = {"platformb": {"platformburl": "dummy.url",
                               "platformbresourceserverclientid": "b55af4d5c085",
                               "platformbresourceserversecret": "c0lj",
                               "platformbcorrugateclientcolonsecret": "e:trnw0bfpg",
                               "platformbcorrugatesecret": "trjlpyg",
                               "platformbcorrugateclient": "83d6e370abce",
                               "platformbhypervisorid": "-e6fa72d11353",
                               "platformbcluster": "p21se01",
                               "platformbbrickhousetier": "amd",
                               "platformbnetcidr": "cidr/26",
                               "platformbgatewayip": "gateway",
                               "platformbtenantrid": "test"},
                 "deadbolt": {"username": "test",
                              "password": "test"}
                 }

    return data_dict[key][attribute]

class xyz:
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

class TestTenant(unittest.TestCase):

    @patch('iaas.platformb.get_config')
    def setUp(self, config_mock):
        config_mock.side_effect = mock_get_config
        self.platformb = PlatformBManager()
        self.entitya = EntityA("dwl1", self.platformb)

    @patch('iaas.utils.Utils.post_JSON')
    def test_create(self, post_json_mock):
        response_instance = MagicMock()
        response_instance.json.return_value = {"status_code": 200,
                                               "id": "dkwoj"}
        post_json_mock.return_value = response_instance
        result = self.entitya.create("tenat_name")
        self.assertEqual(result, None)

    @patch('iaas.utils.Utils.post_JSON')
    def test_create_group(self, post_json_mock):
        response_instance = MagicMock()
        response_instance.json.return_value = {"status_code": 200,
                                               "id": "dkwoj"}
        post_json_mock.return_value = response_instance
        result = self.entitya.create_group("gr_name")
        self.assertEqual(result, None)

        # Without group name.
        result = self.entitya.create_group()
        self.assertEqual(result, None)

    @patch('iaas.utils.Utils.post_JSON')
    def test_create_user(self, post_json_mock):
        post_json_mock().text = "text"
        result = self.entitya.create_user("password", "groupid")
        self.assertEqual(result, None)

    def test_import_rpc(self):
        self.entitya.import_rpc(xyz("id", b"secret"))
