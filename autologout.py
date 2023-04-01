import hashlib
import logging
import traceback
from datetime import datetime, timedelta

import time

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException, \
    RocketMissingParamException

from rocketchat_API.rocketchat import RocketChat


logging.basicConfig(level=logging.DEBUG)

class RocketChatApi(RocketChat):
    def __init__(self, user=None, password=None, auth_token=None, user_id=None, server_url='http://127.0.0.1:3000',
                 ssl_verify=True, proxies=None, timeout=30, session=None, client_certs=None):
        """Creates a RocketChat object and does login on the specified server"""
        super().__init__(user, password, auth_token, user_id, server_url, ssl_verify, proxies, timeout, session,
                         client_certs)

        if password:
            self.headers['X-2fa-code'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
            self.headers['X-2fa-method'] = 'password'


def main():
    rocket = RocketChatApi('ivat', 'Pbvf94', server_url='https://rocketchat.sitetesting.fun', ssl_verify=False)

    users = rocket.users_list(type={'$in': ['user']}).json()
    for user in users["users"]:
        try:
            user_info = rocket.users_info(user["username"]).json()
        except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
            print(f"Error: {e}")
            continue

        last_login_dt = user_info['user'].get('lastLogin')
        if not last_login_dt:
            print('User has not logined yet')
            continue

        last_activity = datetime.strptime(last_login_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_time = datetime.now()
        is_admin = 'admin' in user_info['user']['roles']
        
        if not is_admin and (current_time - last_activity) >= timedelta(minutes=2):
            try:
                rocket.users_update(user_id=user['_id'], active=False)
                rocket.users_update(user_id=user['_id'], active=True)
                print(f"User {user_info['user']['username']} was logged out")
            except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
                print(f"Error: {e}")
                continue


if __name__ == '__main__':
    while True:
        try:
            print('Start the script')
            main()
            time.sleep(60)
        except Exception as e:
            print('Error: {}'.format(traceback.format_exc(e)))
            time.sleep(60)
