from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ServersSerializer, PingipSerializer, ChassisstatusSerializer, ChassispoweronSerializer,\
    ChassispoweroffSerializer, ChassispowerresetSerializer, ChassispowercycleSerializer, ChassispowertopxeSerializer,\
    ChassispowertobiosSerializer, GetmacaddressSerializer, SetmacaddressSerializer, IpmichangeadminpassSerializer,\
    fog_get_server_idSerializer, fog_add_taskSerializer, fog_add_serverSerializer, fog_add_dhcpSerializer,\
    IpmisetiptostaticSerializer, ChassisuidonSerializer, ChassisuidoffSerializer, IpmiconfigureipSerializer,\
    IpmisetiptodhcpSerializer, Ipmiresetfactorydefaults
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from .models import servers
from .modules import ping, chassisstatus, chassispoweron, chassispoweroff, chassispowerreset, chassispowercycle,\
    chassis_power_to_pxe, chassis_power_to_bios, get_mac_address, ipmi_change_admin_pass, fog_get_server_id, fog_add_task,\
    fog_add_server, fog_add_dhcp, fog_postadd_dhcp, ipmi_set_ip_to_static, chassis_uid_on, chassis_uid_off, ipmi_configure_ip,\
    ipmi_set_ip_to_dhcp, ipmi_reset_factory_defaults
from .vars import fog_task_types


class ListServers(generics.ListAPIView):
    queryset = servers.objects.all()
    serializer_class = ServersSerializer


class CreateServer(generics.CreateAPIView):
    serializer_class = ServersSerializer

    def create_server(self, serializer):
        serializer.save()


class DetailsServer(generics.RetrieveAPIView):
    queryset = servers.objects.all()
    serializer_class = ServersSerializer


class DeleteServer(generics.DestroyAPIView):
    queryset = servers.objects.all()
    serializer_class = ServersSerializer


class UpdateServer(generics.UpdateAPIView):
    queryset = servers.objects.all()
    serializer_class = ServersSerializer


