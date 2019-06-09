import random
import string
from .. vars import *


def chassis_power_to_bios(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    chassispowertopxe_data = dict()
    chassispowertopxe_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' chassis bootparam set bootflag force_bios" \
                  " > {} 2>&1 && " \
                  "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' chassis power cycle > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, log_file, command_timeout, ipmi_ip, ipmi_username,
            ipmi_password, log_file)

        output_status_code = os.system(command)

        if output_status_code == 0:
            chassispowertopxe_data['status'] = "success"

        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
            chassispowertopxe_data['status'] = ipmi_connection_error
            chassispowertopxe_data['description'] = logs_file_contents

        os.remove(log_file)

    except:
        chassispowertopxe_data['status'] = "Exception ERROR!"

    return chassispowertopxe_data
