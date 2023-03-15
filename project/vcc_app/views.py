from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from .models import User
import pickle
import math
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, CustomUserCreationForm

with open('breast_cancer.pkl', 'rb') as f:
    breast_model = pickle.load(f)

with open('lung_cancer.pkl', 'rb') as l:
    lung_model = pickle.load(l)


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        logged_in = True
    else:
        username = ""
        logged_in = False
    my_dict = {'insert_index': "",
               'username': username, 'logged_in': logged_in}
    return render(request, 'vcc_app/index.html', context=my_dict)


@login_required(login_url='log')
def logoutpage(request):
    logout(request)
    return redirect(reverse('index'))


def loginpage(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'register':
            context = {'has_error': False, 'data': request.POST}
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(
                request, 'Account created successfully.')
            return redirect('log')

        if request.POST.get('submit') == 'login':
            context = {'data': request.POST}
            name = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=name)
                if user.check_password(password):
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    messages.error(
                        request, 'Invalid credentials, please try again.')
                    return render(request, 'vcc_app/login.html', context, status=401)
            except User.DoesNotExist:
                messages.error(
                    request, 'Invalid credentials, please try again.')
                return render(request, 'vcc_app/login.html', context, status=401)

    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/login.html', context=template_name)


@login_required(login_url='log')
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
        y_pred = breast_model.predict(
            [[rm, pm, am, cm, com, cpm, rs, ps, As, rw, pw, aw, cw, cow, cpw]])

        if y_pred[0] == 'B':
            y_pred = 'low chances'

        elif y_pred[0] == 'M':
            y_pred = 'high chances'

        else:
            y_pred = 'error in input'

    return render(request, 'vcc_app/result.html', {'result': y_pred})


@login_required(login_url='log')
def lung(request):
    template_name = {'insert_index': ""}
    return render(request, 'vcc_app/lung.html', context=template_name)


def lcancer_result(request):

    # air pollution
    a = request.POST['air_pollution']
    print(a)
    if a is not None:
        try:
            a = int(a)
            if a in range(0, 25):
                input1 = 1
            elif a >= 25 and a < 50:
                input1 = 2
            elif a >= 50 and a < 75:
                input1 = 3
            elif a >= 75 and a < 100:
                input1 = 4
            elif a >= 100 and a < 125:
                input1 = 5
            elif a >= 125 and a < 150:
                input1 = 6
            elif a >= 150 and a < 175:
                input1 = 7
            elif a >= 175 and a < 200:
                input1 = 8
            elif a >= 200 and a < 300:
                input1 = 9
            elif a >= 300:
                input1 = 10
            else:
                input1 = 0
        except ValueError:
            input1 = 0
    else:
        input1 = 0

    # alcohol use
    b = request.POST['alcohol_use']
    b = int(b)
    input2 = b

    # dust allergy
    c = request.POST['chk[]']
    c = int(c)

    d = request.POST['dust_allergy']
    if d is not None:
        try:
            d = int(d)

        except ValueError:
            d = "error"
    else:
        d = "error"

    x = (c+d)/2
    input3 = math.floor(x)

    # occupational hazard
    e = request.POST['hazard1']
    e = int(e)
    f = request.POST['hazard2']
    f = int(f)
    y = (e+f)/2
    input4 = math.floor(y)

    # genetic risk
    g = request.POST['genetic_risk']
    g = int(g)
    input5 = g

    # chronic lung disease
    h = request.POST['chronic_disease']
    h = int(h)
    input6 = h

    # balanced diet
    s = request.POST['diet']
    s = int(s)
    input7 = s

    # obesity
    k = request.POST['obesity']
    if k is not None:
        try:
            k = float(k)
            if k >= 0 and k < 18.5:
                input8 = 1
            elif k >= 18.5 and k < 25:
                input8 = 2
            elif k >= 25 and k < 30:
                input8 = 4
            elif k >= 30 and k < 35:
                input8 = 5
            elif k >= 35 and k < 40:
                input8 = 7
            elif k >= 40 and k < 42.5:
                input8 = 8
            elif a >= 42.5:
                input1 = 10
            else:
                input8 = 0
        except ValueError:
            input8 = 0
    else:
        input8 = 0

    # passive smoker
    l = request.POST['passive_smoker']
    l = int(l)
    input9 = l

    # chest pain
    m = request.POST['chest_pain1']
    m = int(m)
    n = request.POST['chest_pain2']
    n = int(n)
    o = (m+n)/2
    input10 = math.floor(o)

    # coughing blood
    p = request.POST['blood']
    p = int(p)
    input11 = p

    # fatigue
    q = request.POST['fatigue']
    q = int(q)
    input12 = q

    result_list = [input1, input2, input3, input4, input5,
                   input6, input7, input8, input9, input10, input11, input12]

    prediction = lung_model.predict([result_list])

    if prediction[0] == "Low":
        prediction = 'low chances'

    elif prediction[0] == "High":
        prediction = 'possibility of lung cancer'

    else:
        prediction = 'error in input'

    return render(request, "vcc_app/lung_result.html", {'key': prediction})


@login_required(login_url='log')
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
