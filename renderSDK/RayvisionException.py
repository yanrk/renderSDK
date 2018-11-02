#!/usr/bin/env python
# -*- coding:utf-8 -*-

class RayvisionError(Exception):
    """
    raise RayvisionError if something wrong.
    """
    def __init__(self, error_code, error, *args, **kwargs):
        super(RayvisionError, self).__init__(self, error)
        self.error_code = error_code
        self.error = error

    def __str__(self):
        return 'RayvisionError: {0}: {1}'.format(self.error_code, self.error)

    __repr__ = __str__


class APIError(RayvisionError):
    """
    raise APIError if receiving json message indicating failure.(return_code!=200)
    """
    def __init__(self, error_code, error, request):
        super(APIError, self).__init__(self, error)
        self.error_code = error_code
        self.error = error
        self.request = request

    def __str__(self):
        return 'APIError: {0}: {1}, request: {2}'.format(self.error_code, self.error, self.request)

    __repr__ = __str__


if __name__ == '__main__':
    raise APIError(400, "bad request", 'task.renderbus.com')
    