# Create your tests here.
#from django.test import SimpleTestCase
import unittest
from mock import patch

from iaas.abstract import IAASManager
from iaas.tests.test_class import TestClass

TEST_ABSTRACT_CLASS_DETAILS = {
    "XSTREAM_CLASS_NAME": "TestClass",
    "XSTREAM_CLASS_PATH": "iaas.tests.test_class",
}
# This Class is completed...
class TestIAASAbstractClass(unittest.TestCase):
    def test_IAAS_abstractclass_exception(self):
        expected_output = {'comment': 'Argument method_name cannot be empty or None.',
                           'status': False}
        iaas_manager = IAASManager()
        output = iaas_manager.call(None)
        self.assertEquals(output, expected_output)

    @patch('iaas.abstract.IAASManager.__iaas_manager_factory_method__')
    @patch('iaas.abstract.IAASManager.__find_class_name_by_method__')
    def test_IAAS_call_true(self, mock_find_class_name, mock_factory_method):
        with patch('iaas.platforma.PlatformAManager') as mock:
            instance = mock.return_value
            instance.authenticate.return_value = True

        mock_factory_method.return_value = instance
        mock_find_class_name.return_value = "Xstream"

        iaas_manager = IAASManager()
        result = iaas_manager.call("authenticate")
        self.assertTrue(result)

    @patch('iaas.abstract.IAASManager.__iaas_manager_factory_method__')
    @patch('iaas.abstract.IAASManager.__find_class_name_by_method__')
    def test_call_exception(self, mock_find_class_name, mock_factory_method):
        with patch('iaas.platforma.PlatformAManager') as mock:
            instance = mock.return_value
            instance.authenticate.return_value = True

        mock_factory_method.return_value = instance
        mock_find_class_name.return_value = "Xstream"

        expected_output = {'comment': "Method 'no_method' not defined in this 'MagicMock' class.",
                           'status': False}
        iaas_manager = IAASManager()
        output = iaas_manager.call("no_method")
        self.assertEquals(output, expected_output)

    @patch('iaas.abstract.ABSTRACT_CLASS_DETAILS', TEST_ABSTRACT_CLASS_DETAILS)
    def test_iaas_manager_factory_method_true(self):
        iaas_manager = IAASManager()
        xstream_instance = iaas_manager.__iaas_manager_factory_method__("Xstream")
        self.assertIsInstance(xstream_instance, TestClass)

    def test_iaas_manager_factory_method_exception(self):
        iaas_manager = IAASManager()
        self.assertRaises(Exception, lambda: iaas_manager.__iaas_manager_factory_method__("NoClass"))

    def test_iaas_find_class_name_by_method_true(self):
        iaas_manager = IAASManager()
        self.assertEquals(iaas_manager.__find_class_name_by_method__("authenticate"), "Platforma")

    @patch('iaas.abstract.IAASManager.API_CONFIG_PATH', 'test.yaml')
    def test_iaas_find_class_name_by_method_exception(self):
        iaas_manager = IAASManager()
        self.assertRaises(Exception, lambda: iaas_manager.__find_class_name_by_method__("authenticate"))
