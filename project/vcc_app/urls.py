from django.urls import path
from vcc_app import views
from django.conf.urls import url
from .views import loginpage
from .views import bcancer
from .views import leukemia
from .views import lung

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', loginpage, name='log'),
    path('breastcancer/', bcancer, name='bcancer'),
    path('leukemia/', leukemia, name='leukemia'),
    path('lungcancer/', lung, name='lung'),
]
