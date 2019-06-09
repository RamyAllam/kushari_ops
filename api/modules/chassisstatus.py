import subprocess
from .. vars import *


def chassisstatus(ipmi_ip, ipmi_username, ipmi_password):
    chassisstatus_data = dict()
    chassisstatus_data['ipmi_ip'] = ipmi_ip

    try:
        command = "timeout {} ipmitool -R 2 -I lanplus -H {} -U {} -P '{}' chassis status | grep -i 'system power'" \
                  " | awk \'{{print $4}}'".format(command_timeout, ipmi_ip, ipmi_username, ipmi_password)
        output = str(subprocess.check_output(command, shell=True))

        if chassisstatus_var['on'] in output:
            chassisstatus_data['status'] = chassisstatus_var['on']

        elif chassisstatus_var['off'] in output:
            chassisstatus_data['status'] = chassisstatus_var['off']

        else:
            chassisstatus_data['status'] = ipmi_connection_error
    except:
        chassisstatus_data['status'] = "Exception ERROR!"

    return chassisstatus_data
