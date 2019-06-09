import random
import string
from .. vars import *


def chassis_uid_off(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    chassis_uid_off_data = dict()
    chassis_uid_off_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' chassis identify 0 > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file
        )
        output_status_code = os.system(command)

        if output_status_code == 0:
            chassis_uid_off_data['status'] = "success"

        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
            chassis_uid_off_data['status'] = ipmi_connection_error
            chassis_uid_off_data['description'] = logs_file_contents
        os.remove(log_file)

    except Exception as e:
        chassis_uid_off_data['description'] = "{}".format(e)
        chassis_uid_off_data['status'] = "Exception ERROR!"

    return chassis_uid_off_data
