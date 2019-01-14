from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [

	url(r'^login/$', views.mobile_login, name='mobile_login'),
	url(r'^getQuantityDetailsurl/$', views.getQuantityDetailsurl, name='getQuantityDetailsurl'),
	url(r'^getCurrentData/$', views.getCurrentData, name='getCurrentData'),
	url(r'^controlActuator/$', views.controlActuator, name='controlActuator'),
	url(r'^dataUpdate/$', views.dataUpdate, name='dataUpdate'),
	url(r'^changeactuatorstatus/$', views.changeActuatorStatus, name='changeactuatorstatus'),
	
	
	
	
	
	
]