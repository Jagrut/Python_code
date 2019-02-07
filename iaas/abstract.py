import urllib3
import importlib
import logging

from common.constants import ABSTRACT_CLASS_DETAILS
from common.functions import get_config

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class IAASManager():
    """
    Abstract Class for PlatformA and PlatformB apis.
    """
    API_CONFIG_PATH = "iaas/api_config.yaml"
    CLASS_NAME = "_CLASS_NAME"
    CLASS_PATH = "_CLASS_PATH"

    def __iaas_manager_factory_method__(self, class_name):
        """
        Factory Method for abstract class, which will dynamically load modules and
        create's instance of that module class.

        Args:
            class_name(string): Name of subclass for factory method.
        Return:
            object: Output will be instance of class as factory method.
        """
        key_class_name = class_name.upper()+self.CLASS_NAME
        key_class_path = class_name.upper()+self.CLASS_PATH

        if key_class_path not in ABSTRACT_CLASS_DETAILS \
           or key_class_name not in ABSTRACT_CLASS_DETAILS:

            message = "Class - '{}' details are not updated in constants file.".format(class_name)
            logger.critical(message)
            raise Exception(message)

        module = importlib.import_module(ABSTRACT_CLASS_DETAILS[key_class_path])

        if ABSTRACT_CLASS_DETAILS[key_class_name] in dir(module):
            api_class = getattr(module, ABSTRACT_CLASS_DETAILS[key_class_name])
            obj = api_class()
            return obj
        else:
            message = "This Class - '{}' is not defined.".format(ABSTRACT_CLASS_DETAILS[key_class_name])
            logger.critical(message)
            raise Exception(message)

    def __find_class_name_by_method__(self, method_name):
        """
        This method will Map factory method's to respective subclasses.

        Args:
            method_name(string): Name of the factory method.

        Return:
            string: Output will be Class name for the factory method.
        """
        class_name = get_config('API', method_name, self.API_CONFIG_PATH)
        return class_name

    def call(self, method_name, kw=None):
        """
        Executor method will execute factory methods by mapping subclass.

        Args:
            method_name(string): Name of the factory method.
            kw(dictionary)(optional): Input data to the factory method.

        Return:
            Output will be returned as per factory method's output.
        """
        try:
            if method_name == "" or method_name is None:
                message = "Argument method_name cannot be empty or None."
                error_message = {'status': False}
                error_message['comment'] = message
                return error_message
            method_class_name = self.__find_class_name_by_method__(method_name)
            class_instance = self.__iaas_manager_factory_method__(method_class_name)
            if method_name in dir(class_instance):
                return getattr(class_instance, method_name)(parameters=kw)
            else:
                message = "Method '{}' not defined in this '{}' class."\
                          .format(method_name, class_instance.__class__.__name__)
                logger.critical(message)
                error_message = {'status': False}
                error_message['comment'] = message
                return error_message
        except KeyError as e:
            message = "Missing key: {}".format(e)
            logger.critical(message)
            raise KeyError(message)
        except Exception as ex:
            message = "Exception: An exception occured: {}".format(ex)
            logger.critical(message)
            raise Exception(message)
