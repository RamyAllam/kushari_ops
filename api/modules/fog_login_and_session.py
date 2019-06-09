from .. vars import *
import requests


# Fog gives the user a session once he logged into the page and then authorize it after login, get it
def fog_get_phpsession(url):
    fog_get_phpsession_data = dict()
    try:
        response = requests.get(url, timeout=10)
        fog_get_phpsession_data['session'] = response.cookies['PHPSESSID']
        fog_get_phpsession_data['status'] = "success"
        return fog_get_phpsession_data
    except Exception as e:
        fog_get_phpsession_data['status'] = "error"
        fog_get_phpsession_data['description'] = "{}".format(e)
        return fog_get_phpsession_data


# Send post request with login credentials to authorize the PHP session
def fog_login(url, php_session):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'uname': fog_username, 'upass': fog_password, 'ulang': 'English', 'login': 'Login'}
    cookies = dict(PHPSESSID=php_session)
    fog_login_data = dict()
    try:
        response = requests.post(url, data=params, headers=headers, cookies=cookies, timeout=10)

        # If user logged, the next page in fog web contains information including the server IP.
        # Let's verify if it's actually logged.
        if fog_server_ip in response.text:
            fog_login_data['status'] = 'success'
            return fog_login_data
        else:
            fog_login_data['status'] = "failed"
            return fog_login_data
    except Exception as e:
        fog_login_data['status'] = "error"
        fog_login_data['description'] = "{}".format(e)
        return fog_login_data
