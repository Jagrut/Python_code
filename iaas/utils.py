import base64
import logging
import requests
from common.exceptions import APIException
logger = logging.getLogger(__name__)

class Utils(object):
    """ Utility class. """

    @staticmethod
    def get_b64_colon_secret(id, secret):
        """
        Generate a base64 encoded colon secret, which is 'id:secret'
        :param id: id as a string.
        :param secret: secret as a string.
        :return: encoded bytes.
        """

        colon_secret = '{}:{}'.format(id, secret)
        encoded = base64.b64encode(bytes(colon_secret, 'utf-8'))
        return encoded

    @staticmethod
    def result_success(result):
        """
        Check if HTTP result code is in the 2xx range.
        :param result: status code.
        :return: Boolean True or False.
        """

        if 200 <= result < 300:
            return True

        return False

    @staticmethod
    def result_redirect(result):
        """
        Check if HTTP result code is in the 3xx range, for redirects.
        :param result: status code.
        :return: Boolean True or False.
        """

        if 300 <= result < 400:
            return True

        return False

    @staticmethod
    def post_form(url, headers, payload, doing):
        """
        Post form data, which will be encoded as application/x-www-form-urlencoded
        :param url: url to make a post request.
        :param headers: request headers.
        :param payload: data.
        :param doing: task.
        :return: response object.
        """

        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return Utils.make_post_request(url, headers=headers, doing=doing, data=payload)

    @staticmethod
    def post_JSON(url, headers, payload, doing):
        """
        Post data as JSON
        :param url: url to make a post request.
        :param headers: request headers.
        :param payload: data.
        :param doing: task.
        :return: response object.
        """

        headers['Content-Type'] = 'application/json'

        return Utils.make_post_request(url,
                                       headers=headers,
                                       doing=doing,
                                       json_data=payload)

    @staticmethod
    def make_post_request(url, headers=None, doing='', json_data=None, data=None):
        """
        Make a POST request to a given url. This takes either JSON, raw
        form data.
        :param url: url to make a post request.
        :param headers: request headers.
        :param doing: task.
        :param json_data: json post request data.
        :param data: form post request data.
        :return: response object.
        :except: api error.
        """

        if not headers:
            headers = {}

        logger.debug('SEND url    : {}'.format(url))
        logger.debug('SEND headers: {}'.format(headers))

        if json_data:
            logger.debug('SEND json   : {}'.format(json_data))
            resp = requests.post(url, verify=False, headers=headers, json=json_data)
        elif data:
            logger.debug('SEND data   : {}'.format(data))
            resp = requests.post(url, verify=False, headers=headers, data=data)

        recv_text = resp.text
        logger.debug('RECV status : {}'.format(resp.status_code))
        logger.debug('RECV headers: {}'.format(resp.headers))
        logger.debug('RECV text   : {}'.format(recv_text))
        logger.debug('RECV resp   : {}'.format(resp))

        if Utils.result_success(resp.status_code):
            return resp
        else:
            err_msg = 'ERROR, received {} code while {}'.format(resp.status_code, doing)
            raise APIException(err_msg)

    @staticmethod
    def make_get_request(url, headers=None, doing=''):
        """
        Make a GET request to a given url.
        :param url: url to make a post request.
        :param headers: request headers.
        :param doing: task.
        :return: response object.
        :except: api error.
        """

        if not headers:
            headers = {}

        logger.debug('SEND url    : {}'.format(url))
        logger.debug('SEND headers: {}'.format(headers))

        resp = requests.get(url, verify=False, headers=headers)
        recv_text = resp.text

        logger.debug('RECV status : {}'.format(resp.status_code))
        logger.debug('RECV headers: {}'.format(resp.headers))
        logger.debug('RECV text   : {}'.format(recv_text))
        logger.debug('RECV resp   : {}'.format(resp))

        if Utils.result_success(resp.status_code):
            return resp
        else:
            err_msg = 'ERROR, received {} code while {}'.format(resp.status_code, doing)
            raise APIException(err_msg)
