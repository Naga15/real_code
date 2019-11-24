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
from .vehicle import *

import io
import plotly.offline as offline
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import simplejson as json
import csv

import uuid 
import psycopg2
#import pdfkit
from django.template import Context
from dateutil.parser import parse


from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


import logging
db_logger = logging.getLogger('django_auth')

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
                        db_logger.info('User Login : '+str(username)+' is successfully login.')
                        return redirect('/dashboard')
                    else:
                        db_logger.warning('User Login : '+str(username)+' is inactive Username.')
                        messages.error(request, "'"+str(username)+"' is inactive Username.")
                        return redirect('/login')
                else:
                    db_logger.warning('User Login : '+str(username)+' is invalid username.')
                    messages.error(request, "'"+str(username)+"' is invalid username.")
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
        db_logger.info('User Logout : '+str(request.user.username)+' is successfully logout.')
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
            #search chassis
            results = search_chassis_timeline(filter_search)
            if results:
                I_Array     = []
                X_Array     = []
                Y_Array     = []
                FT_Array    = []
                hovertext   = []
                for record in results:
                    p = {'chassisid' : record[0], 'eventdesc' : record[1], 'timedate' : record[2], 'timeday' : record[3], 'timeweek' : record[4], 'timecalendarweek' : record[5], 'mileage' : record[6], 'mileagekm' : record[7], 'enginehours' : record[8], 'engineonly' : record[9], 'eventid' : record[10]}
                    timedate = p['timedate']
                    I_Array.append(str(p['eventid']))
                    if filter_x_axis == 'Week':
                        timedate = timedate.strftime("%w %b %Y")
                        X_Array.append('Week '+str(timedate))
                    elif filter_x_axis == 'Month':
                        timedate = timedate.strftime("%b %Y")
                        X_Array.append(timedate)
                    else:
                        timedate = timedate.strftime("%m/%d/%Y")
                        X_Array.append(timedate)
                    #filter by Y Axis
                    if filter_y_axis == 'Hours':
                        hours = p['enginehours']
                        Y_Array.append(hours)
                    elif filter_y_axis == 'Km':
                        km = p['mileagekm']
                        Y_Array.append(km)
                    else:
                        Y_Array.append(p['mileage'])

                    hovertext.append(str(p['eventdesc'])+'<br>Date : '+str(timedate)+'<br>Week : '+str(p['timeweek'])+'<br>Calendar Week : '+str(p['timecalendarweek'])+'<br>Hours : '+str(p['enginehours'])+'<br>')
                    FT_Array.append(p['eventdesc'])

                context['data']         = chassis_information(filter_search)
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
def service(request,chassisid, eventid):
    context = {}
    #chassis event information
    result = chassis_event_information(chassisid,eventid)
    if result:
        eventname   = str(result[1])
        if(eventname == 'Engine Build'):
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        elif(eventname == 'Chassis Build'):
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        elif(eventname == 'Warranty Claim'):
            context['results']  = chassis_claim_information(chassisid)
            template = 'form/Claim.html'
        elif(eventname == 'service'):
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        elif(eventname == 'basic W'):
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        elif(eventname == 'basicE'):
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        else:
            context['data'] = chassis_information(chassisid)
            template = 'form/Case.html'
        context['service']  = result
        context['title']    = result[1]
        html_body = render_to_string(template, context)
        return HttpResponse(html_body)
    else:
        return HttpResponse('Invalid Request')


