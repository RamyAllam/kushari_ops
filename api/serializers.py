from rest_framework import serializers
from .models import servers
from .vars import fog_task_types


class ServersSerializer(serializers.ModelSerializer):

    class Meta:
        model = servers
        fields = ('label', 'main_ip', 'gateway', 'netmask', 'ipmi_ip', 'ipmi_username', 'ipmi_password', 'mac_address')


class PingipSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassisstatusSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispoweronSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispoweroffSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispowerresetSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispowercycleSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispowertopxeSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassispowertobiosSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassisuidonSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class ChassisuidoffSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class GetmacaddressSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class SetmacaddressSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class IpmichangeadminpassSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class IpmisetiptostaticSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class IpmisetiptodhcpSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class Ipmiresetfactorydefaults(serializers.Serializer):
    ip = serializers.IPAddressField()


class IpmiconfigureipSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class fog_get_server_idSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class fog_add_taskSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    task_type = serializers.ChoiceField(choices=list(fog_task_types.keys()), allow_blank=False, allow_null=False)


class fog_add_serverSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()


class fog_add_dhcpSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
