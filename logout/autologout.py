import os
import hashlib
import logging
import time
import traceback
from collections import namedtuple
from datetime import datetime, timedelta
from dotenv import load_dotenv

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException, \
    RocketMissingParamException

from rocketchat_API.rocketchat import RocketChat

load_dotenv()
logging.basicConfig(level=logging.INFO)

conf = namedtuple('conf', ['ROCKETCHAT_URL', 'ROCKETCHAT_USER', 'ROCKETCHAT_PASSWORD'])
conf.ROCKETCHAT_URL = os.getenv('ROCKETCHAT_URL')
conf.ROCKETCHAT_USER = os.getenv('ROCKETCHAT_USER')
conf.ROCKETCHAT_PASSWORD = os.getenv('ROCKETCHAT_PASSWORD')
conf.LOGOUT_LIMIT = int(os.getenv('LOGOUT_LIMIT', 120))
conf.SLEEP_TIME = int(os.getenv('SLEEP_TIME', 60))


class RocketChatApi(RocketChat):
    def __init__(self, user=None, password=None, auth_token=None, user_id=None, server_url='http://127.0.0.1:3000',
                 ssl_verify=True, proxies=None, timeout=30, session=None, client_certs=None):
        super().__init__(user, password, auth_token, user_id, server_url, ssl_verify, proxies, timeout, session,
                         client_certs)

        if password:
            self.headers['X-2fa-code'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
            self.headers['X-2fa-method'] = 'password'


def main():
    logging.debug('start the script')

    rocket = RocketChatApi(user=conf.ROCKETCHAT_USER,
                           password=conf.ROCKETCHAT_PASSWORD,
                           server_url=conf.ROCKETCHAT_URL,
                           ssl_verify=False)

    logging.debug('get users list')
    users = rocket.users_list(type={'$in': ['user']}).json()
    for user in users["users"]:

        logging.debug(f'try get user info: {user["username"]}')
        try:
            user_info = rocket.users_info(user["username"]).json()
        except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
            logging.error(f'ERROR: get user info: {e}')
            continue

        last_login_str = user_info['user'].get('lastLogin')
        if not last_login_str:
            logging.warning(f'user {user_info["user"]["username"]} has not logined yet')
            continue

        logging.debug(f'last {user_info["user"]["username"]} login: {last_login_str}')

        last_login_dt = datetime.strptime(last_login_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        current_time = datetime.now()
        is_admin = 'admin' in user_info['user']['roles']

        if is_admin:
            logging.warning(f'User {user_info["user"]["username"]} is admin, skip')
            continue

        if (current_time - last_login_dt) >= timedelta(seconds=conf.LOGOUT_LIMIT):
            logging.info(f'try user {user_info["user"]["username"]} logout')
            try:
                rocket.users_update(user_id=user['_id'], active=False)
                rocket.users_update(user_id=user['_id'], active=True)
                logging.info(f"User {user_info['user']['username']} was logged out")
            except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
                logging.error(f'ERROR: user {user_info["user"]["username"]} logout: {e}')
                continue


if __name__ == '__main__':
    while True:
        try:
            main()
            time.sleep(conf.SLEEP_TIME)
        except:
            logging.error(f'ERROR: {traceback.format_exc()}')
            time.sleep(conf.SLEEP_TIME)
