"""rumahiot_sidik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from rumahiot_lemari.apps.network_connection.views import retrieve_user_wifi_connection_list, \
    add_user_wifi_connection, \
    update_user_wifi_connection, \
    remove_user_wifi_connection

urlpatterns = [
    url(r'^wifi/list$',retrieve_user_wifi_connection_list,name='retrieve_user_wifi_connection_list' ),
    url(r'^wifi/add$',add_user_wifi_connection,name='add_user_wifi_connection' ),
    url(r'^wifi/update$',update_user_wifi_connection,name='update_user_wifi_connection' ),
    url(r'^wifi/remove/(?P<user_wifi_connection_uuid>.+)$', remove_user_wifi_connection, name='remove_user_wifi_connection'),
]

