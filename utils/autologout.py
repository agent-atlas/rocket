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

        if last_activity_time < time_threshold and last_status != 'online':
            rocket.logout_user(user['username'])

while True:
    main()