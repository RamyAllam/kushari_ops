import random
import string
from .. vars import *


def chassispowercycle(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    chassispowercycle_data = dict()
    chassispowercycle_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' chassis power cycle > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file)
        output_status_code = os.system(command)

        if output_status_code == 0:
            chassispowercycle_data['status'] = "success"

        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
            chassispowercycle_data['status'] = ipmi_connection_error
            chassispowercycle_data['description'] = logs_file_contents
        os.remove(log_file)

    except:
        chassispowercycle_data['status'] = "Exception ERROR!"

    return chassispowercycle_data
