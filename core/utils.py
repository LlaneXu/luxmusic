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
import json
# 3rd import

# self import

# module level variables here


def attr_to_dict(instance, keys=None, json_keys=None, object_keys=None):
    """
    translate attr of a instance into a dict
    :param instance:
    :param keys:
    :param json_keys:
    :param object_keys:
    :return:
    """
    ret = {}
    keys = keys if keys else instance.keys if hasattr(instance, "keys") else ()
    json_keys = json_keys if json_keys else (instance.json_keys if hasattr(instance, "json_keys") else ())
    object_keys = object_keys if object_keys else (instance.object_keys if hasattr(instance, "object_keys") else ())

    for key in keys:
        ret[key] = getattr(instance, key)
    for key in json_keys:
        try:
            ret[key] = json.loads(getattr(instance, key))
        except json.JSONDecodeError:
            import traceback
            traceback.print_exc()
            pass
    for key in object_keys:
        ret[key] = getattr(instance, key).to_dict()
    return ret


