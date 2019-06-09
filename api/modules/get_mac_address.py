import random
import string
from .. vars import *


def get_mac_address(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    macaddress_data = dict()
    macaddress_data['ipmi_ip'] = ipmi_ip

    try:
        if nic_port == "eth0":
            command = "timeout {} ipmitool -I lanplus -H {} -U {} -P '{}' raw 0x30 0x21> {} 2>&1".format(
                command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file)
        else:
            command = "timeout {} ipmitool -I lanplus -H {} -U {} -P '{}' raw 0x30 0x9f | head -n 1 > {} 2>&1".format(
                command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file)

        output_status_code = os.system(command)

        with open("{}".format(log_file), 'r') as file:
            if nic_port == "eth0":
                logs_file_contents = file.read().replace('\n', '')

                # IPMI command output is like ' 7a 07 02 02 1c c6 8a 33 ab da' and the following to extract the mac addr
                logs_file_contents_mac = ':'.join(logs_file_contents.split(" ")[-6:])

            else:
                logs_file_contents = file.read().replace('\n', '').lstrip()

                # GET the second PORT
                logs_file_contents_mac = ':'.join(logs_file_contents.split(" ")[:7]).replace("01:", "")

        if output_status_code == 0:
            macaddress_data['macaddress'] = logs_file_contents_mac
            macaddress_data['status'] = "success"

        else:
            macaddress_data['status'] = ipmi_connection_error
            macaddress_data['description'] = logs_file_contents

        os.remove(log_file)

    except:
        macaddress_data['status'] = "Exception ERROR!"

    return macaddress_data
