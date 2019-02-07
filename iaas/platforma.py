from iaas.utils import Utils
import logging
from rest_framework import status

from time import sleep

from common.functions import get_config
from common.constants import KEY_PLATFORMA, WAIT_TIME_BETWEEN_REQUESTS

logger = logging.getLogger(__name__)

class PlatformAManager():
    """
    Class to connect with PlatformA and perform various operations on PlatformA
    """

    def __init__(self, login=None, password=None, host=None, api_version=None):
        if login is None:
            self.login = get_config(KEY_PLATFORMA, "username")
        else:
            self.login = login

        if password is None:
            self.password = get_config(KEY_PLATFORMA, "password")
        else:
            self.password = password

        if host is None:
            self.host = get_config(KEY_PLATFORMA, "host")
        else:
            self.host = host

        if api_version is None:
            self.api_version = get_config(KEY_PLATFORMA, "api_version")
        else:
            self.api_version = api_version

        self.request_header = {}
        self.XTM_TOKEN = None
        self.tenant_id = None

    def url(self, api_name):
        """
        Create's standard url for the api name.

        Args:
            api_name (string): Name of the api callable on PlatformA.

        Returns:
            string: Ouput will a url with hostname  and api name.

        """
        return "https://%s/api/%s/%s/" % (self.host, self.api_version, api_name)

    def authenticate(self, **kwargs):
        """
        Authenticate against PlatformA.

        Returns:
            integer: Status code

        """
        try:
            response = Utils.post_JSON(self.url("auth"), headers={},
                                       payload={"username": self.login, "password": self.password},
                                       doing="Authenticating on Platforma")

            self.XTM_TOKEN = response.json().get('Token', None)
            user_info = response.json().get('User', None)
            if user_info:
                self.tenant_id = user_info.get('TenantID', None)

            self.request_header["Authorization"] = 'Bearer %s' % self.XTM_TOKEN
            return response.status_code
        except Exception as e:
            message = "Some unknown exception occurs - {}".format(e)
            logging.debug(message)
            return status.HTTP_417_EXPECTATION_FAILED

    def get_tenant_id(self, **kwargs):
        """
        Fetch tenant id of the PlatformA.

        Returns:
            string: Tenant id

        """
        if self.authenticate() == 200:
            return self.tenant_id
        else:
            return None

    def get_task_status(self, **kwargs):
        """
        Gets the request status using TaskInfo API

        Args:
            message_id (string): Request message id for the task.

        Returns:
            string: Returns status "Success" or "Failure"

        """
        if kwargs is None or kwargs['parameters'] is None:
            message = "For 'get_task_status' method parameters are not parsed."
            logger.critical(message)
            raise ValueError(message)

        if "message_id" not in kwargs['parameters']:
            message = "Key 'message_id' not in kwargs."
            logger.critical(message)
            raise ValueError(message)

        message_id = kwargs['parameters']['message_id']

        return_data = {"state": "Error"}
        auth = self.authenticate()
        if auth == 200:
            task_completed = False
            state_message = "Queued"
            while not task_completed:
                sleep(WAIT_TIME_BETWEEN_REQUESTS)
                response = Utils.make_get_request(self.url("TaskInfo" + "/" + str(message_id)),
                                                  headers=self.request_header, verify=False)
                if 'StateMessage' in response.json():
                    state_message = response.json()['StateMessage']
                if state_message == "Success" or state_message == "Error":
                    task_completed = True
                    return_data["state"] = state_message
                    if state_message == "Success":
                        return_data["vm_id"] = response.json()['Result']
        else:
            message = "unable to authenticate to the PlatformA server," \
                      " got the below response from server {}".format(auth)
            logging.debug(message)
            raise Exception(message)

        return return_data
