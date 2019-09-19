from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache  import cache_control
from django.http.response import  HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings #
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import Group, User
from django.template.loader import get_template, render_to_string
from .models import *

from plotly.offline import plot
import plotly.graph_objs as go
import requests
import pandas as pd
from datetime import datetime
import json
import requests
import csv

import logging
db_logger = logging.getLogger('django_auth_ldap')

#login 
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    messages.error(request, "'"+str(username)+"' is Inactive Username.")
                    return redirect('/login')
            else:
                messages.error(request, "'"+str(username)+"' is not found.")
                return redirect('/')
    else:
            form = LoginForm()
    
    context = {"form": form,}
    return render(request, 'login.html', context)

#logout
@login_required(login_url="/login")  # - if not logged in redirect to /
def logout_view(request):
    try:
        logout(request)
        return redirect('/login')
    except Exception as e:
        return e

#dashboard
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    context = {}
    filter_search = ''
    filter_x_axis = 'Day'
    filter_y_axis = 'Miles'
    isData = 'No'
    DefaultMessage = 'Please search vehicle information using Chassis ID / ESN'
    if request.method == "POST":
        filter_search = request.POST.get('search')
        filter_x_axis = request.POST.get('x-axis')
        filter_y_axis = request.POST.get('y-axis')
        if filter_search != '':
            info = CEPData.objects.filter(Chassis = filter_search).first()
            if info:
                service_count = info.service_set.count()
                if service_count > 0: 
                    services    = info.service_set.all()
                    I_Array     = []
                    X_Array     = []
                    Y_Array     = []
                    hovertext   = []
                    for service in services:
                        I_Array.append(str(service.token))
                        #X_Array.append(service.Service_Date.strftime("%d %b, %Y"))
                        #Y_Array.append(service.Mileage)
                        #filter by X Axis
                        if filter_x_axis == 'Week':
                            X_Array.append('Week '+str(service.Service_Date.strftime("%w %b %Y")))
                        elif filter_x_axis == 'Month':
                            X_Array.append(service.Service_Date.strftime("%b %Y"))
                        else:
                            X_Array.append(service.Service_Date.strftime("%d %b, %Y"))
                        #filter by Y Axis
                        if filter_y_axis == 'Hours':
                            km = service.Mileage * 1.60934
                            hours = km * 0.62
                            Y_Array.append(round(hours))
                        elif filter_y_axis == 'Km':
                            km = service.Mileage * 1.60934
                            Y_Array.append(round(km))
                        else:
                            Y_Array.append(service.Mileage)

                        hovertext.append('Engine Build<br>Date : '+str(service.Service_Date.strftime("%d %b, %Y"))+'<br>Week : 0<br>Calendar Week : 5<br>Hours : 120<br>')
                    context['data']         = info
                    context['X_Array']      = json.dumps(X_Array)
                    context['Y_Array']      = json.dumps(Y_Array)
                    context['I_Array']      = json.dumps(I_Array)
                    context['hovertext']    = json.dumps(hovertext)
                    isData = 'Yes'
            else:
                DefaultMessage = 'Vehicle Information not found, Please try with other Chassis ID / ESN.'
    context['filter_search'] = filter_search
    context['filter_x_axis'] = filter_x_axis
    context['filter_y_axis'] = filter_y_axis
    context['isData'] = isData
    context['DefaultMessage'] = DefaultMessage
    return render(request, 'dashboard.html', context)

#get_chart
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def service(request,token):
    service = Service.objects.filter(token = token).first()
    if service:
        html_body = render_to_string('service.html', context={})
        return HttpResponse(html_body)
    else:
        return HttpResponse('Invalid Request')


#get_chart
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_csv(request):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&apikey=demo&datatype=csv'
    response = requests.get(url)        

    with open('out.csv', 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))