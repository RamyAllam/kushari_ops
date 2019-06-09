import random
import string
from .. vars import *


def ipmi_set_ip_to_dhcp(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    ipmi_set_ip_to_dhcp_data = dict()
    ipmi_set_ip_to_dhcp_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' lan set 1 ipsrc dhcp > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file)

        output_status_code = os.system(command)

        if output_status_code == 0:
            ipmi_set_ip_to_dhcp_data['status'] = "success"

        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
                ipmi_set_ip_to_dhcp_data['status'] = ipmi_connection_error
                ipmi_set_ip_to_dhcp_data['description'] = logs_file_contents
        os.remove(log_file)

    except Exception as e:
        ipmi_set_ip_to_dhcp_data['status'] = "failed"
        ipmi_set_ip_to_dhcp_data['description'] = "{}".format(e)

    return ipmi_set_ip_to_dhcp_data
