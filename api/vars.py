import os
from .fog_and_dhcp_vars import *

# [Internal strings]
ping_var = {'up': 'up', 'down': 'down'}
chassisstatus_var = {'on': 'on', 'off': 'off'}  # Output from ipmitool cmd
ipmi_connection_error = "Error connecting to IPMI"
ssh_connection_error = "Error connecting to ssh"
ssh_command_error = "Command status code is not 0, possibly failed"
fog_task_created_success_phrase = "Tasked Successfully"
fog_task_created_already_found_phrase = "Host is already a member of an active task"

# [General]
ping_count = 2
command_timeout = 15
current_working_dir = os.path.dirname(os.path.realpath(__file__))
path_to_logs = "{}/logs".format(current_working_dir)
path_to_tmp = "{}/tmp".format(current_working_dir)

# [FogProject]
fog_server_url = "http://{}/fog".format(fog_server_ip)

'''
Each image in FogProject has an ID, and the following are the most common images with their IDs.
Please double check the below IDs as it may change depending on fogproject version
'''
fog_task_types = {
    'deploy': '1',
    'capture': '2',
    'fastwipe': '18',
    'normalwipe': '19',
    'fullwipe': '20',
    'debug': '3'
}

fog_login_url = "{}/management/index.php".format(fog_server_url)


# [DHCP]
dhcp_template_file = "{}/modules/src/dhcp_template.conf".format(current_working_dir)
dhcp_server_config_path = "/etc/dhcp/kushari-ops/"

# Available options are private_key and password_auth
dhcp_server_ssh_auth_method = "private_key"

# This script is exected on the DHCP server after the server is added to DHCP using kushari-ops API
dhcp_update_include_list_script = "/usr/local/kushari-ops/update_dhcp_config.sh"
dhcp_execute_postscript_add_command = "bash {}".format(dhcp_update_include_list_script)

# [Internal API EndPoints]
kushari_get_fog_server_id_api_link = "{}/foggetserverid/".format(kushari_ops_api_link)

# [Network]
'''
This is used to get the mac address for the interface using IPMI. eth0 is the first interface, and eth1 is the second
'''
nic_port = "eth1"
