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
from .models import *

from plotly.offline import plot
import plotly.graph_objs as go
import requests
import pandas as pd
from datetime import datetime


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
    if request.method == "POST":
        filter_search = request.POST.get('search')
        if filter_search != '':
            info = CEPData.objects.filter(Chassis = filter_search).first()
            if info:
                config   = {'scrollZoom': False,'displayModeBar': False,'editable': False}    
                layout = go.Layout(
                    xaxis=dict(
                        title='Day',showgrid=False, zeroline=False
                    ),
                    yaxis=dict(
                        title='Miles',showgrid=False, zeroline=False
                    ),
                    margin=go.layout.Margin( l=30, r=30, b=10, t=10, pad=5 ),
                )
                service_count = info.service_set.count()
                if service_count > 0: 
                    services = info.service_set.all()
                    X_Array = []
                    Y_Array = []
                    hovertext = []
                    customdataurls = []
                    for service in services:
                        X_Array.append(service.Service_Date.strftime("%d %b, %Y"))
                        Y_Array.append(service.Mileage)
                        hovertext.append('Engine Build<br>Date : '+str(service.Service_Date.strftime("%d %b, %Y"))+'<br>Week : 0<br>Calendar Week : 5<br>Hours : 120<br><a href="https://www.google.com" style="text-decoration: underline;">CEP Data</a>')
                        customdataurls.append('<a href="https://www.google.com" style="text-decoration: underline overline dotted red;">CEP Data</a>')
                        
                    #figure = go.Figure([go.Scatter(x=X_Array,y=Y_Array,customdata=customdataurls,)],layout=layout)
                    figure = go.Figure([go.Scatter(x=X_Array,y=Y_Array,hoverinfo="text",hovertext=hovertext,marker=dict(color="black"),)],layout=layout)
                    #figure = go.Figure([go.Scatter(x=X_Array,y=Y_Array,text=hovertext,mode='markers',hoverinfo='text',textposition='bottom center', marker=dict(showscale=False,colorscale='Rainbow',reversescale=True,color=[],size=10,line=dict(width=2)),)],layout=layout)
                    
                    '''
                    cnt=0
                    for x in X_Array:
                        figure.update_layout(
                                showlegend=False,
                                annotations=[
                                    go.layout.Annotation(
                                        x=x,
                                        y=Y_Array[cnt],
                                        xref="x",
                                        yref="y",
                                        text='Engine Build<br>Date : '+str(x)+'<br>Week : 0<br>Calendar Week : 5<br>Hours : 120<br><a href="https://www.google.com" style="text-decoration: underline;">CEP Data</a>',
                                        showarrow=True,
                                        arrowhead=7,
                                        ax=0+int(cnt),
                                        ay=-40+int(cnt)
                                    )
                                ]
                            )
                        print('------------------')
                        print(Y_Array[cnt])
                        cnt=cnt+1
                    '''
                    
                    plot_div = plot(figure, config = config, show_link=False, output_type='div', include_plotlyjs=False)
                    context['data'] = info
                    context['plot_div'] = plot_div

    context['filter_search'] = filter_search
    return render(request, 'dashboard.html', context)

#get_chart
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chart(request):
    context = ''
    if request.method == "POST":
        filter_search = request.POST.get('search')
        filter_x_axis = request.POST.get('x-axis')
        filter_y_axis = request.POST.get('y-axis')
        if filter_search != '':
            info = CEPData.objects.filter(Chassis = filter_search).first()
            if info:
                config   = {'scrollZoom': False,'displayModeBar': False,'editable': False}    
                layout = go.Layout(
                    clickmode='event+select',
                    xaxis=dict(
                        title=str(filter_x_axis),
                        showgrid=False,
                        zeroline=False,
                    ),
                    yaxis=dict(
                        title=str(filter_y_axis),showgrid=False, zeroline=False
                    )
                    ,margin=go.layout.Margin( l=30, r=30, b=10, t=10, pad=5 ),
                )
                service_count = info.service_set.count()
                if service_count > 0: 
                    services = info.service_set.all()
                    X_Array = []
                    Y_Array = []
                    for service in services:
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
                    #chart
                    figure = go.Figure([go.Scatter(x=X_Array, y=Y_Array)],layout=layout)
                    plot_div = plot(figure, config = config, show_link=False, output_type='div', include_plotlyjs=False)

                #response
                context = plot_div
    return HttpResponse(context)