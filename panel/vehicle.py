from django.conf import settings
import psycopg2
import pandas as pd
from datetime import datetime
import logging
db_logger = logging.getLogger('django_auth')

#chassis information
def chassis_information(chassisid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("select * from dim_chassis where chassisid = '%s'" % (chassisid))
      df=cursor.fetchone()
      cursor.close()
      record = {}
      if(df):
         record['chassisid']                    = df[0] if df[0] else ''
         record['orderprocessingdivision']      = df[1] if df[1] else ''
         record['transmissionconfiguration']    = df[2] if df[2] else ''
         record['application']                  = df[3] if df[3] else ''
         record['aftertreatmentsoftwarelevel']  = df[4] if df[4] else ''
         record['vehicleidentificationnumber']  = df[5] if df[5] else ''
         record['rearaxleratio']                = df[6] if df[6] else ''
         record['inservicedate']                = df[7] if df[7] else ''
         record['deliverydate']                 = df[8] if df[8] else ''
         record['currentmileage']               = df[9] if df[9] else ''
         record['chassisbuildmonth']            = df[10] if df[10] else ''
         record['lastupdated']                  = df[11] if df[11] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#search chassis timeline
def search_chassis_timeline(search):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute(""" select 
                                    chassisid,eventdesc,timedate,timeday,timeweek,timecalendarweek,mileage,mileagekm,enginehours,engineonly,fact_timeline.eventid as eventid
                           from 
                                    fact_timeline
                                    join dim_event on fact_timeline.eventid = dim_event.eventid
                           where
                                    chassisid = '%s'
                           order by
                                    timedate ASC
                        """% (search))
      df=cursor.fetchall()
      cursor.close()
      return df
   except Exception as e:
      db_logger.exception(e)
      return []

#chassis event information
def chassis_event_information(chassisid,eventid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("select * from dim_event where eventid = '%s'" % (eventid))
      df=cursor.fetchone()
      cursor.close()
      return df
   except Exception as e:
      db_logger.exception(e)
      return []