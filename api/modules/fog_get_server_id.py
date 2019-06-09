import pymysql
from .. vars import *


def fog_get_server_id(mysql_server=fog_mysql_server_ip, mysql_user=fog_mysql_user, mysql_pass=fog_mysql_password,
                      mysql_db=fog_mysql_db_name, server_label=''):
    fog_get_server_id_data = dict()

    # We store servers labels in fog in format DC-SERVERID Ex. DC1-004, make sure it's in this format
    server_label = str(server_label).replace(".", "-")
    fog_get_server_id_data['server_label'] = server_label

    try:
        db = pymysql.connect(mysql_server, mysql_user, mysql_pass, mysql_db, connect_timeout=10)
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("select hostID from hosts where hostName='{}'".format(server_label))
        data = cursor.fetchone()
        db.close()

        # Remove any special characters and return the value
        server_label = ''.join(e for e in str(data) if e.isalnum())

        if server_label != "None":
            fog_get_server_id_data['status'] = "success"
            fog_get_server_id_data['fog_server_id'] = server_label

        else:
            fog_get_server_id_data['status'] = "Not found!"
        return fog_get_server_id_data

    except pymysql.OperationalError as error:
        fog_get_server_id_data['status'] = "error"
        fog_get_server_id_data['description'] = "Error connecting to MySQL - {}".format(str(error))

        return fog_get_server_id_data
