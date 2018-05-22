from django import forms
from django.utils.translation import ugettext_lazy as _

class AddUserWifiConnectionForm(forms.Form):
    connection_name = forms.CharField(required=True, max_length=32)
    ssid = forms.CharField(required=True, max_length=32)
    # 1 for true, 0 for false
    security_enabled = forms.CharField(required=True, max_length=1)
    # Just fill password with "-" if security is disabled
    password = forms.CharField(required=False, max_length=63)

class UpdateUserWifiConnectionForm(forms.Form):
    user_wifi_connection_uuid = forms.CharField(required=True, max_length=32)
    connection_name = forms.CharField(required=True, max_length=32)
    ssid = forms.CharField(required=True, max_length=32)
    # 1 for true, 0 for false
    security_enabled = forms.CharField(required=True, max_length=1)
    # Just fill password with "-" if security is disabled
    password = forms.CharField(required=False, max_length=63)