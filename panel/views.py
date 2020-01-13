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

# This is the login function
# Which takes the data from the user as username and password 
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Check form validation
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = authenticate(username=username, password=password)
                # Check user is exist or not in the database
                if user is not None:
                    # If user is available the check he is active or not.
                    if user.is_active:
                        # If user is active then  redirect to dashboard page.
                        login(request, user)
                        db_logger.info('User Login : '+str(username)+' is successfully login.')
                        return redirect('/dashboard')
                    else:
                        # If user is inactive then display error and redirect to login page.
                        db_logger.warning('User Login : '+str(username)+' is inactive Username.')
                        messages.error(request, "'"+str(username)+"' is inactive Username.")
                        return redirect('/login')
                else:
                    # If user is none then display error and redirect to login page.
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
    # Return HTML page with context data.
    return render(request, 'login.html', context)

# This is the logout function
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
def logout_view(request):
    try:
        # If user logout successfully then redirect to login page
        db_logger.info('User Logout : '+str(request.user.username)+' is successfully logout.')
        logout(request)
        return redirect('/login')
    except Exception as e:
        return e

# This function is use to collect all information of user Dashboard.
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # Define required variables.
    context = {}
    filter_search       = ''
    filter_x_axis       = 'Day'
    filter_y_axis       = 'Miles'
    isData              = 'No'
    filter_Engine_Only  = 0

    DefaultMessage = 'Please search vehicle information using Chassis ID / ESN'
    # Check form is submit or not  with POST method.
    if request.method == "POST":
        # Get Form data
        filter_search       = request.POST.get('search')
        filter_x_axis       = request.POST.get('x-axis')
        filter_y_axis       = request.POST.get('y-axis')
        
        # Check filter_search textbox is null or not.
        if filter_search != '':
            # Check filter_Engine_Only checkbox is checked or not.
            if 'Engine_Only' in request.POST:
                filter_Engine_Only = 1
            # Get chassis information
            chassis_info = chassis_information(filter_search)
            # Check chassis information is null or not.
            if chassis_info:
                # Get the Chassis timeline data.
                results = search_chassis_timeline(filter_search, chassis_info['engineserialno'], filter_Engine_Only)
                # Check Chassis timeline data is null or not.
                if results:
                    I_Array     = []
                    X_Array     = []
                    Y_Array     = []
                    FT_Array    = []
                    hovertext   = []
                    Color_Array = []
                    Recors_data = []
                    for record in results:
                        p = {'shortvin' : record[0], 'eventid' : record[1], 'eventdesc' : record[2].strip(), 'timedate' : record[3], 'timeday' : record[4], 'timeweek' : record[5], 'timemonth': record[6],'timecalendarweek' : record[7], 'mileage' : record[8], 'mileagekm' : record[9], 'enginehours' : record[10], 'engineonly' : record[11]}
                        timedate    = p['timedate'].strftime("%m/%d/%Y")
                        old_formate = timedate
                        #I_Array.append(str(p['eventid']))
                        I_Array.append(str(p['eventid'])+'--'+str(p['timedate']))
 
                        # Filter By X axis, it must be Week, Month or Day
                        if filter_x_axis == 'Week':
                            X_Array.append(str(p['timeweek']))
                        elif filter_x_axis == 'Month':
                            X_Array.append(str(p['timemonth']))
                        else:
                            if filter_x_axis == 'Day':
                                X_Array.append(str(p['timeday']))

                        # Filter By Y axis, it must be Hours, Km or Mileage
                        if filter_y_axis == 'Hours':
                            hours = p['enginehours']
                            Y_Array.append(hours)
                        elif filter_y_axis == 'Km':
                            km = p['mileagekm']
                            Y_Array.append(km)
                        else:
                            Y_Array.append(p['mileage'])

                        # Specify color code of different services.
                        if(str(p['eventdesc']) == 'Engine Build'):
                            Color_Array.append('#007bff')
                        elif(str(p['eventdesc']) == 'Chassis Build'):
                            Color_Array.append('#ffc107')
                        elif(str(p['eventdesc']) == 'Warranty Claim'):
                            Color_Array.append('#28a745')
                        elif(str(p['eventdesc']) == 'FC'):
                            Color_Array.append('#dc3545')
                        else:
                            Color_Array.append('#17a2b8')

                        # Show hours as hh:mm:ss in datapoint hovertext
                        hover_hours = "{:.2f}".format(p['enginehours'])
                        
                        # Mileage value with 2 precision.
                        mileage = "{:.2f}".format(p['mileage'])

                        # Recors_data use to display timeline data in tabular form.
                        Recors_data.append({'id' : str(p['eventid'])+'--'+str(p['timedate']), 'eventdesc' : str(p['eventdesc']), 
                                            'timedate' : timedate, 'timeweek' : p['timeweek'], 
                                            'timecalendarweek' : p['timecalendarweek'], 'enginehours' : hover_hours,
                                            'eventid' : p['eventid'],
                                            'mileage': mileage,
                                           })
                        hovertext.append(str(p['eventdesc'])+'<br>Date : '+str(timedate)+'<br>Week : '+str(p['timeweek'])+'<br>Calendar Week : '+str(p['timecalendarweek'])+'<br>Hours : '+str(hover_hours)+'<br>')
                        FT_Array.append(p['eventdesc'])
                        
                    # Append required value to context dictionary
                    context['data']         = chassis_information(filter_search)
                    context['X_Array']      = json.dumps(X_Array)
                    context['Y_Array']      = json.dumps(Y_Array)
                    context['I_Array']      = json.dumps(I_Array)
                    context['hovertext']    = json.dumps(hovertext)
                    context['FT_Array']     = json.dumps(FT_Array)
                    context['Color_Array']  = json.dumps(Color_Array)
                    context['Recors_data']  = Recors_data
                    isData = 'Yes'
                else:
                    # Check Chassis timeline data is null then set error message.
                    DefaultMessage = 'Vehicle Information not found, Please try with other Chassis ID / ESN.'
            else:
                # Check chassis information is null then set error message.
                DefaultMessage = 'Vehicle Information not found, Please try with other Chassis ID / ESN.'

    # Append required value to context dictionary        
    context['filter_search'] = filter_search
    context['filter_x_axis'] = filter_x_axis
    context['filter_y_axis'] = filter_y_axis
    context['isData'] = isData
    context['DefaultMessage'] = DefaultMessage
    context['filter_Engine_Only'] = filter_Engine_Only
    
    # Return HTML page with context data.
    return render(request, 'dashboard.html', context)

