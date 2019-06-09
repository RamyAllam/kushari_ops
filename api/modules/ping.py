from .. vars import *


def ping(ip_address):
    ping_data = dict()
    ping_data['ip'] = ip_address

    if os.system("ping -c {} {} >/dev/null 2>&1".format(ping_count, ip_address)) == 0:
        ping_data['status'] = ping_var['up']

    else:
        ping_data['status'] = ping_var['down']

    return ping_data
