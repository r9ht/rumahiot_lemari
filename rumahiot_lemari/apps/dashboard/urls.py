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
from rumahiot_lemari.apps.dashboard.views import add_device_dashboard_chart, get_device_dashboard_chart, remove_device_dashboard_chart

urlpatterns = [
    url(r'^chart/list$', get_device_dashboard_chart,name='get_device_dashboard_chart' ),
    url(r'^chart/add$', add_device_dashboard_chart,name='add_device_dashboard_chart' ),
    url(r'^chart/remove/(?P<user_dashboard_chart_uuid>.+)$', remove_device_dashboard_chart,name='remove_device_dashboard_chart' )
]
