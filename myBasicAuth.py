from dash_auth.auth import Auth
import base64
import flask
import hashlib
import base64
from dash_auth.basic_auth import BasicAuth


class MyBasicAuth(BasicAuth):

    def is_authorized(self):
        header = flask.request.headers.get('Authorization', None)
        if not header:
            return False
        username_password = base64.b64decode(header.split('Basic ')[1])
        username_password_utf8 = username_password.decode('utf-8')
        username, password = username_password_utf8.split(':', 1)
        return self._users.get(username) == hashlib.sha256(password.encode()).hexdigest().upper()
