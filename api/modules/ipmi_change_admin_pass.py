import random
import string
from .. vars import *


def ipmi_change_admin_pass(ipmi_ip, ipmi_username, ipmi_password):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)
    password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                       for _ in range(15))

    ipmichangeadminpass_data = dict()
    ipmichangeadminpass_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' user set password 2 {} > {} 2>&1".format(
            command_timeout, ipmi_ip, ipmi_username, ipmi_password, password, log_file)
        output_status_code = os.system(command)

        if output_status_code == 0:
            ipmichangeadminpass_data['status'] = "success"
            ipmichangeadminpass_data['newpassword'] = password
        else:
            with open("{}".format(log_file), 'r') as file:
                logs_file_contents = file.read().replace('\n', '')
            ipmichangeadminpass_data['status'] = ipmi_connection_error
            ipmichangeadminpass_data['description'] = logs_file_contents
        os.remove(log_file)

    except:
        ipmichangeadminpass_data['status'] = "Exception ERROR!"

    return ipmichangeadminpass_data
