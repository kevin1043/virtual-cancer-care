from django.core.files.storage import default_storage
import cv2
import io
from tkinter import Image
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from markupsafe import Markup
# from matplotlib import transforms
import torch
from .models import User, BreastCancerResult, LungCancerResult, LeukemiaCancerResult
import pickle
import math
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, CustomUserCreationForm
import os
from keras.models import load_model
import numpy as np
from django.http import JsonResponse
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from keras.optimizers import Adam
#optimizer = tf.keras.optimizers.Adam()
from PIL import Image
from keras.utils import load_img, img_to_array
# from utils.cellInfo import cell_dic
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf  # created in step 4


def user_dashboard(request):
    if request.method == 'POST':

        cancer_type = request.POST.get('cancer_type', None)
        if cancer_type:
            user_results = get_user_results(request.user.id, cancer_type)
            field_names = [f.name for f in user_results.model._meta.fields]
            if request.user.is_authenticated:
                username = request.user.username
                logged_in = True
            else:
                username = ""
                logged_in = False
            template_name = {'insert_index': "",
                             'username': username, 'logged_in': logged_in, 'user_results': user_results, 'field_names': field_names}
            return render(request, 'vcc_app/userdashboard.html', context=template_name)
        else:
            user_results = get_user_results(request.user.id)
            # Set default field names to be displayed if no model is selected
            # Change this as per your requirement
            field_names = ['prediction', 'timestamp']
            if request.user.is_authenticated:
                username = request.user.username
                logged_in = True
            else:
                username = ""
                logged_in = False
            template_name = {'insert_index': "",
                             'username': username, 'logged_in': logged_in, 'user_results': user_results, 'field_names': field_names}
            return render(request, 'vcc_app/userdashboard.html', context=template_name)
    else:
        user_results = get_user_results(request.user.id)
        # Set default field names to be displayed if no model is selected
        # Change this as per your requirement
        field_names = ['prediction', 'timestamp']
        if request.user.is_authenticated:
            username = request.user.username
            logged_in = True
        else:
            username = ""
            logged_in = False
        template_name = {'insert_index': "",
                         'username': username, 'logged_in': logged_in, 'user_results': user_results, 'field_names': field_names}
        return render(request, 'vcc_app/userdashboard.html', context=template_name)


def get_user_results(user_id, cancer_type=None):
    if cancer_type == 'lung':
        return LungCancerResult.objects.filter(user_id=user_id)
    elif cancer_type == 'breast':
        return BreastCancerResult.objects.filter(user_id=user_id)
    elif cancer_type == 'leukemia':
        return LeukemiaCancerResult.objects.filter(user_id=user_id)
    else:
        return [LungCancerResult.objects.filter(user_id=user_id),
                BreastCancerResult.objects.filter(user_id=user_id),
                LeukemiaCancerResult.objects.filter(user_id=user_id)]


class GenerateBcancerPdf(View):
    def get(self, request, *args, **kwargs):
        user_result = BreastCancerResult.objects.filter(
            user=request.user).order_by('-timestamp').first()

        data = {
            'radius_mean': user_result.radius_mean,
            'perimeter_mean': user_result.perimeter_mean,
            'area_mean': user_result.area_mean,
            'concavity_mean': user_result.concavity_mean,
            'concave_points_mean': user_result.concave_points_mean,
            'radius_worst': user_result.radius_worst,
            'perimeter_worst': user_result.perimeter_worst,
            'area_worst': user_result.area_worst,
            'concavity_worst': user_result.concavity_worst,
            'concave_points_worst': user_result.concave_points_worst,
            'predicted_result': user_result.predicted_result,

        }
        # Pass the data to the template rendering function
        template = 'vcc_app/invoicebcancer.html'
        context = {'inputs': data}
        html = render(request, template, context)

        # Generate the PDF file
        pdf = render_to_pdf(template, context)
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        user_result = LungCancerResult.objects.filter(
            user=request.user).order_by('-timestamp').first()

        data = {
            'air_pollution': user_result.air_pollution,
            'alcohol_use': user_result.alcohol_use,
            'dust_allergy1': user_result.dust_allergy1,
            'dust_allergy2': user_result.dust_allergy2,
            'occupational_hazard1': user_result.occupational_hazard1,
            'occupational_hazard2': user_result.occupational_hazard2,
            'genetic_risk': user_result.genetic_risk,
            'chronic_lung_disease': user_result.chronic_lung_disease,
            'balanced_diet': user_result.balanced_diet,
            'obesity': user_result.obesity,
            'passive_smoker': user_result.passive_smoker,
            'chest_pain1': user_result.chest_pain1,
            'chest_pain2': user_result.chest_pain2,
            'coughing_blood': user_result.coughing_blood,
            'fatigue': user_result.fatigue,
            'prediction': user_result.prediction,
        }

        # Pass the data to the template rendering function
        template = 'vcc_app/invoice.html'
        context = {'inputs': data}
        html = render(request, template, context)

        # Generate the PDF file
        pdf = render_to_pdf(template, context)
        return HttpResponse(pdf, content_type='application/pdf')