# This function is use for open popup box.
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def service(request,shortvin, eventdata, engineonly):
    context = {}
    # Get chassis event information.
    eventdata   = eventdata.split('--')
    eventid     = eventdata[0]
    eventdate   = eventdata[1]
    result = chassis_event_information(eventid)
    # Check chassis event information is null or not.
    if result:
        eventname       = str(result[1])
        # Get chassis information.
        chassis_info    = chassis_information(shortvin)
        # If eventname is Engine Build then get CEP data and open CEP popup box
        if(eventname == 'Engine Build'):
            context['data'] = cep_data_information(shortvin, chassis_info['engineserialno'])
            template = 'form/CEP.html'
        # If eventname is Chassis Build then get Plant data and open Plant popup box
        elif(eventname == 'Chassis Build'):
            context['data'] = plant_data_information(shortvin, chassis_info['engineserialno'])
            template = 'form/Plant.html'
        # If eventname is Warranty Claim then get Claim data and open Claim popup box
        elif(eventname == 'Warranty Claim'):
            context['results']  = claim_information(shortvin,chassis_info['engineserialno'], eventdate)
            template = 'form/Claim.html'
        # If eventname is Campaign Claim then get Claim data and open Claim popup box
        elif(eventname == 'Campaign Claim'):
            context['results'] = claim_information(shortvin, chassis_info['engineserialno'], eventdate)
            template = 'form/Claim.html'
        # If eventname is FC then get Fault Code data and open Fault Code popup box
        elif(eventname == 'FC'):
            context['data'] = fault_code_information(shortvin,chassis_info['engineserialno'],eventdate)
            template = 'form/Fault_code.html'
        # If eventname is Basic Warranty Period then get Case data and open Case popup box
        elif(eventname == 'Basic Warranty Period'):
            context['data'] = chassis_information(shortvin)
            template = 'form/Case.html'
        # If eventname is Basic Engine Warranty Period then get Case data and open Case popup box
        elif(eventname == 'Basic Engine Warranty Period'):
            context['data'] = chassis_information(shortvin)
            template = 'form/Case.html'
        else:
            context['data'] = chassis_information(shortvin)
            template = 'form/Case.html'
        # Append value to context dictionary
        context['service']  = result
        context['title']    = result[1]
        html_body = render_to_string(template, context)
        
        # Return HTML template with context dictionary
        return HttpResponse(html_body)
    else:
        return HttpResponse('Invalid Request')

