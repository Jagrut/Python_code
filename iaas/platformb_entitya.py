import logging

logger = logging.getLogger(__name__)

class EntityA(object):
    """
    Tenant.
    """

    def __init__(self, admin_access_token, platformb_obj, json_data=None):
        """
        :param admin_access_token: admin_access_token.
        :param platformb_obj: platformb object.
        :param json_data: json_data.
        """
        self.entitya_rid = None
        self.entitya_name = None
        self.entitya_domain = None
        self.entitya_id = None
        self.group_name = None
        self.group_id = None

        # Requesting Party Client values
        self.rpc_id = None
        self.rpc_secret = None

        # Requesting Party User values
        self.rpu_username = None
        self.rpu_password = None

        self.networks = []
        self.storage = []

        self.admin_access_token = admin_access_token
        self.platformb_obj = platformb_obj

    def create(self, entitya_name, entitya_domain=None):
        """
        Create the entitya via deadbolt.
        :param entitya_name: entitya_name.
        :param entitya_domain: entitya_domain.
        :return: entitya_id.
        """

        if not entitya_domain:
            entitya_domain = entitya_name

        self.entitya_name = entitya_name
        self.entitya_domain = entitya_domain

        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.admin_access_token)
        payload = {
            "name": entitya_name,
            "entitya_domain": entitya_domain}
        print(payload)
        # Some rest calls.

        return self.entitya_id

    def create_group(self, group_name=None):
        """
        Create a user group for entitya users, belonging to a particular
        resource server.
        :param group_name: group_name.
        :return: group_id.
        """

        if not group_name:
            self.group_name = 'Users for EntityA {}'.format(self.entitya_id)
        else:
            self.group_name = group_name

        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.admin_access_token)
        payload = {
            "client_id": self.platformb_obj.resource_server_clientid,
            "group_name": self.group_name}
        print(payload)
        # Some rest call.

    def create_user(self, password, group_id, first_name=None, last_name=None, email=None):
        """
        Create a user which will have access to the resources that we've
        previously had the resource server register itself to protect.
        :param password: password.
        :param group_id: group_id.
        :param first_name: first_name.
        :param last_name: last_name.
        :param email: email.
        :return: response text.
        """

        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.admin_access_token)
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "entitya_id": self.entitya_id,
            "sam_account_name": "Basic",
            "temp_password": password,
            "user_groups": [group_id]}
        print(payload)
        # Some rest call.

    def import_rpc(self, rpc):
        """
        Takes a RequestingPartyClient object, and registers the id/secret
        with the entitya.
        :param rpc: RequestingPartyClient object.
        :return:
        """

        self.rpc_id = rpc.id
        self.rpc_secret = rpc.secret
