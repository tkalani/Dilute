from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^signup/$', views.Signup, name='signup'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),  
    url(r'^home/$', views.home, name='home'),
    url(r'^dashboard/$', views.Dashboard, name='dashboard'),
    url(r'^dataUpdate/(?P<mobile_no>[0-9]{10})/$', views.dataUpdate, name='dataUpdate'),   
    url(r'^main/$', views.Main, name='main'),  
    url(r'^residence/$', views.Residence, name='residence'),
    url(r'^updateVehicles/$', views.UpdateVehicles, name='updateVehicles'),
    url(r'^updateMembers/$', views.UpdateMembers, name='updateMembers'),
    url(r'^updatePlants/$', views.UpdatePlants, name='updatePlants'),
    url(r'^UpdateResidenceDetails/$', views.UpdateResidenceDetails, name='UpdateResidenceDetails'),
    url(r'^getInitialSettingsDetails/$', views.GetInitialSettingsDetails, name='getInitialSettingsDetails'),
    url(r'^updateReservoirSettings/$', views.updateReservoirSettings, name='updateReservoirSettings'),
    url(r'^logQuantumMainTankData/$', views.logQuantumMainTankData.as_view(), name='logQuantumMainTankData'),
    url(r'^logCategoryTanksData/$', views.logCategoryTanksData.as_view(), name='logCategoryTanksData'),
    url(r'^showDataDateRange/$', views.showDataDateRange, name='showDataDateRange'),
    url(r'^updateActuatorControlSettings/$', views.updateActuatorControlSettings, name='updateActuatorControlSettings'),
    url(r'^updateActuatorLinkSettings/$', views.updateActuatorLinkSettings, name='updateActuatorLinkSettings'),
    url(r'^controlActuator/$', views.controlActuator, name='controlActuator'),
    url(r'^predictions/$', views.predictions, name='predictions'),
    url(r'^predictionsData/$', views.predictionsData, name='predictionsData'),
    url(r'^city/(?P<cityID>[0-9])/$', views.city, name='city'),
    url(r'^cityData/$', views.cityData, name='cityData')
]