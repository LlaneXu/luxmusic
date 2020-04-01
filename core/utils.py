# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/19 20:03
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : utils.py

Description:

Update:

Todo:


"""
# system import
import os
import shutil
import json
import sys
import logging
from django.db.models.fields.related import ForeignKey
# 3rd import

# self import

# module level variables here


def attr_to_dict(instance, keys=None, json_keys=None, foreign_keys=None, many2many_keys=None):
    """
    translate attr of a instance into a dict
    :param instance:
    :param keys:
    :param json_keys:
    :param foreign_keys:
    :param many2many_keys:
    :return:
    """
    ret = {}
    # get the information in instance._meta
    instance_keys = []
    instance_foreign_keys = []
    for field in instance._meta.fields:
        if type(field) is ForeignKey:
            instance_foreign_keys.append(field.name)
        else:
            instance_keys.append(field.name)
    instance_many2many_name = [field.name for field in instance._meta.many_to_many]

    # priority sequence:
    # params > attributes in defines > default
    if keys:
        pass
    elif hasattr(instance, "keys"):
        keys = instance.keys
    else:
        keys = instance_keys

    if json_keys:
        pass
    elif hasattr(instance, "json_keys"):
        json_keys = instance.json_keys
    else:
        json_keys = ()

    if foreign_keys:
        pass
    elif hasattr(instance, "foreign_keys"):
        foreign_keys = instance.foreign_keys
    else:
        foreign_keys = instance_foreign_keys

    if many2many_keys:
        pass
    elif hasattr(object, "many2many_keys"):
        many2many_keys = instance.many2many_keys
    else:
        many2many_keys = instance_many2many_name

    for key in keys:
        value = getattr(instance, key)
        if key == "uuid":
            ret[key] = value.hex
        else:
            ret[key] = value
    for key in json_keys:
        try:
            ret[key] = json.loads(getattr(instance, key))
        except json.JSONDecodeError:
            import traceback
            traceback.print_exc()
            pass
    for key in foreign_keys:
        value = getattr(instance, key)
        if value:
            ret[key] = value.to_dict()
        else:
            ret[key] = {}
    for key in many2many_keys:
        ret[key] = [item.to_dict() for item in getattr(instance, key).all()]
    return ret

def camelize(dash):
    """
    convert 'this_is_an_example' into 'thisIsAnExample'
    Args:
        dash:

    Returns:

    """
    words = dash.split('_')
    capital_words = [words[0]]
    for word in words[1:]:
        capital_words.append(word.capitalize())
    return ''.join(capital_words)


def json_camelize(data):
    """
    convert a json with dash version key into lower camel key.
    support iterate
    Examples:
        { "this_key": 1}
        into
        {"thisKey": 1}

    Args:
        data:

    Returns:

    """
    if not isinstance(data, dict):
        return data

    ret = {}
    for key in data:
        if isinstance(data[key], dict):
            ret[camelize(key)] = json_camelize(data[key])
        elif isinstance(data[key], list):
            temp_list = []
            for item in data[key]:
                temp_list.append(json_camelize(item))
            ret[camelize(key)] = temp_list
        else:
            ret[camelize(key)] = data[key]
    return ret


def invert_camelize(camel):
    """
    convert camel style to underline style
    Examples:
        "thisIsAnExample" to "this_is_an_example"
    can also support the style with the first upper letter.
        "ThisIs" to "this_is"
    Args:
        camel:

    Returns:

    """
    ret = camel[0] if camel[0].islower() else camel[0].lower()

    for ch in camel[1:]:
        ret += ch if ch.islower() else '_' + ch.lower()
    return ret


def queryset_to_js(instance, keys=None, json_keys=None, object_keys=None):
    ret = attr_to_dict(instance, keys,json_keys, object_keys)
    return json_camelize(ret)


def map_json(data, key_map):
    """
    translate srcKey into destKey of a json
    :param data:
    :param map: ((src_key, dest_key),)
    :return:
    """
    for (src_key, dest_key) in key_map:
        data[dest_key] = data[src_key]
        del data[src_key]
    return data

def init_logging():
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.pop()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formater = logging.Formatter(
        fmt="%(asctime)s [%(name)s] %(lineno)d %(levelname)s: %(message)s",
        datefmt="%Y-%M-%d %H:%M:%S"
    )
    handler.setFormatter(formater)
    logger.addHandler(handler)
    # logging.basicConfig(
    #     stream=sys.stdout,
    #     format="%(asctime)s %(name)s %(lineno)d %(levelname)s: %(message)s",
    #     level=logging.INFO,
    #     datefmt="%Y-%M-%d %H:%M:%S"
    # )
    # pass


def copy(src, dst):
    """
    including creating folder
    :param src:
    :param dst:
    :return:
    """
    parent = os.path.split(dst)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)
    shutil.copy(src, dst)
