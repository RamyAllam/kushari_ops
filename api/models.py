from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class location(models.Model):
    dc_name_or_city = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.dc_name_or_city


class servers(models.Model):
    label = models.CharField(unique=True, max_length=250)
    main_ip = models.GenericIPAddressField(unique=True, primary_key=True)
    gateway = models.GenericIPAddressField()
    netmask = models.GenericIPAddressField()
    ipmi_ip = models.GenericIPAddressField(unique=True)
    ipmi_username = models.CharField(max_length=250, default='ADMIN')
    ipmi_password = models.CharField(max_length=250)
    mac_address = models.CharField(max_length=18, blank=True, default='')
    dc_location = models.ForeignKey(location, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (self.label, self.main_ip, self.dc_location)


# This code is triggered whenever a new user has been created and saved to the database to create a token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
