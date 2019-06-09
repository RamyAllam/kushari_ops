from .execute_ssh_commands import execute_ssh_command
from .. vars import *


def postadd_dhcp_config(command='', server_ip='', ssh_user='root', ssh_password='', ssh_port=22, ssh_key='',
                        auth_method='private_key', remote=1):

    postadd_dhcp_config_data = dict()
    execute_dhcp_post_add = execute_ssh_command(command=command,
                                                server_ip=server_ip,
                                                ssh_user=ssh_user, ssh_password=ssh_password,
                                                ssh_port=ssh_port,
                                                ssh_key=ssh_key, auth_method=auth_method, remote=remote)

    if execute_dhcp_post_add['status'] == 'success' and execute_dhcp_post_add['output_exit_code'] == '0':
        postadd_dhcp_config_data['status'] = "success"
        postadd_dhcp_config_data['type'] = execute_dhcp_post_add['type']
        postadd_dhcp_config_data['output_exit_code'] = execute_dhcp_post_add['output_exit_code']
        postadd_dhcp_config_data['output'] = execute_dhcp_post_add['output']
        return postadd_dhcp_config_data

    else:
        return execute_dhcp_post_add


def start_postadd_dhcp_config():
    data = postadd_dhcp_config(command=dhcp_execute_postscript_add_command, server_ip=dhcp_server_ip,
                               ssh_user=dhcp_server_ssh_user,
                               ssh_password=dhcp_server_ssh_password, ssh_port=dhcp_server_ssh_port,
                               ssh_key=dhcp_server_ssh_key,
                               auth_method=dhcp_server_ssh_auth_method, remote=1)

    return data
