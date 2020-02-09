import unittest
from mock import patch

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
                              "password": "test"
                              }
                 }
    return data_dict[key][attribute]

class TestCHPAPIManager(unittest.TestCase):

    @patch('iaas.platformb.get_config')
    def test_create_tenant(self, get_config_mock):
        get_config_mock.side_effect = mock_get_config

        platformb = PlatformBManager()
        kw_arg_1 = {"entitya_name": "tenant_name",
                    "user_pass": "user_pass"}
        tenant = platformb.create_entitya(parameters=kw_arg_1)
        self.assertEqual(tenant, None)

        self.assertRaises(ValueError, lambda: platformb.create_entitya(parameters=None))

        kw_arg_2 = {"tenant_name": "tenant_name"}
        self.assertRaises(ValueError, lambda: platformb.create_entitya(parameters=kw_arg_2))

        kw_arg_3 = {"user_pass": "user_pass"}
        self.assertRaises(ValueError, lambda: platformb.create_entitya(parameters=kw_arg_3))

    @patch('iaas.platformb.get_config')
    def test_authentication(self, config_mock):
        config_mock.side_effect = mock_get_config
        self.platformb = PlatformBManager()
        self.assertRaises(NotImplementedError, lambda: self.platformb.authenticate(parameters={}))
