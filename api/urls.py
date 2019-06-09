from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListServers, CreateServer, DetailsServer, DeleteServer, UpdateServer, pingipView,\
    chassisstatusView, chassispoweronView, chassispoweroffView, chassispowerresetView, chassispowercycleView,\
    chassis_power_to_pxeView, chassis_power_to_biosView, get_mac_addressView, set_mac_addressView,\
    ipmi_change_admin_passView, fog_get_server_idView, fog_add_taskView, fog_add_serverView, fog_add_dhcpView,\
    fog_postadd_dhcpView, ipmi_set_ip_to_staticView, chassisuidonView, chassisuidoffView, ipmi_configure_ipView,\
    ipmi_set_ip_to_dhcpView, ipmi_reset_factory_defaultsView
from rest_framework.authtoken import views

urlpatterns = {
    url(r'^list/$', ListServers.as_view(), name="list"),
    url(r'^create/$', CreateServer.as_view(), name="create"),
    url(r'^details/(?P<pk>[a-zA-Z0-9.]+)', DetailsServer.as_view(), name="details"),
    url(r'^delete/(?P<pk>[a-zA-Z0-9.]+)', DeleteServer.as_view(), name="remove"),
    url(r'^update/(?P<pk>[a-zA-Z0-9.]+)', UpdateServer.as_view(), name="update"),
    url(r'^ping/$', pingipView, name="ping"),
    url(r'^chassisstatus/$', chassisstatusView, name="chassisstatus"),
    url(r'^chassispoweron/$', chassispoweronView, name="chassispoweron"),
    url(r'^chassispoweroff/$', chassispoweroffView, name="chassispoweroff"),
    url(r'^chassispowerreset/$', chassispowerresetView, name="chassispowerreset"),
    url(r'^chassispowercycle/$', chassispowercycleView, name="chassispowercycle"),
    url(r'^chassisuidon/$', chassisuidonView, name="chassisuidon"),
    url(r'^chassisuidoff/$', chassisuidoffView, name="chassisuidoff"),
    url(r'^chassispowertopxe/$', chassis_power_to_pxeView, name="chassispowertopxe"),
    url(r'^chassispowertobios/$', chassis_power_to_biosView, name="chassispowertobiosView"),
    url(r'^getmacaddress/$', get_mac_addressView, name="getmacaddress"),
    url(r'^setmacaddress/$', set_mac_addressView, name="setmacaddress"),
    url(r'^ipmichangeadminpass/$', ipmi_change_admin_passView, name="ipmichangeadminpass"),
    url(r'^ipmisetiptostatic/$', ipmi_set_ip_to_staticView, name="ipmisetiptostatic"),
    url(r'^ipmisetiptodhcp/$', ipmi_set_ip_to_dhcpView, name="ipmisetiptodhcp"),
    url(r'^ipmiconfigureip/$', ipmi_configure_ipView, name="ipmiconfigureip"),
    url(r'^ipmiresetfactorydefaults/$', ipmi_reset_factory_defaultsView, name="ipmiresetfactorydefaults"),
    url(r'^foggetserverid/$', fog_get_server_idView, name="foggetserverid"),
    url(r'^fogaddtask/$', fog_add_taskView, name="fogaddtask"),
    url(r'^fogaddserver/$', fog_add_serverView, name="fogaddserver"),
    url(r'^fogadddhcp/$', fog_add_dhcpView, name="fogadddhcp"),
    url(r'^fogpostadddhcp/$', fog_postadd_dhcpView, name="fogpostadddhcp"),
    url(r'^api-token-auth/', views.obtain_auth_token)

}

urlpatterns = format_suffix_patterns(urlpatterns)