class CustomAdam(Adam):
    pass


# Load the trained model
#all_model = tf.keras.models.load_model('model.h5')
custom_objects = {'CustomAdam': CustomAdam}
all_model = tf.keras.models.load_model(
    'model.h5', custom_objects=custom_objects)


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
    if request.user.is_authenticated:
        username = request.user.username
        logged_in = True
    else:
        username = ""
        logged_in = False
    template_name = {'insert_index': "",
                     'username': username, 'logged_in': logged_in}
    return render(request, 'vcc_app/breast_cancer.html', context=template_name)
#  context = {'result': y_pred, 'inputs': inputs,'username': username, 'logged_in': logged_in}
    # return render(request, 'vcc_app/result.html', context=context)


@login_required(login_url='log')
def bcancer_result(request):
    y_pred = ''

    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            logged_in = True
        else:
            username = ""
            logged_in = False

        rm = request.POST['radius_mean']
        pm = request.POST['perimeter_mean']
        am = request.POST['area_mean']
        #cm = request.POST['compactness_mean']
        com = request.POST['concavity_mean']
        cpm = request.POST['concave points_mean']
        rw = request.POST['radius_worst']
        pw = request.POST['perimeter_worst']
        aw = request.POST['area_worst']
        #cw = request.POST['compactness_worst']
        cow = request.POST['concavity_worst']
        cpw = request.POST['concave_points_worst']

        # create a dictionary with key-value pairs of entered values
        inputs = {'radius_mean': rm, 'perimeter_mean': pm, 'area_mean': am,
                  'concavity_mean': com,
                  'concave points_mean': cpm,
                  'radius_worst': rw,
                  'perimeter_worst': pw, 'area_worst': aw,
                  'concavity_worst': cow,
                  'concave_points_worst': cpw}

        y_pred = breast_model.predict(
            [[rm, pm, am, com, cpm, rw, pw, aw, cow, cpw]])

        if y_pred[0] == 'B':
            y_pred = 'low chances'
        elif y_pred[0] == 'M':
            y_pred = 'high chances'
        else:
            y_pred = 'error in input'
        # add the inputs dictionary to the context dictionary
        # store the result in the database for the logged-in user
        temp = BreastCancerResult(
            user=request.user,
            radius_mean=rm,
            perimeter_mean=pm,
            area_mean=am,
            concavity_mean=com,
            concave_points_mean=cpm,
            radius_worst=rw,
            perimeter_worst=pw,
            area_worst=aw,
            concavity_worst=cow,
            concave_points_worst=cpw,
            predicted_result=y_pred,
        )
        temp.save()
        context = {'result': y_pred, 'inputs': inputs,
                   'username': username, 'logged_in': logged_in}
        return render(request, 'vcc_app/result.html', context=context)
    else:
        return render(request, 'vcc_app/')


@login_required(login_url='log')
def lung(request):
    if request.user.is_authenticated:
        username = request.user.username
        logged_in = True
    else:
        username = ""
        logged_in = False
    template_name = {'insert_index': "",
                     'username': username, 'logged_in': logged_in}
    return render(request, 'vcc_app/lung.html', context=template_name)


