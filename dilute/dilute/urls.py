from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', views.homepage, name='homepage'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^api/', include('api.urls', namespace='api'))
]