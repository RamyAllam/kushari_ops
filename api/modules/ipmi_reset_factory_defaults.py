import random
import string
from .. vars import *


def ipmi_reset_factory_defaults(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    ipmi_reset_factory_defaults_data = dict()
    ipmi_reset_factory_defaults_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' raw 0x3c 0x40 > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file)

        output_status_code = os.system(command)

        if output_status_code == 0:
            ipmi_reset_factory_defaults_data['status'] = "success"

        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
                ipmi_reset_factory_defaults_data['status'] = ipmi_connection_error
                ipmi_reset_factory_defaults_data['description'] = logs_file_contents
        os.remove(log_file)

    except Exception as e:
        ipmi_reset_factory_defaults_data['status'] = "failed"
        ipmi_reset_factory_defaults_data['description'] = "{}".format(e)

    return ipmi_reset_factory_defaults_data