# This function is use for Export as CSV.
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_csv(request, token, x_axis, y_axis, engineonly):
    # Convert str to int
    engineonly = int(engineonly)
    # Get chassis information
    chassis_info = chassis_information(token)
    # Get chassis timeline information
    results = search_chassis_timeline(token, chassis_info['engineserialno'], engineonly)
    # Check chassis timeline information is null or not
    if results:
        Recors_data = []
        X_Array = []
        Y_Array = []
        # Get one by one result
        for record in results:
            p = {'shortvin' : record[0], 'eventid' : record[1], 'eventdesc' : record[2].strip(), 'timedate' : record[3], 'timeday' : record[4], 'timeweek' : record[5], 'timemonth': record[6],'timecalendarweek' : record[7], 'mileage' : record[8], 'mileagekm' : record[9], 'enginehours' : record[10], 'engineonly' : record[11]}
            timedate = p['timedate'].strftime("%m/%d/%Y")
            old_formate = timedate

            # Filter By X axis, it must be Week, Month or Day
            if x_axis == 'Week':
                X_Array.append(str(p['timeweek']))
            elif x_axis == 'Month':
                X_Array.append(str(p['timemonth']))
            else:
                if x_axis == 'Day':
                    X_Array.append(str(p['timeday']))

            # Filter By Y axis, it must be Hours, Km or Mileage
            if y_axis == 'Hours':
                hours = p['enginehours']
                Y_Array.append(hours)
            elif y_axis == 'Km':
                km = p['mileagekm']
                Y_Array.append(km)
            else:
                Y_Array.append(p['mileage'])

            # Engine hours with 2 precision floating point
            hover_hours = "{:.2f}".format(p['enginehours'])

            # Recors_data use to collect required information for CSV file.
            Recors_data.append({'eventdesc': str(p['eventdesc']),
                                'timedate': timedate, 'timeweek': p['timeweek'],
                                'timecalendarweek': p['timecalendarweek'], 'enginehours': hover_hours,
                                'eventid': p['eventid'],
                                'mileage': p['mileage'],
                               })

        response = HttpResponse(content_type='text/csv')
        # Define CSV filename.
        filename = str(token)+'-Chassis-History-'+str(datetime.now())
        response['Content-Disposition'] = 'attachment; filename="'+str(filename)+'.csv"'
        writer = csv.writer(response)
        
        # Write heading in CSV file.
        writer.writerow(['Service','Date','Week','Calender Week', 'Hours', 'Mileage', 'View'
                         #'X-axis[' + x_axis + ']',
                         #'Y-axis[' + y_axis + ']'
                         ])
        # If Recors_data is not null then perform following task
        if Recors_data:
            # Get one by one Recors_data
            for record in Recors_data:
                # For event description
                if record['eventdesc'] == 'Engine Build':
                    view = 'CEP Data'
                elif record['eventdesc'] == 'Chassis Build':
                    view = 'Plant Data'
                elif record['eventdesc'] == 'Warranty Claim':
                    view = 'Claim Info'
                elif record['eventdesc'] == 'FC':
                    view = 'Fault code'
                else:
                    view = record['eventdesc']
                    
                # Write information in CSV file.
                writer.writerow([record['eventdesc'],
                                record['timedate'],
                                record['timeweek'],
                                record['timecalendarweek'],
                                record['enginehours'],
                                record['mileage'],
                                view
                                #X_Array[counter],
                                #Y_Array[counter]
                                ])
        return response

