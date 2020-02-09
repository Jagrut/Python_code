import unittest
from mock import MagicMock
from mock import patch
from iaas.platforma import PlatformAManager

def mock_get_config(key, attribute):
    data_dict = {"github": {"url": "https://example.com",
                            "username": "test",
                            "password": "password",
                            "api_version": "v3"},
                 "platforma": {"host": "https://platforma.example.com",
                               "username": "test",
                               "password": "Password1",
                               "api_version": "v1.3"}
                 }

    return data_dict[key][attribute]

class TestPlatformA(unittest.TestCase):

    def test_init(self):
        self.platforma = PlatformAManager("test", "password", "test@hostname", "v1.3")
        self.assertEqual(self.platforma.password, "password")

    @patch('iaas.platforma.get_config')
    @patch('iaas.platforma.Utils')
    def test_authentication(self, utils_mock, config_mock):
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = {"Token": "dwddwf"}
        utils_mock.post_JSON.return_value = response_instance

        config_mock.side_effect = mock_get_config

        self.platforma = PlatformAManager()
        result = self.platforma.authenticate(parameters={})
        self.assertEqual(result, 200)

    @patch('iaas.platforma.PlatformAManager.authenticate')
    @patch('iaas.platforma.get_config')
    def test_get_tenant_id(self, config_mock, authenticate_mock):
        authenticate_mock.return_value = 200
        response_instance = MagicMock()
        response_instance.status_code = 200

        config_mock.side_effect = mock_get_config

        self.platforma = PlatformAManager()
        self.platforma.tenant_id = MagicMock()
        self.platforma.tenant_id = '9f92203e-313c-4b35-88ff-ff00a9d77153'
        tenan_id = self.platforma.get_tenant_id(parameters={})
        self.assertEqual(tenan_id, '9f92203e-313c-4b35-88ff-ff00a9d77153')

    @patch('iaas.platforma.PlatformAManager.authenticate')
    @patch('iaas.platforma.get_config')
    def test_get_tenant_id_none(self, config_mock, authenticate_mock):
        authenticate_mock.return_value = 400
        config_mock.side_effect = mock_get_config

        self.platforma = PlatformAManager()
        self.platforma.tenant_id = MagicMock()
        tenan_id = self.platforma.get_tenant_id(parameters={})
        self.assertIs(tenan_id, None)

    @patch('iaas.platforma.get_config')
    @patch('iaas.platforma.PlatformAManager.authenticate')
    @patch('iaas.platforma.Utils')
    def test_get_task_status(self, utils_mock, authenticate_mock, config_mock):
        # Mocking self.authenticate() method
        authenticate_mock.return_value = 200
        config_mock.side_effect = mock_get_config
        response_instance = MagicMock()
        response_instance.status_code = 200
        return_data = {'ManagedResourceID': '9f92203e-313c-4b35-88ff-ff00a9d77153',
                       'ParentTaskId': None,
                       'TenantID': '9f92203e-313c-4b35-88ff-ff00a9d77153',
                       'CreatedDate': '2018-06-22T05:28:19.777Z',
                       'SessionID': None, 'EditedBy': 'test@hostname',
                       'PortalUserName': 'test@hostname', 'MessageName': 'SetVM',
                       'TaskInfoID': 'c22135d9-5931-4aff-8462-e6601c5b573b',
                       'LocalizableError': None, 'CreatedBy': 'test@hostname',
                       'ManagedResourceName': 'qqqqqq',
                       'Errors': None, 'TaskName': 'Provisioning VM qqqqqq', 'Progress': 1,
                       'Cancellable': False, 'StateMessage': 'Success',
                       'StartTime': '2018-06-22T05:28:19.777Z',
                       'CorrelationId': 'c22135d9-5931-4aff-8462-e6601c5b573b',
                       'Result': None, 'EditedDate': '2018-06-22T05:28:20.919Z',
                       'ManagedResourceIdentifier': None,
                       'ManagedResourceType': 'Tenant', 'CustomerId': 0,
                       'TaskId': 'c22135d9-5931-4aff-8462-e6601c5b573b',
                       'SiteID': '69d29e4b-ce66-66b9-a07d-c4612616bb0f',
                       'FinishTime': None, 'HypervisorID': None, 'UserName': 'test@hostname',
                       'Acl': [{'ResourceRole': '3f9d5bf4-0f63-4ede-8a31-f832af8dc07b',
                                'UserGroup': '77922643-80cb-7eb5-d6ca-6c21327b6d11', 'Permissions': 1},
                               {'ResourceRole': '3985741b-0df2-4e9a-869b-46369842b0da',
                                'UserGroup': 'b742a2b9-2063-f1b0-b831-40aa5d39234e', 'Permissions': 1},
                               {'ResourceRole': '3f9d5bf4-0f63-4ede-8a31-f832af8dc07b',
                                'UserGroup': '84e201ba-a318-46a9-abec-65c801d76477', 'Permissions': 1},
                               {'ResourceRole': '3f9d5bf4-0f63-4ede-8a31-f832af8dc07b',
                                'UserGroup': '2819972e-7be9-4d7c-a809-cd1c6a1baf86', 'Permissions': 1}],
                       'State': 3
                       }

        match_data = {'vm_id': None, 'state': 'Success'}
        response_instance.json.return_value = return_data
        utils_mock.make_get_request.return_value = response_instance

        self.platforma = PlatformAManager()
        with patch('iaas.platforma.sleep'):
            parameter_dict = {"message_id": "123s-3fs32-svseves-43sefsef"}
            msg_info = self.platforma.get_task_status(parameters=parameter_dict)
            self.assertEqual(msg_info, match_data)
