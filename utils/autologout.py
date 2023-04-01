# from rocketchat_API.rocketchat import RocketChat
import requests
from datetime import datetime, timedelta

import time
from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException
from rocketchat_API.APIExceptions.RocketAuthenticationException import RocketAuthenticationException
from rocketchat_API.APIExceptions.RocketMissingParamException import RocketMissingParamException
from rocketchat_API import RocketChatAPI

def main():
    api = RocketChatAPI(settings={
    "username": "ivat",
    "password": "Pbvf94",
    "domain": "rocketchat.sitetesting.fun",
    "ssl_verify": False
})
# ssl_verify=False
    # rocket = RocketChat('ivat', 'Pbvf94', server_url='https://rocketchat.sitetesting.fun', )

    timeout_minutes = 2
    time_threshold = datetime.now() - timedelta(minutes=timeout_minutes)
    # users_online = api.users_list(status='online').json()
    online_users = api.users_list(status='online').json()
    for user in online_users["users"]:
        # получение информации о пользователе
        try:
            user_info = api.users_info(user["username"]).json()
        except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
            print(f"Error: {e}")
            continue
        
        # получение времени последней активности пользователя
        last_activity = user_info["user"]["lastLogin"]["$date"] / 1000.0
        current_time = time.time()
        
        # проверка, прошло ли более 2 минут с последней активности пользователя
        if current_time - last_activity > 120:
            # отправка запроса на логаут пользователя
            try:
                api.logout_user(user_id=user_info["user"]["_id"])
                print(f"User {user_info['user']['username']} was logged out")
            except (RocketConnectionException, RocketAuthenticationException, RocketMissingParamException) as e:
                print(f"Error: {e}")
                continue
while True:
    try:
        main()
        time.sleep(120)
    except Exception as e:
        print('Error:, {}'.format(e))