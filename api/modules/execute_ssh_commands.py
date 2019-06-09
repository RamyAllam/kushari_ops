import random
import string
from .. vars import *
import paramiko


def connect_ssh_remote(server_ip='', ssh_user='root', ssh_password='', ssh_port=22,
                       ssh_key='', auth_method="private_key"):

    connect_ssh_data = dict()
    global ssh_client
    try:

        private_key = paramiko.RSAKey.from_private_key_file(ssh_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if auth_method == 'private_key':
            ssh_client.connect(hostname=server_ip, username=ssh_user, pkey=private_key, port=ssh_port, timeout=10)
        else:
            ssh_client.connect(hostname=server_ip, username=ssh_user, password=ssh_password, port=ssh_port, timeout=10)

        connect_ssh_data['status'] = "success"
        connect_ssh_data['type'] = "remote"
        return connect_ssh_data, ssh_client

    except Exception as e:
        connect_ssh_data['status'] = "error"
        connect_ssh_data['type'] = "remote"
        connect_ssh_data['description'] = "Exception ERROR! - {}".format(e)
        return connect_ssh_data


def execute_ssh_command(command='hostname', server_ip='', ssh_user='root', ssh_password='', ssh_port=22,
                       ssh_key='', auth_method="private_key", remote=0):
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    log_file = "{}/{}.txt".format(path_to_logs, process_id)

    # Make sure the logs dir is there
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)

    execute_ssh_command_data = dict()
    global ssh_client
    try:

        if remote == 1:
            if auth_method == 'private_key':
                ssh_client = connect_ssh_remote(server_ip=server_ip, ssh_user=ssh_user, auth_method="private_key",
                                                ssh_port=ssh_port, ssh_key=ssh_key)
            else:
                ssh_client = connect_ssh_remote(server_ip=server_ip, ssh_user=ssh_user, auth_method="private_key",
                                                ssh_port=ssh_port, ssh_password=ssh_password)

            connection_object = ssh_client[1]
            connection_status = ssh_client[0]

            if connection_status['status'] == 'success':
                stdin, stdout, stderr = connection_object.exec_command(command)
                output_exit_code = stdout.channel.recv_exit_status()
                connection_object.close()

                for i in stdin, stdout, stderr:
                    try:
                        with open("{}".format(log_file), 'a') as file:
                            file.write("{}\n".format(i.readlines()))
                            file.close()

                    # Avoid failure in case of stdin or stderr are not there
                    except IOError:
                        pass

                if output_exit_code == 0:
                    with open("{}".format(log_file), 'r') as file:
                        logs_file_contents = file.read().replace('\n', '')

                    execute_ssh_command_data['status'] = "success"
                    execute_ssh_command_data['output_exit_code'] = "0"
                    execute_ssh_command_data['type'] = "remote"
                    execute_ssh_command_data['output'] = logs_file_contents
                    os.remove(log_file)

                else:
                    with open("{}".format(log_file), 'r') as file:
                        logs_file_contents = file.read().replace('\n', '')
                    execute_ssh_command_data['status'] = "success"
                    execute_ssh_command_data['output_exit_code'] = output_exit_code
                    execute_ssh_command_data['type'] = "remote"
                    execute_ssh_command_data['description'] = "{} - {}".format(ssh_command_error, logs_file_contents)
                    os.remove(log_file)
                return execute_ssh_command_data
            else:
                return connection_status

    except Exception as e:
        execute_ssh_command_data['status'] = "error"
        execute_ssh_command_data['type'] = "remote"
        execute_ssh_command_data['description-sshclient'] = "{}".format(ssh_client)
        execute_ssh_command_data['description-exception'] = "{}".format(e)
        return execute_ssh_command_data


def ssh_upload_file(remotefilepath='', localfilepath='', server_ip='', ssh_user='root', ssh_password='', ssh_port=22,
                    ssh_key='', auth_method="private_key"):

    # Make sure the logs dir is there
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)

    ssh_upload_file_data = dict()
    global ssh_client
    try:
        if auth_method == 'private_key':
            ssh_client = connect_ssh_remote(server_ip=server_ip, ssh_user=ssh_user, auth_method="private_key",
                                            ssh_port=ssh_port, ssh_key=ssh_key)
        else:
            ssh_client = connect_ssh_remote(server_ip=server_ip, ssh_user=ssh_user, auth_method="private_key",
                                            ssh_port=ssh_port, ssh_password=ssh_password)

        connection_status = ssh_client[0]
        connection_object = ssh_client[1]

        # Check if SSH is connected
        if connection_status['status'] == 'success':
            # Connect to SFTP and upload the file
            ftp_client = connection_object.open_sftp()
            ftp_client.put(localfilepath, remotefilepath)

            # Check the file info on the remote server to make sure it's uploaded
            file_info = ftp_client.lstat(remotefilepath)
            if file_info:
                ssh_upload_file_data['status'] = "success"
                ssh_upload_file_data['type'] = "remote"
                ssh_upload_file_data['remotefilepath'] = remotefilepath
                ssh_upload_file_data['localfilepath'] = localfilepath

            # If the file is not found, return failed upload
            else:
                ssh_upload_file_data['status'] = "failed"
                ssh_upload_file_data['type'] = "remote"
                ssh_upload_file_data['remotefilepath'] = remotefilepath
                ssh_upload_file_data['localfilepath'] = localfilepath

            # Close the connections
            ftp_client.close()
            connection_object.close()
            return ssh_upload_file_data

        # If SSH connection error
        else:
            return connection_status

    except Exception as e:
        ssh_upload_file_data['status'] = "error"
        ssh_upload_file_data['type'] = "remote"
        ssh_upload_file_data['remotefilepath'] = remotefilepath
        ssh_upload_file_data['localfilepath'] = localfilepath
        ssh_upload_file_data['description-sshclient'] = "{}".format(ssh_client)
        ssh_upload_file_data['description-exception'] = "{}".format(e)
        return ssh_upload_file_data
