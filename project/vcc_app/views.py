from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_requireds
def index(request):
    my_dict = {'insert_index': ""}
    return render(request, 'vcc_app/index.html', context=my_dict)


def loginpage(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'register':
            name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(name)
            print(email)
            print(password)
            new_user = User.objects.create_user(name, email, password)
            new_user.save()
            return redirect('log')

        if request.POST.get('submit') == 'login':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            print(name)
            print(password)
            print(user)
            if user is not None:
                print(name)
                print(password)
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Error, user does not exist')

    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/login.html', context=template_name)


def bcancer(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/breast_cancer.html', context=template_name)


def lung(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/lung.html', context=template_name)


def leukemia(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/leukemia.html', context=template_name)
