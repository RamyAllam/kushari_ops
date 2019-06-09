import requests
import random
import string
from .. vars import *
from .fog_login_and_session import fog_get_phpsession, fog_login


# Call internal API service to get the server ID from FOG database
def fog_get_server_id(server_ip, api_token=api_token):
    fog_get_server_id_data = dict()

    try:

        headers = {'Authorization': 'Token {}'.format(api_token)}
        params = {'ip': server_ip}
        response = requests.post("{}".format(kushari_get_fog_server_id_api_link), data=params,
                                 headers=headers, timeout=60)
        status = response.json()['status']
        if status == "success":
            fog_get_server_id_data['fog_server_id'] = response.json()['fog_server_id']
            fog_get_server_id_data['status'] = "success"
            return fog_get_server_id_data
        else:
            fog_get_server_id_data['status'] = "failed"
            return fog_get_server_id_data

    except Exception as e:
        fog_get_server_id_data['status'] = "error"
        fog_get_server_id_data['description'] = "{} - {}".format(response.json()['description'], e)
        return fog_get_server_id_data


# Create a host from FOG web
def fog_create_host(server_label, server_ip, mac_address, description, phpsession, image_id=fog_image_id):
    fog_create_host_data = dict()
    headers = {'Cookie': 'PHPSESSID={}'.format(phpsession)}
    params = {'host': server_label,
              'mac': mac_address,
              'description': description,
              'key': '',
              'image': image_id,
              'kern': '',
              'args': '',
              'init': '',
              'dev': '',
              'bootTypeExit': '',
              'efiBootTypeExit': '',
              'fakeusernameremembered': '',
              'fakepasswordremembered': '',
              'domainname': '',
              'ou': '',
              'domainuser': '',
              'domainpassword': '',
              'domainpasswordlegacy': '',
              'enforcesel': 'on',
              'enforce': '',
              'updatead': 'Add'
              }
    fog_create_host_url = "{}/management/index.php?node=host&sub=add".format(fog_server_url)

    try:
        # Check if the server is already there
        server_id_data = fog_get_server_id(server_ip, api_token=api_token)
        if server_id_data['status'] == 'success':
            server_id = server_id_data['fog_server_id']
            fog_create_host_data['status'] = "alreadythere"
            fog_create_host_data['fog_server_id'] = server_id
            return fog_create_host_data

        else:
            # Create the server, send the post request
            response = requests.post(fog_create_host_url, data=params, headers=headers, timeout=10)
            # Check if server created
            server_id_data = fog_get_server_id(server_ip, api_token=api_token)
            if server_id_data['status'] == 'success':
                server_id = server_id_data['fog_server_id']
                fog_create_host_data['status'] = "success"
                fog_create_host_data['fog_server_id'] = server_id
                return fog_create_host_data
            else:
                fog_create_host_data['status'] = "failed"
                fog_create_host_data['description'] = "Unable to add a host!"
            return fog_create_host_data
    except Exception as e:
        fog_create_host_data['status'] = "error"
        fog_create_host_data['description'] = "{}".format(e)
        return fog_create_host_data


# Call everything!
def fog_start_create_host(server_ip, server_label, mac_address):
    fog_start_create_host_data = dict()

    # We store servers labels in fog in format DC-SERVERID Ex. DC1-004, make sure it's in this format
    server_label = str(server_label).replace(".", "-")

    # Generate windows administrator password
    windows_administrator_password = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(25))

    phpsession = fog_get_phpsession(fog_login_url)
    global login_status
    login_status = ""
    login_failed_description = ""

    # Check if session and server ID are there
    if phpsession['status'] == "success":
        fog_start_create_host_data['server_label'] = server_label
        fog_start_create_host_data['server_ip'] = server_ip
        fog_start_create_host_data['phpsession'] = phpsession['session']
        # If session and ID are there, login and create the task
        login = fog_login(fog_login_url, phpsession['session'])
        if login['status'] == "success":
            login_status = "success"
            create_host_data = fog_create_host(server_label, server_ip, mac_address, windows_administrator_password,
                                               phpsession['session'], image_id=fog_image_id)

            if create_host_data['status'] == "success":
                fog_start_create_host_data['status'] = "success"
                fog_start_create_host_data['fog_server_id'] = create_host_data['fog_server_id']
                fog_start_create_host_data['windows-administrator-password'] = windows_administrator_password
                return fog_start_create_host_data

            # If the host already there, return different json data
            elif create_host_data['status'] == "alreadythere":
                fog_start_create_host_data['status'] = "success"
                fog_start_create_host_data['fog_server_id'] = create_host_data['fog_server_id']
                fog_start_create_host_data['alreadythere'] = True

                return fog_start_create_host_data

            else:
                fog_start_create_host_data['status'] = create_host_data['status']
                fog_start_create_host_data['description'] = create_host_data['description']
                return fog_start_create_host_data

        elif login['status'] == "failed":
            login_status = "failed"
        else:
            login_status = "error"
            login_failed_description = login['description']

    # If everything is down, report it
    if login_status == "error" and phpsession['status'] == "error":
        fog_start_create_host_data['status'] = "Systems are down"
        fog_start_create_host_data['login-status'] = "Login failed to FOG!"
        fog_start_create_host_data['login-description'] = login_failed_description
        fog_start_create_host_data['session-status'] = "Failed to get session key!"
        fog_start_create_host_data['session-description'] = phpsession['description']
        return fog_start_create_host_data

    if login_status == "failed":
        fog_start_create_host_data['status'] = "Login failed to FOG!"
        return fog_start_create_host_data

    if login_status == "error":
        fog_start_create_host_data['status'] = "Login failed to FOG!"
        fog_start_create_host_data['description'] = login_failed_description
        return fog_start_create_host_data

    if phpsession['status'] == "error":
        fog_start_create_host_data['status'] = "Failed to get session key!"
        fog_start_create_host_data['description'] = phpsession['description']
        return fog_start_create_host_data

    else:
        fog_start_create_host_data['status'] = "error2"
        return fog_start_create_host_data
