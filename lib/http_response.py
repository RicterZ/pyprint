__author__ = 'Ricter'
from web import HTTPError


class Created(HTTPError):
    """`201 Created`"""
    message = '{"message", "Article published success"}'

    def __init__(self):
        status = "201 Created"
        headers = {'Content-Type': 'application/json'}
        HTTPError.__init__(self, status, headers, self.message)


class NoContent(HTTPError):
    """`204 No Content`"""
    message = '{"message", "Article deleted success"}'

    def __init__(self):
        status = "204 No Content"
        headers = {'Content-Type': 'application/json'}
        HTTPError.__init__(self, status, headers, self.message)


class Unauthorized(HTTPError):
    """`401 Unauthorized` error"""
    message = '{"message": "Authentication Failed"}'

    def __init__(self):
        status = "401 Unauthorized"
        headers = {'Content-type': 'application/json'}
        HTTPError.__init__(self, status, headers, self.message)


class Forbidden(HTTPError):
    """`403 Forbidden` error"""
    message = '{"message": "Permission Denied"}'

    def __init__(self):
        status = "403 Forbidden"
        headers = {'Content-Type': 'application/json'}
        HTTPError.__init__(self, status, headers, self.message)