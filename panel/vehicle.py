from django.conf import settings
import psycopg2
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import logging
db_logger = logging.getLogger('django_auth')

#chassis information
def chassis_information(chassisid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      # cursor.execute("select * from dim_chassis where chassisid = '%s'" % (chassisid))
      cursor.execute("""select distinct public.dim_engine.chassisid,public.dim_engine.enginefamilyname,
public.dim_engine.engineserialno,eniginemodelyear,dim_engine.breakdownengineconfiguration,
hprating,truckmodel,currentsoftwarelevel,lastsoftwarelevel,
transmissionconfiguration,currentmileage,aftertreatmentsoftwarelevel,rearaxleratio
from public.dim_chassis
join  public.dim_engine on public.dim_chassis.chassisid = public.dim_engine.chassisid
where dim_chassis.chassisid = '%s'
order by public.dim_chassis.chassisid                     """ % (chassisid))




      df=cursor.fetchone()
      cursor.close()
      record = {}
      if(df):
         record['chassisid']                    = df[0] if df[0] else ''
         record['enginefamilyname']      = df[1] if df[1] else ''
         record['engineserialno']    = df[2] if df[2] else ''
         record['eniginemodelyear']                  = df[3] if df[3] else ''
         record['breakdownengineconfiguration']  = df[4] if df[4] else ''
         record['hprating']  = df[5] if df[5] else ''
         record['truckmodel']                = df[6] if df[6] else ''
         record['currentsoftwarelevel']                = df[7] if df[7] else ''
         record['lastsoftwarelevel']                 = df[8] if df[8] else ''
         record['transmissionconfiguration']               = df[9] if df[9] else ''
         record['currentmileage']            = df[10] if df[10] else ''
         record['aftertreatmentsoftwarelevel']                  = df[11] if df[11] else ''
         record['rearaxleratio']                  = df[12] if df[12] else ''

         # record['chassisid']                    = df[0] if df[0] else ''
         # record['engineserialno']      = df[1] if df[1] else ''
         # record['transmissionconfiguration']    = df[2] if df[2] else ''
         # record['application']                  = df[3] if df[3] else ''
         # record['aftertreatmentsoftwarelevel']  = df[4] if df[4] else ''
         # record['vehicleidentificationnumber']  = df[5] if df[5] else ''
         # record['rearaxleratio']                = df[6] if df[6] else ''
         # record['inservicedate']                = df[7] if df[7] else ''
         # record['deliverydate']                 = df[8] if df[8] else ''
         # record['currentmileage']               = df[9] if df[9] else ''
         # record['chassisbuildmonth']            = df[10] if df[10] else ''
         # record['lastupdated']                  = df[11] if df[11] else ''

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
                                 distinct   chassisid,eventdesc,timedate,timeday,timeweek,timecalendarweek,mileage,mileagekm,enginehours,engineonly,fact_timeline.eventid as eventid
                           from 
                                    fact_timeline
                                    join dim_event on fact_timeline.eventid = dim_event.eventid
                           where
                                    chassisid = '%s'
                           order by
                                    timedate ASC
                        """% (search))
      # cursor.execute(""" select 
      #                 distinct   chassisid,eventdesc,timedate,timeday,timeweek,timecalendarweek,mileage,mileagekm,enginehours,engineonly,fact_timeline.eventid as eventid
      #                      from public.fact_timeline
      #                      join public.dim_event on public.fact_timeline.eventid = public.dim_event.eventid
      #                      where chassisid = '%s'
      #                      order by public.fact_timeline.eventid
      #                   """% (search))
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

#chassis claim information
def chassis_claim_information(chassisid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("select * from fact_claim where chassisid = '%s'" % (chassisid))
      df=cursor.fetchall()
      data = []
      if df:
         for record in df:
            #claimdate   = parse(record[1].strip())
            #claimdate   = claimdate.strftime("%m/%d/%Y")
            fact_claim = {'claimdate' : record[1].strip(), 'claimid' : record[2].strip(), 'lastupdated' : record[3].strip()}
            #get claim parts
            cursor.execute("select * from fact_claimparts where claimid = '%s'" % (fact_claim['claimid']))
            parts=cursor.fetchone()
            if parts:
               fact_claim['partno']       = parts[1].strip()
               fact_claim['partdesc']     = parts[2].strip()
               fact_claim['partamt']      = parts[3].strip()
               fact_claim['partsource']   = parts[4].strip()
               fact_claim['partqty']      = parts[5].strip()
            data.append(fact_claim)
      cursor.close()
      return data
   except Exception as e:
      db_logger.exception(e)
      return []
