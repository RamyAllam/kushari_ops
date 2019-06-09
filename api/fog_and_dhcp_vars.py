# [FogProject]
# FogProject server IP
fog_server_ip = "CHANGE_ME"

# FogProject Username
fog_username = "CHANGE_ME"

# FogProject Password
fog_password = "CHANGE_ME"

# FogProject MySQL server IP
fog_mysql_server_ip = "CHANGE_ME"

# FogProject MySQL username
fog_mysql_user = "CHANGE_ME"

# FogProject MySQL password
fog_mysql_password = "CHANGE_ME"

# FogProject MySQL db name
fog_mysql_db_name = "CHANGE_ME"

# FogProject image ID, used by default for new added hosts through the API
fog_image_id = 1  # CHANGE_ME

# [DHCP]
# DHCP server IP, or leave it if DHCP is running on the same FogProject server
dhcp_server_ip = fog_server_ip

# DHCP server port, default to 22
dhcp_server_ssh_port = 22

# DHCP server username, default to root
dhcp_server_ssh_user = "root"

# DHCP server password ( Optional ), used only if "dhcp_server_ssh_auth_method" is not set to private_key
dhcp_server_ssh_password = "CHANGE_ME"

# Private SSH KEY path on kushari server to auth to fog server
dhcp_server_ssh_key = "/home/CHANGE_ME/.ssh/id_rsa"

# [Internal API EndPoints]
# Kushari-ops server API link. Ex https://kushari-ops.ramyallam.com:8080/api
kushari_ops_api_link = "https://DOMAIN:PORT/api"  # Change me

# API token for kushar-ops admin user to do internal communications, get it from the admin area
api_token = "CHANGE_ME"
