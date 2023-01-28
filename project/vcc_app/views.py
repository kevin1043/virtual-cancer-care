from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Create your views here.


def index(request):
    my_dict = {'insert_index': ""}
    return render(request, 'vcc_app/index.html', context=my_dict)


def log(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/login.html', context=template_name)
