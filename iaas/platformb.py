from iaas.utils import Utils
from common.functions import get_config
from common.constants import KEY_PLATFORMB
import logging

logger = logging.getLogger(__name__)

class PlatformBManager():

    def __init__(self, platformburl=None, platformbresourceserverclientid=None,
                 platformbresourceserversecret=None,
                 platformbcorrugateclientcolonsecret=None,
                 platformbcorrugateclient=None,
                 platformbhypervisorid=None,
                 platformbcorrugatesecret=None):
        """
        :param platformburl: apiurl.
        :param platformbresourceserverclientid: resourceserverclientid.
        :param platformbresourceserversecret: resourceserversecret.
        :param platformbcorrugateclientcolonsecret: corrugateclientcolonsecret.
        :param platformbcorrugateclient: corrugateclient.
        :param platformbhypervisorid: hypervisorid.
        :param platformbcorrugatesecret: corrugatesecret.
        """
        try:
            self.url_base = platformburl
            self.resource_server_clientid = platformbresourceserverclientid
            self.resource_server_secret = platformbresourceserversecret
            self.corrugate_client = platformbcorrugateclient
            self.corrugate_secret = platformbcorrugatesecret
            self.hypervisor_id = platformbhypervisorid

            if not platformburl:
                self.url_base = '{}'.format(get_config(KEY_PLATFORMB, "platformburl"))

            self.servicea_url = 'https://kratos.{}'.format(self.url_base)

            if not platformbresourceserverclientid:
                rsc = get_config(KEY_PLATFORMB, "platformbresourceserverclientid")
                self.resource_server_clientid = '{}'.format(rsc)

            if not platformbresourceserversecret:
                rss = get_config(KEY_PLATFORMB, "platformbresourceserversecret")
                self.resource_server_secret = '{}'.format(rss)

            # resource_server_colon_secret_b64 as rscs
            rscs = Utils.get_b64_colon_secret(self.resource_server_clientid,
                                              self.resource_server_secret)

            self.resource_server_colon_secret_b64 = rscs
            if not platformbcorrugateclient:
                self.corrugate_client = '{}'.format(get_config(KEY_PLATFORMB, "platformbcorrugateclient"))
            if not platformbcorrugatesecret:
                self.corrugate_secret = '{}'.format(get_config(KEY_PLATFORMB, "platformbcorrugatesecret"))

            # corrugate_colon_secret_b64 as ccs.
            ccs = Utils.get_b64_colon_secret(self.corrugate_client,
                                             self.corrugate_secret)
            self.corrugate_colon_secret_b64 = ccs
            if not platformbhypervisorid:
                self.hypervisor_id = '{}'.format(get_config(KEY_PLATFORMB, "platformbhypervisorid"))
        except KeyError as e:
            message = 'Required  variable {} missing'.format(e)
            logger.critical(message)
            raise KeyError(message)

    def authenticate(self, **kwargs):
        raise NotImplementedError("To be implemented")

    def create_entitya(self, **kwargs):
        """
        Create a entitya in data center.
        :param entitya_name: entitya_name.
        :param user_pass: user_pass.
        :param group_name: group_name.
        """
        if kwargs is None or kwargs['parameters'] is None:
            message = "'create_entitya' method expects parameters as a key-value form."
            logger.critical(message)
            raise ValueError(message)

        if "entitya_name" not in kwargs['parameters']:
            message = "Key 'entitya_name' not in kwargs."
            logger.critical(message)
            raise ValueError(message)

        if "user_pass" not in kwargs['parameters']:
            message = "Key 'user_pass' not in kwargs."
            logger.critical(message)
            raise ValueError(message)

        group_name = kwargs['parameters'].get('group_name', None)

        tenant_name = kwargs['parameters']['entitya_name']
        user_pass = kwargs['parameters']['user_pass']
        logger.info("group_name: {}".format(group_name))
        logger.info("tenant_name: {}".format(tenant_name))
        logger.info("user_pass: {}".format(user_pass))
        # User other services to create entitya.
        pass
