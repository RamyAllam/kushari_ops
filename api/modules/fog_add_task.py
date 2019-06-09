import requests
from .. vars import *
from .fog_login_and_session import fog_get_phpsession, fog_login


# Schedule a task from FOG web
def fog_create_task(server_id, phpsession, task_type):
    fog_create_task_data = dict()
    headers = {'Cookie': 'PHPSESSID={}'.format(phpsession)}
    params = {'wol': 'off', 'scheduleType': 'instant', 'taskhosts': server_id}
    fog_add_task_deploy_url = "{}/management/index.php?node=host&sub=deploy&id={}&type={}".format(
        fog_server_url, server_id, task_type)

    try:
        response = requests.post(fog_add_task_deploy_url, data=params, headers=headers, timeout=10)
        if fog_task_created_success_phrase in response.text:
            fog_create_task_data['status'] = "success"
            return fog_create_task_data
        elif fog_task_created_already_found_phrase in response.text:
            fog_create_task_data['status'] = "failed"
            fog_create_task_data['description'] = "Already there! Please cancel the task first"
            return fog_create_task_data
        else:
            fog_create_task_data['status'] = "failed"
            fog_create_task_data['description'] = "Unable to add a task!"
            return fog_create_task_data
    except Exception as e:
        fog_create_task_data['status'] = "error"
        fog_create_task_data['description'] = "{}".format(e)
        return fog_create_task_data


# Call internal API service to get the server ID from FOG database
def fog_get_server_id(server_ip, api_token=api_token):
    fog_get_server_id_data = dict()
    try:

        headers = {'Authorization': 'Token {}'.format(api_token)}
        params = {'ip': server_ip}
        response = requests.post("{}".format(kushari_get_fog_server_id_api_link), data=params,
                                 headers=headers, timeout=60)
        fog_get_server_id_data['fog_server_id'] = response.json()['fog_server_id']
        fog_get_server_id_data['status'] = "success"

        return fog_get_server_id_data

    except Exception as e:
        fog_get_server_id_data['status'] = "error"
        fog_get_server_id_data['description'] = "{} - {}".format(response.json()['description'], e)
        return fog_get_server_id_data


# Call everything!
def fog_start_deployment(server_ip, server_label, fog_task_type):
    fog_start_deployment_data = dict()

    # We store servers labels in fog in format DC-SERVERID Ex. DC1-004, make sure it's in this format
    server_label = str(server_label).replace(".", "-")

    # GET the server ID, session, and authenticate the session
    server_id = fog_get_server_id(server_ip, api_token=api_token)
    phpsession = fog_get_phpsession(fog_login_url)
    login_status = ""
    login_failed_description = ""

    # Check if session and server ID are there
    if phpsession['status'] == "success" and server_id['status'] == "success":
        fog_start_deployment_data['server_label'] = server_label
        fog_start_deployment_data['server_ip'] = server_ip
        fog_start_deployment_data['server_id'] = server_id['fog_server_id']
        fog_start_deployment_data['phpsession'] = phpsession['session']

        # If session and ID are there, login and create the task
        login = fog_login(fog_login_url, phpsession['session'])
        if login['status'] == "success":
            login_status = "success"
            create_task_data = fog_create_task(server_id['fog_server_id'], phpsession['session'], fog_task_type)
            fog_start_deployment_data['status'] = create_task_data['status']

            if fog_start_deployment_data['status'] == "success":
                return fog_start_deployment_data
            else:
                fog_start_deployment_data['status'] = create_task_data['status']
                fog_start_deployment_data['description'] = create_task_data['description']
                return fog_start_deployment_data

        elif login['status'] == "failed":
            login_status = "failed"
        else:
            login_status = "error"
            login_failed_description = login['description']

    # If everything is down, report it
    if login_status == "error" and phpsession['status'] == "error" and server_id['status'] == "error":
        fog_start_deployment_data['status'] = "Systems are down"
        fog_start_deployment_data['login-status'] = "Login failed to FOG!"
        fog_start_deployment_data['login-description'] = login_failed_description
        fog_start_deployment_data['session-status'] = "Failed to get session key!"
        fog_start_deployment_data['session-description'] = phpsession['description']
        fog_start_deployment_data['database-status'] = "Failed to get data from FOG DB!"
        fog_start_deployment_data['database-description'] = server_id['description']
        return fog_start_deployment_data

    if login_status == "failed":
        fog_start_deployment_data['status'] = "Login failed to FOG!"
        return fog_start_deployment_data

    if login_status == "error":
        fog_start_deployment_data['status'] = "Login failed to FOG!"
        fog_start_deployment_data['description'] = login_failed_description
        return fog_start_deployment_data

    if phpsession['status'] == "error":
        fog_start_deployment_data['status'] = "Failed to get session key!"
        fog_start_deployment_data['description'] = phpsession['description']
        return fog_start_deployment_data

    if server_id['status'] == "error":
        fog_start_deployment_data['status'] = "Failed to get data from FOG DB!"
        fog_start_deployment_data['description'] = server_id['description']
        return fog_start_deployment_data

    else:
        return "Error!"
