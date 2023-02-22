from django.urls import path
from vcc_app import views
from django.conf.urls import url
from .views import bcancer_result, lcancer_result, loginpage
from .views import bcancer
from .views import leukemia
from .views import lung

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', loginpage, name='log'),
    path('breastcancer/', bcancer, name='bcancer'),
    path('result/', bcancer_result, name='bresult'),
    path('lung_result/', lcancer_result, name='lresult'),
    path('leukemia/', leukemia, name='leukemia'),
    path('lungcancer/', lung, name='lung'),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),
]