@api_view(['POST'])
def pingipView(request):

    if request.method == 'POST':
        serializer = PingipSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip = data['ip']

            # Ping IP
            results = ping.ping(ip)

            # If Ok, return the results
            return Response(results, status=status.HTTP_200_OK)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassisstatusView(request):

    if request.method == 'POST':
        serializer = ChassisstatusSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis Status
                results = chassisstatus.chassisstatus(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassispoweronView(request):

    if request.method == 'POST':
        serializer = ChassispoweronSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power on
                results = chassispoweron.chassispoweron(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassispoweroffView(request):

    if request.method == 'POST':
        serializer = ChassispoweroffSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power off
                results = chassispoweroff.chassispoweroff(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassispowerresetView(request):

    if request.method == 'POST':
        serializer = ChassispowerresetSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power reset
                results = chassispowerreset.chassispowerreset(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassispowercycleView(request):

    if request.method == 'POST':
        serializer = ChassispowercycleSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power cycle
                results = chassispowercycle.chassispowercycle(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassisuidonView(request):

    if request.method == 'POST':
        serializer = ChassisuidonSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis UID ON
                results = chassis_uid_on.chassis_uid_on(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassisuidoffView(request):

    if request.method == 'POST':
        serializer = ChassisuidoffSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis UID OFF
                results = chassis_uid_off.chassis_uid_off(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassis_power_to_pxeView(request):

    if request.method == 'POST':
        serializer = ChassispowertopxeSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power to PXE
                results = chassis_power_to_pxe.chassis_power_to_pxe(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def chassis_power_to_biosView(request):

    if request.method == 'POST':
        serializer = ChassispowertobiosSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Chassis power to bios
                results = chassis_power_to_bios.chassis_power_to_bios(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_mac_addressView(request):

    if request.method == 'POST':
        serializer = GetmacaddressSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Get Mac Address
                results = get_mac_address.get_mac_address(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def set_mac_addressView(request):

    if request.method == 'POST':
        serializer = SetmacaddressSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Get Mac Address
                results = get_mac_address.get_mac_address(ipmi_ip, ipmi_username, ipmi_password)
                # Save the results to DB and add try in case the ipmi cmd failed to retrieve the mac address
                try:
                    if results['macaddress']:
                        db_objects.mac_address = results['macaddress']
                        db_objects.save()
                except:
                    pass
                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ipmi_change_admin_passView(request):

    if request.method == 'POST':
        serializer = IpmichangeadminpassSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Change Admin pass and return thew new pass
                results = ipmi_change_admin_pass.ipmi_change_admin_pass(ipmi_ip, ipmi_username, ipmi_password)
                # Save the results to DB and add try in case the ipmi cmd failed to change the pass
                try:
                    if results['newpassword']:
                        db_objects.ipmi_password = results['newpassword']
                        db_objects.save()
                except:
                    pass
                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ipmi_set_ip_to_staticView(request):

    if request.method == 'POST':
        serializer = IpmisetiptostaticSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Set IP to Static
                results = ipmi_set_ip_to_static.ipmi_set_ip_to_static(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ipmi_set_ip_to_dhcpView(request):

    if request.method == 'POST':
        serializer = IpmisetiptodhcpSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Set IP to dhcp
                results = ipmi_set_ip_to_dhcp.ipmi_set_ip_to_dhcp(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ipmi_reset_factory_defaultsView(request):

    if request.method == 'POST':
        serializer = Ipmiresetfactorydefaults(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Set To Factory Defaults
                results = ipmi_reset_factory_defaults.ipmi_reset_factory_defaults(ipmi_ip, ipmi_username, ipmi_password)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ipmi_configure_ipView(request):

    if request.method == 'POST':
        serializer = IpmiconfigureipSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']
            new_ip_from_request = data['new_ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    ipmi_ip = db_objects.ipmi_ip
                    ipmi_username = db_objects.ipmi_username
                    ipmi_password = db_objects.ipmi_password

                # IPMI Configure IP
                results = ipmi_configure_ip.ipmi_configure_ip(ipmi_ip, ipmi_username, ipmi_password,
                                                              new_ipmi_ip=new_ip_from_request)
                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fog_get_server_idView(request):

    if request.method == 'POST':
        serializer = fog_get_server_idSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:

                for db_objects in ip_from_db:
                    server_label = db_objects.label
                # Call get server ID function
                results = fog_get_server_id.fog_get_server_id(server_label=server_label)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fog_add_taskView(request):

    if request.method == 'POST':
        serializer = fog_add_taskSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']
            fog_task_type_from_request = data['task_type']

            # Process the data after getting it from the request
            fog_task_type_get_integer = fog_task_types[fog_task_type_from_request]
            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    main_ip = db_objects.main_ip
                    label = db_objects.label

                # Call add task function
                results = fog_add_task.fog_start_deployment(server_ip=main_ip, server_label=label,
                                                            fog_task_type=fog_task_type_get_integer)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fog_add_serverView(request):

    if request.method == 'POST':
        serializer = fog_add_serverSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    main_ip = db_objects.main_ip
                    label = db_objects.label
                    mac_address = db_objects.mac_address

                # Call add task function
                results = fog_add_server.fog_start_create_host(server_ip=main_ip, server_label=label, mac_address=mac_address)

                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fog_add_dhcpView(request):

    if request.method == 'POST':
        serializer = fog_add_dhcpSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the data from json
            json = JSONRenderer().render(serializer.data)
            stream = BytesIO(json)
            data = JSONParser().parse(stream)
            ip_from_request = data['ip']

            ip_from_db = servers.objects.filter(main_ip=ip_from_request)

            if ip_from_db:
                for db_objects in ip_from_db:
                    main_ip = db_objects.main_ip
                    gateway = db_objects.gateway
                    netmask = db_objects.netmask
                    label = db_objects.label
                    mac_address = db_objects.mac_address

                # Call add task function
                results = fog_add_dhcp.generate_dhcp_config(network=main_ip, netmask=netmask, gateway=gateway,
                                                            ipaddr=main_ip, hostname=label, mac=mac_address)
                # If Ok, return the results
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response("{} Not found!".format(ip_from_request), status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fog_postadd_dhcpView(request):

    if request.method == 'POST':
        results = fog_postadd_dhcp.start_postadd_dhcp_config()

        # If Ok, return the results
        return Response(results, status=status.HTTP_200_OK)
