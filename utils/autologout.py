from rocketchat_API.rocketchat import RocketChat
import requests
from datetime import datetime, timedelta

# Set up the Rocket.Chat API connection
rocket = RocketChat('admin', '1234QWE', server_url='https://rocketchat.sitetesting.fun')

# Define the timeout period in minutes
timeout_minutes = 2

# Calculate the time threshold for user inactivity
time_threshold = datetime.now() - timedelta(minutes=timeout_minutes)

# Get the list of online users
online_users = rocket.users_list(filters={'status': 'online'}).json()['users']

# Iterate through the online users
for user in online_users:
    # Get the last activity time for the user
    last_activity_time = datetime.strptime(user['lastLogin']['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # Check if the user's last activity time is before the time threshold
    if last_activity_time < time_threshold:
        # Get the user's token
        token = rocket.login(user['username'], 'password').json()['data']['authToken']

        # Logout the user from all sessions
        rocket.logout_user(user['username'])

        # Delete the user's session cookie
        requests.delete('https://rocketchat.sitetesting.fun/_session/' + token, headers={'Cookie': 'rc_uid=' + user['username'] + '; rc_token=' + token + ';'})