#Data export to csv
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_csv(request,token,x_axis,y_axis):
    #search chassis
    results = search_chassis_timeline(token)
    if results:
        X_Array     = []
        Y_Array     = []
        hovertext   = []
        for record in results:
            p = {'chassisid' : record[0], 'eventdesc' : record[1], 'timedate' : record[2], 'timeday' : record[3], 'timeweek' : record[4], 'timecalendarweek' : record[5], 'mileage' : record[6], 'mileagekm' : record[7], 'enginehours' : record[8], 'engineonly' : record[9], 'eventid' : record[10]}
            timedate = p['timedate']
            #filter by X Axis
            if x_axis == 'Week':
                timedate = timedate.strftime("%w %b %Y")
                X_Array.append('Week '+str(timedate))
            elif x_axis == 'Month':
                timedate = timedate.strftime("%b %Y")
                X_Array.append(timedate)
            else:
                timedate = timedate.strftime("%m/%d/%Y")
                X_Array.append(timedate)
            #filter by Y Axis
            if y_axis == 'Hours':
                hours = p['enginehours']
                Y_Array.append(hours)
            elif y_axis == 'Km':
                km = p['mileagekm']
                Y_Array.append(km)
            else:
                Y_Array.append(p['mileage'])

            hovertext.append(str(p['eventdesc'])+' /n Date : '+str(timedate)+'/n Week : '+str(p['timeweek'])+' /n Calendar Week : '+str(p['timecalendarweek'])+' /n Hours : '+str(p['enginehours']))
        
        response = HttpResponse(content_type='text/csv')
        filename = str(token)+'-Chassis-History-'+str(datetime.now())
        response['Content-Disposition'] = 'attachment; filename="'+str(filename)+'.csv"'
        writer = csv.writer(response)
        writer.writerow([x_axis, y_axis])
        if X_Array:
            for x in range(len(X_Array)):
                writer.writerow([X_Array[x], Y_Array[x]])
        return response

#data export to pdf
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf(request,token,x_axis,y_axis):
    #search chassis
    results = search_chassis_timeline(token)
    if results:
        X_Array     = []
        Y_Array     = []
        hovertext   = []
        for record in results:
            p = {'chassisid' : record[0], 'eventdesc' : record[1], 'timedate' : record[2], 'timeday' : record[3], 'timeweek' : record[4], 'timecalendarweek' : record[5], 'mileage' : record[6], 'mileagekm' : record[7], 'enginehours' : record[8], 'engineonly' : record[9], 'eventid' : record[10]}
            timedate = p['timedate']
            #filter by X Axis
            if x_axis == 'Week':
                timedate = timedate.strftime("%w %b %Y")
                X_Array.append('Week '+str(timedate))
            elif x_axis == 'Month':
                timedate = timedate.strftime("%b %Y")
                X_Array.append(timedate)
            else:
                timedate = timedate.strftime("%m/%d/%Y")
                X_Array.append(timedate)
            
            if y_axis == 'Hours':
                hours = p['enginehours']
                Y_Array.append(hours)
            elif y_axis == 'Km':
                km = p['mileagekm']
                Y_Array.append(km)
            else:
                Y_Array.append(p['mileage'])

            #text = str(p['eventdesc'])+' /n Date : '+str(timedate)+'/n Week : '+str(p['timeweek'])+' /n Calendar Week : '+str(p['timecalendarweek'])+' /n Hours : '+str(p['enginehours'])
            text = str(p['eventdesc'])
            hovertext.append(text)

        
        data = [go.Scatter(x=X_Array, y=Y_Array, mode='lines+markers', text=hovertext)]
        config   = {'scrollZoom': False,'displayModeBar': False,'editable': False}    
        layout = go.Layout(
            title= str(token)+' Chassis History',
            width=1200,
            height=800,
            xaxis=dict(
                title=str(x_axis),showgrid=False, zeroline=False
            ),
            yaxis=dict(
                title=str(y_axis),showgrid=False, zeroline=False
            )
            ,margin=go.layout.Margin( l=30, r=30, b=10, t=50, pad=5 )
        )

        filename = str(token)+'-Chassis-History-'+str(datetime.now())+'.pdf'

        fig = offline.plot({'data': data,
                            'layout': layout},
                            config = config,
                            auto_open=False,
                            show_link=False,
                            output_type='div', include_plotlyjs=True)

        opt = {'javascript-delay': 1000,'no-stop-slow-scripts': None,'debug-javascript': None}
        #pdfkit.from_string(fig, 'media/pdf/'+str(filename), options=opt)
        pdf = open('media/pdf/'+str(filename), 'rb')
        response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
        response['Content-Disposition'] = 'attachment; filename='+str(filename)
        pdf.close()
        return response  # returns the response.

