from django.urls import path
from vcc_app import views
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name='index')
]
