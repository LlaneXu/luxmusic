# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/19 18:39
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : response.py

Description:

Update:

Todo:


"""
# system import
import json
import logging
import traceback

# 3rd import
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

# self import

# module level variables here
# 第三方库
# 自有库


class ResponseException(Exception):
    """
    Exception class for triggering HTTP 4XX responses with JSON content, where expected.
    """
    status_code = 400

    def __init__(self, message=None, status=None, *args, **kwargs):
        if status is not None:
            self.status_code = status
        print(kwargs)
        super(ResponseException, self).__init__(message, *args, **kwargs)


class Response(object):
    json_content_type = 'application/json;charset=UTF-8'

    def get(self, request, json_data, *args, **kwargs):
        raise ResponseException('get not allowed', 405)

    def post(self, request, json_data, *args, **kwargs):
        raise ResponseException('post not allowed', 405)

    def put(self, request, json_data, *args, **kwargs):
        raise ResponseException('put not allowed', 405)

    def patch(self, request, json_data, *args, **kwargs):
        raise ResponseException('patch not allowed', 405)

    def delete(self, request, json_data, *args, **kwargs):
        raise ResponseException('delete not allowed', 405)

    def json_response(self, response_data, status=200):
        if settings.DEBUG:
            out_data = json.dumps(response_data, ensure_ascii=False, indent=4,
                                  cls=DjangoJSONEncoder)
        else:
            out_data = json.dumps(response_data, ensure_ascii=False, cls=DjangoJSONEncoder)
        response = HttpResponse(out_data, self.json_content_type, status=status)
        response['Cache-Control'] = 'no-cache'
        return response

    def __call__(self, request, *args, **kwargs):
        try:
            in_data = json.loads(request.body.decode('utf-8'))
        except ValueError:
            in_data = request.body.decode('utf-8')

        self.request = request
        handler = getattr(self, request.method.lower())
        status_code = 200
        try:
            response_data = {
                "data": handler(request, in_data, *args, **kwargs),
                "message": "",
                "code": 0,
            }
        except ResponseException as e:
            response_data = {'message': e.args[0], 'code': -1}
            status_code = e.status_code
        except Exception as e:
            response_data = {'message': '%s' % e, 'code': -1}
            traceback.print_exc()
            status_code = 500
        return self.json_response(response_data, status_code)


