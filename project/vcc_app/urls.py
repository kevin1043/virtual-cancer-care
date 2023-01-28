from django.urls import path
from vcc_app import views
from django.conf.urls import url
from .views import log
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', log, name='log'),
]