# This function is use for Export as PDF.
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf(request,token,x_axis,y_axis,engineonly):
    # Get chassis timeline information
    results = search_chassis_timeline(token,engineonly)
    # Check chassis timeline information is null or not
    if results:
        X_Array     = []
        Y_Array     = []
        hovertext   = []
        for record in results:
            p = {'shortvin' : record[0], 'eventid' : record[1], 'eventdesc' : record[2].strip(), 'timedate' : record[3], 'timeday' : record[4], 'timeweek' : record[5], 'timemonth': record[6],'timecalendarweek' : record[7], 'mileage' : record[8], 'mileagekm' : record[9], 'enginehours' : record[10], 'engineonly' : record[11]}
            timedate = p['timedate'].strftime("%m/%d/%Y")
            
            # Filter By X axis, it must be Week, Month or Day
            if x_axis == 'Week':
                X_Array.append(str(p['timeweek']))
            elif x_axis == 'Month':
                X_Array.append(str(p['timemonth']))
            else:
                if x_axis == 'Day':
                    X_Array.append(str(p['timeday']))

            # Filter By Y axis, it must be Hours, Km or Mileage
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
        
        # Define filename
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
        # Generates the response as pdf response.
        response = HttpResponse(pdf.read(), content_type='application/pdf')  
        response['Content-Disposition'] = 'attachment; filename='+str(filename)
        # Close PDF connection.
        pdf.close()
        # Returns the response.
        return response 

# This function is use for Export as PDF.
# User login is the first priority of this view.
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf_new(request,token,x_axis,y_axis,engineonly):
    try:
        
        # Get chassis timeline information
        results = search_chassis_timeline(token,engineonly)
        # Check chassis timeline information is null or not
        if results:
            # Define null lists
            X_Array     = []
            Y_Array     = []
            hovertext   = []
            # Get one by one result
            for record in results:
                p = {'shortvin' : record[0], 'eventid' : record[1], 'eventdesc' : record[2].strip(), 'timedate' : record[3], 'timeday' : record[4], 'timeweek' : record[5], 'timemonth': record[6],'timecalendarweek' : record[7], 'mileage' : record[8], 'mileagekm' : record[9], 'enginehours' : record[10], 'engineonly' : record[11]}
                timedate = p['timedate'].strftime("%m/%d/%Y")
                testdate = p['timedate'].split(" ")
                timedate = datetime.strptime(testdate[0], '%m/%d/%y')
 
                # Filter By X axis, it must be Week, Month or Day
                if x_axis == 'Week':
                    X_Array.append(str(p['timeweek']))
                elif x_axis == 'Month':
                    X_Array.append(str(p['timemonth']))
                else:
                    if x_axis == 'Day':
                        X_Array.append(str(p['timeday']))

                # Filter By Y axis, it must be Hours, Km or Mileage
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
        
        # Define filename
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
        # Generates the response as pdf response.
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+str(filename)
        # Close PDF connection.
        pdf.close()
        # Returns the response.
        return response
    except Exception as e:
      db_logger.exception(e)
      return []