def lcancer_result(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            logged_in = True
        else:
            username = ""
            logged_in = False
        # air pollution
        a = request.POST['air_pollution']
        print(a)
        if a is not None:
            try:
                a = int(a)
                temp12 = a
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
        if b == 1:
            temp1 = "never"
        elif b == 2:
            temp1 = "1-2 drinks per month"
        elif b == 3:
            temp1 = "1-2 drinks per week"
        elif b == 6:
            temp1 = "1-2 drinks per day"
        elif b == 8:
            temp1 = "8-12 drinks per week"
        elif b == 10:
            temp1 = "more than above "
        input2 = b

        # dust allergy
        c = request.POST['chk[]']
        c = int(c)
        if c == 2:
            temp2 = "1-2"
        elif c == 5:
            temp2 = "weekly"
        elif c == 9:
            temp2 = "more than 5 times a month"
        elif c == 1:
            temp2 = "none"

        d = request.POST['dust_allergy']
        if d is not None:
            try:
                d = int(d)

            except ValueError:
                d = "error"
        else:
            d = "error"
        temp14 = d
        x = (c+d)/2
        input3 = math.floor(x)

        # occupational hazard
        e = request.POST['hazard1']
        e = int(e)
        if e == 10:
            temp3 = "yes"
        elif e == 5:
            temp3 = "sometimes"
        elif e == 1:
            temp3 = "no"

        f = request.POST['hazard2']
        f = int(f)
        if f == 10:
            temp4 = "high"
        elif f == 6:
            temp4 = "moderate"
        elif f == 4:
            temp4 = "low"
        elif f == 1:
            temp4 = "none"
        y = (e+f)/2
        input4 = math.floor(y)

        # genetic risk
        g = request.POST['genetic_risk']
        g = int(g)
        if g == 4:
            temp5 = "Parent"
        elif g == 3:
            temp5 = "GrandParent"
        elif g == 3:
            temp5 = "other blood relative"
        elif g == 1:
            temp5 = "no one"
        input5 = g

        # chronic lung disease
        h = request.POST['chronic_disease']
        h = int(h)
        if h == 10:
            temp6 = "yes"
        elif h == 1:
            temp6 = "no"
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
                temp11 = k
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
        if l == 10:
            temp7 = "yes and frequently"
        elif l == 7:
            temp7 = "yes but not frequently"
        elif l == 5:
            temp7 = "sometimes"
        elif l == 2:
            temp7 = "rarely"
        elif l == 2:
            temp7 = "no"
        input9 = l

        # chest pain
        m = request.POST['chest_pain1']
        m = int(m)
        if m == 10:
            temp8 = "yes"
        elif m == 1:
            temp8 = "no"

        n = request.POST['chest_pain2']
        n = int(n)
        temp13 = n
        o = (m+n)/2
        input10 = math.floor(o)

        # coughing blood
        p = request.POST['blood']
        p = int(p)
        if p == 9:
            temp9 = "frequently"
        elif p == 6:
            temp9 = "has happened few times"
        elif p == 1:
            temp9 = "no"
        input11 = p

        # fatigue
        q = request.POST['fatigue']
        q = int(q)
        if q == 10:
            temp10 = "yes,frequently"
        elif q == 8:
            temp10 = "often"
        elif q == 6:
            temp10 = "sometimes"
        elif q == 3:
            temp10 = "rarely"
        elif q == 1:
            temp10 = "never"

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

        user = request.user

        input = {
            'air_pollution': temp12,
            'alcohol_use': temp1,
            'dust_allergy1': temp2,
            'dust_allergy2': temp14,
            'occupational_hazard1': temp3,
            'occupational_hazard2': temp4,
            'genetic_risk': temp5,
            'chronic_lung_disease': temp6,
            'balanced_diet': input7,
            'obesity': temp11,
            'passive_smoker': temp7,
            'chest_pain1': temp8,
            'chest_pain2': temp13,
            'coughing_blood': temp9,
            'fatigue': temp10,
            'prediction': prediction
        }

        result = LungCancerResult(
            air_pollution=temp12,
            alcohol_use=temp1,
            dust_allergy1=temp2,
            dust_allergy2=temp14,
            occupational_hazard1=temp3,
            occupational_hazard2=temp4,
            genetic_risk=temp5,
            chronic_lung_disease=temp6,
            balanced_diet=input7,
            obesity=temp11,
            passive_smoker=temp7,
            chest_pain1=temp8,
            chest_pain2=temp13,
            coughing_blood=temp9,
            fatigue=temp10,
            prediction=prediction,
            user=user
        )
        result.save()
        template_name = {'insert_index': "", 'key': prediction,
                         'inputs': input, 'username': username, 'logged_in': logged_in}
        return render(request, "vcc_app/lung_result.html", context=template_name)


@login_required(login_url='log')
def leukemia(request):
    if request.user.is_authenticated:
        username = request.user.username
        logged_in = True
    else:
        username = ""
        logged_in = False
    template_name = {'insert_index': "",
                     'username': username, 'logged_in': logged_in}
    return render(request, 'vcc_app/leukemia.html', context=template_name)


disease_classes = ['all',
                   'hem']

# __> here

cell_dic = [
    'healthy cell info here',
    'cancerous cell info here'
]


@login_required(login_url='log')
def all_result(request):
    if request.method == 'POST' and request.FILES:
        # Get the uploaded image file
        if request.user.is_authenticated:
            username = request.user.username
            logged_in = True
        else:
            username = ""
            logged_in = False
        uploaded_file = request.FILES['image']

        # Save the uploaded file to disk with a unique filename
        filename = default_storage.save(uploaded_file.name, uploaded_file)

        # Open the file for reading
        with default_storage.open(filename, 'rb') as f:
            # Read the file data
            file_data = f.read()

        # Decode the file data into a numpy array
        nparr = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Resize the image
        resized_image = cv2.resize(img, (600, 600))
        print("test")
        print(resized_image)
        # Preprocess the image
        x = img_to_array(resized_image)
        x = np.expand_dims(x, axis=0)
        x /= 255.

        # Make predictions on the image using the pre-trained model
        preds = all_model.predict(x)
        sv = preds[0][0]
        cell_dic = [
            'Low chances',
            'High chances'
        ]

        if sv > 0.2:
            result = "healthy cell"
            index = 0
        else:
            result = "cancerous cell"
            index = 1
        prediction1 = (str(cell_dic[index]))
        temp = LeukemiaCancerResult(
            user=request.user,
            sv=sv,
            prediction=prediction1,
        )
        temp.save()
        print("this")
        print(preds)
        print(prediction1)
        x = 1

        template_name = {'insert_index': "", 'result': result, 'preds': sv,
                         'prediction': prediction1, 'username': username, 'logged_in': logged_in}
        # Render the results page with the predictions
        return render(request, 'vcc_app/leukemia_result.html', context=template_name)
        # return render(request, 'vcc_app/leukemia_result.html', {'prediction': x})
    else:
        return render(request, 'index.html')