#data export to pdf
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf_new(request,token,x_axis,y_axis):
    try:
        
        #search chassis
        results = search_chassis_timeline(token)
        if results:
            X_Array     = []
            Y_Array     = []
            hovertext   = []
            for record in results:
                p = {'chassisid' : record[0], 'eventdesc' : record[1], 'timedate' : record[2], 'timeday' : record[3], 'timeweek' : record[4], 'timecalendarweek' : record[5], 'mileage' : record[6], 'mileagekm' : record[7], 'enginehours' : record[8], 'engineonly' : record[9], 'eventid' : record[10]}
                timedate = p['timedate']
                testdate = p['timedate'].split(" ")
                timedate = datetime.strptime(testdate[0], '%d/%m/%y')
                #filter by X Axis
                if x_axis == 'Week':
                    timedate = timedate.strftime("%w %b %Y")
                    X_Array.append('Week '+str(timedate))
                elif x_axis == 'Month':
                    timedate = timedate.strftime("%b %Y")
                    X_Array.append(timedate)
                else:
                    #timedate = timedate.strftime("%Y %m %d")
                    print(type(timedate))
                    X_Array.append(timedate)
                
                if y_axis == 'Hours':
                    mileage = p['enginehours']
                    if float(mileage).is_integer():
                        mileage = int(mileage)
                    else:
                        mileage = float(mileage)
                    Y_Array.append(mileage)
                elif y_axis == 'Km':
                    mileage = p['mileagekm']
                    if float(mileage).is_integer():
                        mileage = int(mileage)
                    else:
                        mileage = float(mileage)
                    Y_Array.append(mileage)
                else:
                    mileage = p['mileage']
                    if float(mileage).is_integer():
                        mileage = int(mileage)
                    else:
                        mileage = float(mileage)
                    Y_Array.append(mileage)

                text = str(p['eventdesc'])+' <br/> Date : '+str(timedate)+'/n Week : '+str(p['timeweek'])+' /n Calendar Week : '+str(p['timecalendarweek'])+' /n Hours : '+str(p['enginehours'])
                hovertext.append(text)

        Data1 = {'x_axis': X_Array,'y_axis': Y_Array,'text': hovertext}
        df1 = DataFrame(Data1,columns=['x_axis','y_axis','text'])
        filename = str(token)+'-Chassis-History-'+str(uuid.uuid4())+'.pdf'
        
        '''
        year            = [datetime(2001, 11, 2),datetime(2002, 11, 2),datetime(2003, 11, 2),datetime(2004, 11, 2),datetime(2005, 11, 2),datetime(2006, 11, 2),datetime(2007, 11, 2),datetime(2008, 11, 2),datetime(2009, 11, 2),datetime(2010, 11, 2),datetime(2011, 11, 2),datetime(2012, 11, 2),datetime(2013, 11, 2),datetime(2014, 11, 2),datetime(2015, 11, 2),datetime(2016, 11, 2),datetime(2017, 11, 2),datetime(2018, 11, 2),datetime(2019, 11, 2)]
        tutorial_count  = [100, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000]
        plt.plot(year, tutorial_count, color="#6c3376", linewidth=3, marker='o')  
        plt.xlabel('Year')  
        plt.ylabel('Number of futurestud.io Tutorials')
        plt.savefig('media/pdf/line_plot.pdf', dpi=None, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None, metadata=None)
        plt.close()
        '''
        
        with PdfPages(r'media/pdf/'+str(filename)) as export_pdf:
            
            plt.plot(df1['x_axis'], df1['y_axis'], color='green', marker='o')
            plt.title('Chassis Time Frame History of '+str(token), fontsize=10)
            plt.xlabel(x_axis, fontsize=8)
            plt.ylabel(y_axis, fontsize=8)

            '''
            bbox_args = dict(boxstyle="round", fc="0.8")
            arrow_args = dict(arrowstyle = '<-', connectionstyle='arc3,rad=0')
            
            for i,text in enumerate(hovertext):
                x = X_Array[i]
                y = Y_Array[i]
                #offsetbox = TextArea(str(), minimumdescent=False)
                plt.annotate(
                    text,
                    xy=(x, y), xytext=(-10, 10),
                    textcoords='offset points', ha='right', va='bottom',
                    fontsize=8,
                    bbox=bbox_args,
                    arrowprops=arrow_args
                    )
            '''
            plt.grid(True)
            export_pdf.savefig()
            plt.close()
        
        pdf = open('media/pdf/'+str(filename), 'rb')
        response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
        response['Content-Disposition'] = 'attachment; filename='+str(filename)
        pdf.close()
        return response  # returns the response.

    except Exception as e:
      db_logger.exception(e)
      return []