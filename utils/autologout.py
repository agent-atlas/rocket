import traceback
from datetime import datetime, timedelta

import time

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException, \
    RocketMissingParamException

from utils.adapter import RocketChatApi


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


if __name__ == 'main':
    while True:
        try:
            print('Start the script')
            main()
            time.sleep(60)
        except Exception as e:
            print('Error: {}'.format(traceback.format_exc(e)))
