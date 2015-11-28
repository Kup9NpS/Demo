import json
import traceback
import base64
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, obj, ensure_ascii=True):
        super(JsonResponse, self).__init__(json.dumps(obj, ensure_ascii=ensure_ascii), content_type='application/json')


def dumps(obj):
    return JsonResponse(obj, ensure_ascii=False)


def response(obj):
    return dumps({'response': obj})


def error(obj):
    return dumps({'error': obj})


class Error(Exception):
    def __init__(self, error_code, error_description, e=None, data=None):
        self.error_code = error_code
        self.error_description = error_description
        if e:
            assert isinstance(e, Exception)
        self.e = e
        if data:
            assert isinstance(data, dict)
        self.data = data
        super(Error, self).__init__(error_code, error_description)

    @staticmethod
    def unhandled(e):
        return Error(0, 'Unhandled exception', e)

    def dict(self):
        data = {'error_code': int(self.error_code), 'error_description': self.error_description}
        if self.e:
            data['error'] = {'class': self.e.__class__.__name__}
            data['error']['args'] = '{}'.format(','.join(list(map(str, self.e.args)))) if len(self.e.args) > 0 else ''
            if hasattr(self.e, '__traceback__'):
                data['error']['traceback'] = '\n'.join(
                    traceback.format_exception(self.e.__class__, self.e, self.e.__traceback__))
                data['error']['traceback'] = base64.b64encode(data['error']['traceback']).decode()
        if self.data:
            data['data'] = self.data
        return data


def handle_error_decor(func):
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if isinstance(resp, HttpResponse):
                return resp
            return response(resp)
        except Error as e:
            return error(e.dict())
        except Exception as e:
            return error(Error.unhandled(e).dict())

    return wrapper