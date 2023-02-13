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


def lung(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/lung.html', context=template_name)


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
