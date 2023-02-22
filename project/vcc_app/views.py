from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from .utils import generate_token
from .models import User
from django.utils import timezone
from pickle import load
import pickle


with open('breast_cancer.pkl', 'rb') as f:
    model = pickle.load(f)
#model = load('./breast_cancer.pkl')


def index(request):
    my_dict = {'insert_index': ""}
    return render(request, 'vcc_app/index.html', context=my_dict)


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    html_email = render_to_string('vcc_app/activate.html', context)
    plain_text_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject=email_subject, body=plain_text_email,
                                   from_email=settings.EMAIL_FROM_USER,
                                   to=[user.email],
                                   reply_to=[settings.EMAIL_FROM_USER])
    email.attach_alternative(html_email, 'text/html')
    email.send()


def loginpage(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'register':
            context = {'has_error': False, 'data': request.POST}
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create(username=username)
            user.set_password(password)
            user.is_email_verified = False
            user.save()
            send_action_email(user, request)
            messages.success(
                request, 'Account created successfully. Please check your email to verify your account.')
            return redirect('log')

        if request.POST.get('submit') == 'login':
            context = {'data': request.POST}
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user and not user.is_email_verified:
                messages.error(
                    request, 'Email is not verified, please check your email inbox')
                return render(request, 'vcc_app/login.html', context)

            if not user:
                messages.error(
                    request, 'Invalid credentials, please try again.')
                return render(request, 'vcc_app/login.html', context, status=401)
            login(request, user)
            return redirect(reverse('index'))

    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/login.html', context=template_name)


def bcancer(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/breast_cancer.html', context=template_name)


def bcancer_result(request):
    y_pred = ''
    #template_name = {'result' : y_pred}
    if request.method == 'POST':
        rm = request.POST['radius_mean']
        pm = request.POST['perimeter_mean']
        am = request.POST['area_mean']
        cm = request.POST['compactness_mean']
        com = request.POST['concavity_mean']
        cpm = request.POST['concave points_mean']
        rs = request.POST['radius_se']
        ps = request.POST['perimeter_se']
        As = request.POST['area_se']
        rw = request.POST['radius_worst']
        pw = request.POST['perimeter_worst']
        aw = request.POST['area_worst']
        cw = request.POST['compactness_worst']
        cow = request.POST['concavity_worst']
        cpw = request.POST['concave points_worst']
        y_pred = model.predict(
            [[rm, pm, am, cm, com, cpm, rs, ps, As, rw, pw, aw, cw, cow, cpw]])
        

        if y_pred[0] == 'B':
            y_pred = 'low chances'

        elif y_pred[0] == 'M':
            y_pred = 'high chances'

        else:
            y_pred = 'error in input'
    
    return render(request, 'vcc_app/result.html', {'result': y_pred})


def lung(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/lung.html', context=template_name)

def lcancer_result(request):
    a = request.POST['air_pollution']
    print(a)
    if a is not None:
        try:
            a = int(a)
            if a in range(0, 25):
                answer = 1
            elif a >= 25 and a < 50:
                answer = 2
            elif a >=50 and a < 75:
                answer = 3
            elif a >=75 and a < 100:
                answer = 4
            elif a >=100 and a < 125:
                answer = 5
            elif a >= 125 and a < 150:
                answer = 6
            elif a >=150 and a < 175:
                answer = 7
            elif a >=175 and a < 200:
                answer = 8
            elif a >=200 and a < 300:
                answer = 9
            elif a >=300:
                answer = 10
            else:
                answer = 0
        except ValueError:
            answer = 0
    else:
        answer = 0

    return render(request, "vcc_app/lung_result.html", {'key': answer})

def leukemia(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/leukemia.html', context=template_name)


def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect('log')

    return render(request, 'vcc_app/activate_failed.html', {"user": user})
