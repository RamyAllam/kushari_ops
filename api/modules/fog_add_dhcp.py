from string import Template
import random
import string
from .execute_ssh_commands import ssh_upload_file
from .. vars import *
from netaddr import *


def generate_dhcp_config(network, netmask, gateway, ipaddr, hostname,
                         mac, nextserver=fog_server_ip, template_file=dhcp_template_file,
                         dhcp_server_ip=dhcp_server_ip, ssh_user=dhcp_server_ssh_user, ssh_password=dhcp_server_ssh_password,
                         auth_method=dhcp_server_ssh_auth_method, ssh_port=dhcp_server_ssh_port, ssh_key=dhcp_server_ssh_key,
                         dhcp_server_config_path=dhcp_server_config_path, broadcast=''):

    # We store servers labels in fog in format DC-SERVERID Ex. DC1-004, make sure it's in this format
    hostname = str(hostname).replace(".", "-")

    # Subnetting
    subnet = IPNetwork('{}/{}'.format(network, netmask))
    ip_list = list(subnet)
    network = str(subnet.network)

    # Check if broadcast is passed, if not, calculate it
    if not len(broadcast):
        broadcast = str(subnet.broadcast)

    # Check if gateway is passed, if not, calculate it
    if not len(gateway):
        gateway = str(ip_list[1])

    generate_dhcp_config_data = dict()
    global upload_file_to_dhcp_server_data

    # Check if other important var are there
    if len(network) and len(netmask) and len(gateway) and len(ipaddr) and len(broadcast) and len(hostname)\
            and len(nextserver) and len(mac):

        process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        tmp_file_export = "{}/{}.conf".format(path_to_tmp, process_id)

        # Make sure the tmp dir is there
        if not os.path.exists(path_to_tmp):
            os.makedirs(path_to_tmp)

        with open(template_file) as file:
            dhcp_template_read_file = file.read()

        dhcp_template = Template(dhcp_template_read_file)

        substitute_list = {'network': network, 'netmask': netmask, 'gateway': gateway, 'broadcast': broadcast,
                           'ipaddr': ipaddr, 'nextserver': nextserver, 'hostname': hostname, 'mac': mac}

        # Generate the dhcp config file
        dhcp_generate_config = dhcp_template.substitute(substitute_list)

        # Save DHCP config file
        with open("{}".format(tmp_file_export), 'a') as file:
            file.write("{}".format(dhcp_generate_config))
            file.close()

        try:
            # Upload DHCP config file
            upload_file_to_dhcp_server_data = ssh_upload_file(server_ip=dhcp_server_ip, ssh_user=ssh_user,
                                                              auth_method=auth_method,
                                                              ssh_port=ssh_port, ssh_key=ssh_key,
                                                              ssh_password=ssh_password,
                                                              remotefilepath="{}/{}.conf".format(
                                                                  dhcp_server_config_path, hostname),
                                                              localfilepath=tmp_file_export
                                                              )

            # Check if DHCP file is uploaded
            if upload_file_to_dhcp_server_data['status'] == 'success':
                generate_dhcp_config_data['status'] = "success"
                generate_dhcp_config_data['type'] = upload_file_to_dhcp_server_data['type']
                generate_dhcp_config_data['remotefilepath'] = upload_file_to_dhcp_server_data['remotefilepath']
                generate_dhcp_config_data['localfilepath'] = upload_file_to_dhcp_server_data['localfilepath']
                os.remove(tmp_file_export)
                return generate_dhcp_config_data

            # If it is not uploaded, return the upload request data
            else:
                return upload_file_to_dhcp_server_data

        except Exception as e:
            generate_dhcp_config_data['status'] = "error"
            generate_dhcp_config_data['description'] = "{} - {}".format(e, upload_file_to_dhcp_server_data)
            return generate_dhcp_config_data

    else:
        generate_dhcp_config_data['status'] = "failed"
        generate_dhcp_config_data['description'] = "One or more of the network variables are missing," \
                                                   " please check kushari-ops server info"
        return generate_dhcp_config_data
