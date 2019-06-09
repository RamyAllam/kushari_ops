import pymysql.cursors
from .. vars import *


def fog_add_server(mysql_server=fog_mysql_server_ip, mysql_user=fog_mysql_user, mysql_pass=fog_mysql_password,
                   mysql_db=fog_mysql_db_name, server_label=''):
    fog_add_server_data = dict()
    # We store servers labels in fog in format DC-SERVERID Ex. DC1-004, make sure it's in this format
    server_label = str(server_label).replace(".", "-")
    fog_add_server_data['server_label'] = server_label

    connection = pymysql.connect(mysql_server, mysql_user, mysql_pass, mysql_db, connect_timeout=10, autocommit=True)

    try:
        with connection.cursor() as cursor:
            sql_add_hosts = "INSERT INTO `hosts` (`hostName`,`hostDesc`,`hostIP`,`hostImage`,`hostBuilding`," \
                            "`hostLastDeploy`,`hostCreateBy`,`hostUseAD`,`hostADDomain`,`hostADOU`,`hostADUser`," \
                            "`hostADPass`," \
                            "`hostADPassLegacy`,`hostProductKey`,`hostPrinterLevel`,`hostKernelArgs`,`hostKernel`," \
                            "`hostDevice`," \
                            "`hostInit`,`hostPending`,`hostPubKey`,`hostSecToken`,`hostSecTime`,`hostPingCode`," \
                            "`hostExitBios`," \
                            "`hostExitEfi`,`hostEnforce`) VALUES ('{}','NV7wjALQ2FUhLjbjKyVE','',7,0," \
                            "'0000-00-00 00:00:00'," \
                            "'fog','','','','','','','','','','','','','','','','0000-00-00 00:00:00','','','',1)" \
                            " ON DUPLICATE KEY UPDATE `hostName`=VALUES(`hostName`),`hostDesc`=VALUES(`hostDesc`)," \
                            "`hostIP`=VALUES(`hostIP`),`hostImage`=VALUES(`hostImage`)," \
                            "`hostBuilding`=VALUES(`hostBuilding`)," \
                            "`hostCreateDate`=VALUES(`hostCreateDate`),`hostLastDeploy`=VALUES(`hostLastDeploy`)," \
                            "`hostCreateBy`=VALUES(`hostCreateBy`),`hostUseAD`=VALUES(`hostUseAD`)," \
                            "`hostADDomain`=VALUES(`hostADDomain`)," \
                            "`hostADOU`=VALUES(`hostADOU`),`hostADUser`=VALUES(`hostADUser`)," \
                            "`hostADPass`=VALUES(`hostADPass`)," \
                            "`hostADPassLegacy`=VALUES(`hostADPassLegacy`),`hostProductKey`=VALUES(`hostProductKey`)," \
                            "`hostPrinterLevel`=VALUES(`hostPrinterLevel`),`hostKernelArgs`=VALUES(`hostKernelArgs`)," \
                            "`hostKernel`=VALUES(`hostKernel`),`hostDevice`=VALUES(`hostDevice`)," \
                            "`hostInit`=VALUES(`hostInit`)," \
                            "`hostPending`=VALUES(`hostPending`),`hostPubKey`=VALUES(`hostPubKey`)," \
                            "`hostSecToken`=VALUES(`hostSecToken`)," \
                            "`hostSecTime`=VALUES(`hostSecTime`),`hostPingCode`=VALUES(`hostPingCode`)," \
                            "`hostExitBios`=VALUES(`hostExitBios`),`hostExitEfi`=VALUES(`hostExitEfi`)," \
                            "`hostEnforce`=VALUES(`hostEnforce`)".format(server_label)

            sql_get_host_id = "select hostID from hosts where hostName='{}'".format(server_label)
            cursor.execute(sql_get_host_id)

            cursor.execute(sql_add_hosts)
            connection.close()

            fog_add_server_data['fog_server_id'] = server_label
            if server_label:
                fog_add_server_data['status'] = "success"
            else:
                fog_add_server_data['status'] = "Not found!"
            return fog_add_server_data

    except pymysql.OperationalError as error:
        connection.close()
        fog_add_server_data['status'] = "error"
        fog_add_server_data['description'] = "Error connecting to MySQL - {}".format(str(error))
        return fog_add_server_data
