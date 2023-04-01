import hashlib

from rocketchat_API.rocketchat import RocketChat


class RocketChatApi(RocketChat):
    def __init__(self, user=None, password=None, auth_token=None, user_id=None, server_url='http://127.0.0.1:3000',
                 ssl_verify=True, proxies=None, timeout=30, session=None, client_certs=None):
        """Creates a RocketChat object and does login on the specified server"""
        super().__init__(user, password, auth_token, user_id, server_url, ssl_verify, proxies, timeout, session,
                         client_certs)

        if password:
            self.headers['X-2fa-code'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
            self.headers['X-2fa-method'] = 'password'
