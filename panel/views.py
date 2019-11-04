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

import io

import plotly.offline as offline
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import json
import csv

import logging

import pdfkit
from django.template import Context


db_logger = logging.getLogger('django_warrant')

#login 
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('/dashboard')
                    else:
                        messages.error(request, "'"+str(username)+"' is Inactive Username.")
                        return redirect('/login')
                else:
                    db_logger.warning('User login error : '+str(user))
                    messages.error(request, "'"+str(username)+"' is not found.")
                    return redirect('/')
            except Exception as e:
                db_logger.exception(e)
                messages.error(request, str(e))
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
                    FT_Array    = []
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
                        FT_Array.append(service.get_FormType_display())

                    context['data']         = info
                    context['X_Array']      = json.dumps(X_Array)
                    context['Y_Array']      = json.dumps(Y_Array)
                    context['I_Array']      = json.dumps(I_Array)
                    context['hovertext']    = json.dumps(hovertext)
                    context['FT_Array']     = json.dumps(FT_Array)
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
    context = {}
    service = Service.objects.filter(token = token).first()
    if service:
        formname = 'form/'+str(service.FormType)+'.html'
        context['service'] = service
        html_body = render_to_string(formname, context)
        return HttpResponse(html_body)
    else:
        return HttpResponse('Invalid Request')


#get_export_to_csv
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_csv(request,token,x_axis,y_axis):
    info = CEPData.objects.filter(token = token).first()
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
                #filter by X Axis
                if x_axis == 'Week':
                    X_Array.append('Week '+str(service.Service_Date.strftime("%w %b %Y")))
                elif x_axis == 'Month':
                    X_Array.append(service.Service_Date.strftime("%b %Y"))
                else:
                    X_Array.append(service.Service_Date.strftime("%d %b, %Y"))
                #filter by Y Axis
                if y_axis == 'Hours':
                    km = service.Mileage * 1.60934
                    hours = km * 0.62
                    Y_Array.append(round(hours))
                elif y_axis == 'Km':
                    km = service.Mileage * 1.60934
                    Y_Array.append(round(km))
                else:
                    Y_Array.append(service.Mileage)

                hovertext.append('Engine Build /n Date : '+str(service.Service_Date.strftime("%d %b, %Y"))+'<br>Week : 0<br>Calendar Week : 5<br>Hours : 120<br><a href="">'+str(service.get_FormType_display())+'</a>')

        response = HttpResponse(content_type='text/csv')
        filename = str(info.Chassis)+'-Chassis-History-'+str(datetime.now())
        response['Content-Disposition'] = 'attachment; filename="'+str(filename)+'.csv"'
        writer = csv.writer(response)
        writer.writerow([x_axis, y_axis])
        if X_Array:
            for x in range(len(X_Array)):
                writer.writerow([X_Array[x], Y_Array[x]])
        return response

#export_to_pdf
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf(request,token,x_axis,y_axis):
    info = CEPData.objects.filter(token = token).first()
    if info:
        service_count = info.service_set.count()
        if service_count > 0: 
            services    = info.service_set.all()
            I_Array     = []
            X_Array     = []
            Y_Array     = []
            hovertext   = []
            annotations = []
            for service in services:
                annotation = {}
                I_Array.append(str(service.token))
                #filter by X Axis
                if x_axis == 'Week':
                    x = 'Week '+str(service.Service_Date.strftime("%w %b %Y"))
                    X_Array.append(x)
                elif x_axis == 'Month':
                    x = 'Week '+str(service.Service_Date.strftime("%b %Y"))
                    X_Array.append(x)
                else:
                    x = 'Week '+str(service.Service_Date.strftime("%d %b, %Y"))
                    X_Array.append(x)

                #filter by Y Axis
                if y_axis == 'Hours':
                    km = service.Mileage * 1.60934
                    hours = km * 0.62
                    y = round(hours)
                    Y_Array.append(y)
                elif y_axis == 'Km':
                    km = service.Mileage * 1.60934
                    y = round(km)
                    Y_Array.append(y)
                else:
                    y = service.Mileage
                    Y_Array.append(y)

                text = 'Engine Build <br> Date : '+str(service.Service_Date.strftime("%d %b, %Y"))+'<br>Week : 0<br>Calendar Week : 5<br>Hours : 120<br><a href="">'+str(service.get_FormType_display())+'</a>'    
                hovertext.append(text)

                annotation['x']             = x
                annotation['y']             = y+250
                annotation['align']         = 'center'
                annotation['arrowcolor']    = '#636363'
                annotation['arrowhead']     = 2
                annotation['arrowsize']     = 1
                annotation['arrowwidth']    = 2
                annotation['text']          = text
                annotation['showarrow']     = True
                annotation['ax']            = 0
                annotation['ay']            = -100
                annotation['bordercolor']   = '#c7c7c7'
                annotation['borderpad']     = 4
                annotation['borderwidth']   = 2
                annotation['bgcolor']       = '#ff7f0e'
                annotation['font']          = dict(size=14,color="#ffffff")
                annotation['opacity']       = 0.8
                annotations.append(annotation)
                
                 
    
        data = [go.Scatter(x=X_Array, y=Y_Array, mode='lines+markers', text=hovertext, textposition='top center')]
        config   = {'scrollZoom': False,'displayModeBar': False,'editable': False}    
        layout = go.Layout(
            title= str(info.Chassis)+' Chassis History',
            width=1200,
            height=800,
            xaxis=dict(
                title=str(x_axis),showgrid=False, zeroline=False
            ),
            yaxis=dict(
                title=str(y_axis),showgrid=False, zeroline=False
            )
            ,margin=go.layout.Margin( l=30, r=30, b=10, t=50, pad=5 ),
            annotations=annotations
        )

        filename = str(info.Chassis)+'-Chassis-History-'+str(datetime.now())+'.pdf'

        fig = offline.plot({'data': data,
                            'layout': layout},
                            config = config,
                            auto_open=False,
                            show_link=False,
                            output_type='div', include_plotlyjs=True)

        opt = {'javascript-delay': 5000,'no-stop-slow-scripts': None,'debug-javascript': None}
        pdfkit.from_string(fig, 'media/pdf/'+str(filename), options=opt)
        pdf = open('media/pdf/'+str(filename), 'rb')
        response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
        response['Content-Disposition'] = 'attachment; filename='+str(filename)
        pdf.close()
        return response  # returns the response.
        
    
