from django.urls import path
from vcc_app import views
from django.conf.urls import url
from .views import all_result, bcancer_result, lcancer_result, loginpage
from .views import bcancer
from .views import leukemia
from .views import lung
from .views import logoutpage

from .views import GeneratePdf, GenerateBcancerPdf, user_dashboard

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', loginpage, name='log'),
    path('breastcancer/', bcancer, name='bcancer'),
    path('result/', bcancer_result, name='bresult'),
    path('lung_result/', lcancer_result, name='lresult'),
    path('leukemia/', leukemia, name='leukemia'),
    path('leukemia_result/', all_result, name='all'),
    path('lungcancer/', lung, name='lung'),
    path('logout/', logoutpage, name='logout'),
    path('generate_pdf/', GeneratePdf.as_view(), name='generate_pdf'),
    path('generate_pdf_bcancer/', GenerateBcancerPdf.as_view(),
         name='generate_pdf_bcancer'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),

]
