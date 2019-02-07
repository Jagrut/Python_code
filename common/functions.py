import base64
import json
import logging
import os
import yaml


from os.path import join
from common.constants import CONFIG_FILE_PATH
COMMON_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def decode_base64_string(encoded_data):
    """Decode the data
    :param encoded_data: Encoded data input
    :return: Decoded string
    """
    return str(base64.b64decode(encoded_data), 'utf-8')


def decode_base64_json(encoded_data):
    """Decode the Json data
    :param encoded_data: Encoded data input
    :return: Decoded json output
    """
    return json.loads(str(base64.b64decode(encoded_data), 'utf-8'))


def get_config(appliance, param, yaml_file_path=join(COMMON_BASE_DIR, CONFIG_FILE_PATH)):
    """This function gives the yaml value corresponding to the parameter
    sample Yaml file
        platforma_details:
            xtm_host: 10.100.26.90
    :param appliance: The header name as mentioned in the yaml file (ex:platforma_details)
    :param param: The parameter name who's value is to be determined (ex: xtm_host)
    :param yaml_file_path: Path of yaml file, Default will the config.yaml file
    :return: value corresponding to the parameter in yaml file
    :except: Exception while opening or loading the file
    """
    with open(yaml_file_path, 'r') as f:
        doc = yaml.load(f)
    param_value = doc[appliance][param]
    if param_value == "":
        message = 'Value is not updated for the parameter:{} in the yaml config file'\
            .format(param)
        raise ValueError(message)
    return param_value

