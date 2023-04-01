from rocketchat_API.rocketchat import RocketChat
import requests
from datetime import datetime, timedelta

def main():
    rocket = RocketChat('ivat', 'Pbvf94', server_url='https://rocketchat.sitetesting.fun')

    timeout_minutes = 2
    time_threshold = datetime.now() - timedelta(minutes=timeout_minutes)
    
    online_users = rocket.users_list(filters={'status': 'online'}).json()['users']

    for user in online_users:
        last_activity_time = datetime.strptime(user['lastLogin']['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        last_status = user['status']

        if last_activity_time < time_threshold and user['status'] != 'online':
            token = rocket.login(user['username'], 'password').json()['data']['authToken']
            
            rocket.logout_user(user['username'])
            requests.delete('https://rocketchat.sitetesting.fun/_session/' + token, headers={'Cookie': 'rc_uid=' + user['username'] + '; rc_token=' + token + ';'})

while True:
    try:
        main()
    except Exception as e:
        print(f'error: {e}')