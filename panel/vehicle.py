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
      cursor.execute("""select 
                              d.*,
                              c.engineserialno,
                              c.enginefamilyname,
                              c.enginemodelname,
                              c.eniginemodelyear,
                              c.breakdownengineconfiguration,
                              c.hprating,
                              c.truckmodel,
                              c.currentsoftwarelevel,
                              c.lastsoftwarelevel
                        from 
                              dim_chassis as d
                              join dim_engine c on d.chassisid = c.chassisid 
                        where 
                              d.chassisid = '%s'""" % (chassisid))

      #cursor.execute("""select distinct dim_engine.chassisid,currentmileage, transmissionconfiguration, application,aftertreatmentsoftwarelevel,rearaxleration from dim_chassis on dim_chassis.chassisid=dim_engine.chassisid where dim_chassis.chassisid = '%s' or dim_engine.engineserialno = '%s' order by dim_chassis.chassisid""" % (chassisid,enginenum))
      df=cursor.fetchone()
      #fields = [item[0] for item in cursor.description]
      cursor.close()
      record = {}
      if(df):
         '''
         record['chassisid']                    = df[0] if df[0] else ''
         record['eventid']      = df[1] if df[1] else ''
         record['eventdesc']    = df[2] if df[2] else ''
         record['timedate']                  = df[3] if df[3] else ''
         record['timeday']  = df[4] if df[4] else ''
         record['timeweek']  = df[5] if df[5] else ''
         record['enginehours']                = df[6] if df[6] else ''
         record['engineonly']                = df[7] if df[7] else ''
         '''
         # record['lastsoftwarelevel']                 = df[8] if df[8] else ''
         # record['transmissionconfiguration']               = df[9] if df[9] else ''
         # record['currentmileage']            = df[10] if df[10] else ''
         # record['aftertreatmentsoftwarelevel']                  = df[11] if df[11] else ''
         # record['rearaxleratio']                  = df[12] if df[12] else ''
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
         record['engineserialno']               = df[12] if df[12] else ''
         record['enginefamilyname']             = df[13] if df[13] else ''
         record['enginemodelname']              = df[14] if df[14] else ''
         record['eniginemodelyear']             = df[15] if df[15] else ''
         record['breakdownengineconfiguration'] = df[16] if df[16] else ''
         record['hprating']                     = df[17] if df[17] else ''
         record['truckmodel']                   = df[18] if df[18] else ''
         record['currentsoftwarelevel']         = df[19] if df[19] else ''
         record['lastsoftwarelevel']            = df[20] if df[20] else ''


      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#search chassis timeline
def search_chassis_timeline(search,engineonly):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      if engineonly == 1:
         cursor.execute(""" select 
                                    distinct   chassisid,eventdesc,timedate,timeday,timeweek,timecalendarweek,mileage,mileagekm,enginehours,engineonly,fact_timeline.eventid as eventid
                              from 
                                       fact_timeline
                                       join dim_event on fact_timeline.eventid = dim_event.eventid
                              where
                                       chassisid = '%s'
                                       and
                                       engineonly = 1
                              order by
                                       timedate ASC
                           """% (search))
      else:
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
            cursor.execute('''select * from "fact_claimparts" where claimid= '%s' ''' % (fact_claim['claimid']))
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

def plant_timeline(chassisid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("select * from fact_timeline where chassisid = '%s'" % (chassisid))
      df=cursor.fetchone()
      cursor.close()
      return df
   except Exception as e:
      db_logger.exception(e)
      return []

def fact_case_information(chassisid):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("select * from fact_case where chassisid = '%s'" % (chassisid))
      df=cursor.fetchall()
      data = []
      if df:
         for record in df:
            fact_case = {'caseid' : record['caseid'].strip(),'casedate':record['casedate'].strip(),'claimid':record['claimid'].strip(),'attachid':record['attachmentid'].strip(),'lastupdated':record['lastupdated'].strip()}
            cursor.execute('''select * from "dim_case" where caseid = '%s'"''' % (fact_case['caseid']))
            case = cursor.fetchone()
            if case:
               fact_case['disposition'] = case['disposition'].strip()
               fact_case['lastupdated'] = case['lastupdated'].strip()
               fact_case['messages'] = case['messages'].strip()
            data.append(fact_case)
      cursor.close()
      return data
   except Exception as e:
      db_logger.exception(e)
      return []

'''
#CEP Data information
def cep_data_information(chassisid,engineserialno):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("""select 
                              distinct 
                              dim_engine.chassisid,currentmileage, transmissionconfiguration, application,aftertreatmentsoftwarelevel,rearaxleration 
                        from 
                              dim_chassis on dim_chassis.chassisid=dim_engine.chassisid 
                        where 
                              dim_chassis.chassisid = '%s'
                              or 
                              dim_engine.engineserialno = '%s'
                        order by 
                              dim_chassis.chassisid"""% (chassisid,engineserialno))
      df=cursor.fetchall()
      cursor.close()
      record = {}
      if(df):
         record['chassisid']                    = df[0] if df[0] else ''
         record['currentmileage']               = df[1] if df[1] else ''
         record['transmissionconfiguration']    = df[2] if df[2] else ''
         record['application']                  = df[3] if df[3] else ''
         record['aftertreatmentsoftwarelevel']  = df[4] if df[4] else ''
         record['rearaxleration']               = df[5] if df[5] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []
'''

#CEP Data information
def cep_data_information(chassisid,engineserialno):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("""SELECT DISTINCT  d.*,
                              c.engineserialno,
                              c.enginefamilyname,
                              c.enginemodelname,
                              c.eniginemodelyear,
                              c.breakdownengineconfiguration,
                              c.hprating,
                              c.truckmodel,
                              c.currentsoftwarelevel,
                              c.lastsoftwarelevel
                        FROM 
                              dim_chassis  as d  
                        JOIN dim_engine c on d.chassisid = c.chassisid 
                        WHERE 
                              d.chassisid = '%s'
                              or 
                              c.engineserialno = '%s'
                        ORDER BY
                              d.chassisid"""% (chassisid,engineserialno))
      df=cursor.fetchone()
      cursor.close()
      record = {}
      if(df):
          record['chassisid'] = df[0] if df[0] else ''
          record['orderprocessingdivision'] = df[1] if df[1] else ''
          record['transmissionconfiguration'] = df[2] if df[2] else ''
          record['application'] = df[3] if df[3] else ''
          record['aftertreatmentsoftwarelevel'] = df[4] if df[4] else ''
          record['vehicleidentificationnumber'] = df[5] if df[5] else ''
          record['rearaxleratio'] = df[6] if df[6] else ''
          record['inservicedate'] = df[7] if df[7] else ''
          record['deliverydate'] = df[8] if df[8] else ''
          record['currentmileage'] = df[9] if df[9] else ''
          record['chassisbuildmonth'] = df[10] if df[10] else ''
          record['lastupdated'] = df[11] if df[11] else ''
          record['engineserialno'] = df[12] if df[12] else ''
          record['enginefamilyname'] = df[13] if df[13] else ''
          record['enginemodelname'] = df[14] if df[14] else ''
          record['eniginemodelyear'] = df[15] if df[15] else ''
          record['breakdownengineconfiguration'] = df[16] if df[16] else ''
          record['hprating'] = df[17] if df[17] else ''
          record['truckmodel'] = df[18] if df[18] else ''
          record['currentsoftwarelevel'] = df[19] if df[19] else ''
          record['lastsoftwarelevel'] = df[20] if df[20] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []



#Plant Data information
def plant_data_information(chassisid,engineserialno):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("""select 
                              distinct 
                              dim_engine.chassisid,currentmileage, transmissionconfiguration, application,aftertreatmentsoftwarelevel,rearaxleration 
                        from 
                              dim_chassis on dim_chassis.chassisid=dim_engine.chassisid 
                        where 
                              dim_chassis.chassisid = '%s'
                              or 
                              dim_engine.engineserialno = '%s'
                        order by 
                              dim_chassis.chassisid"""% (chassisid,engineserialno))
      df=cursor.fetchall()
      cursor.close()
      record = {}
      if(df):
         record['chassisid']                    = df[0] if df[0] else ''
         record['currentmileage']               = df[1] if df[1] else ''
         record['transmissionconfiguration']    = df[2] if df[2] else ''
         record['application']                  = df[3] if df[3] else ''
         record['aftertreatmentsoftwarelevel']  = df[4] if df[4] else ''
         record['rearaxleration']               = df[5] if df[5] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#Claim information
def claim_information(chassisid,engineserialno,eventdate):
   try:
      claimdate   = parse(eventdate)
      year        = claimdate.strftime('%Y')
      month       = claimdate.strftime('%m')
      day         = claimdate.strftime('%d')
      claimdate   = claimdate.strftime("%m/%d/%y %H:%M")
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("""select 
                                 c.claimid, c.dealerstory, c.propart, c.proamount, c.compaignid, c.bulletlink,cp.partno, cp.partdesc, cp.partmat, cp.partsource, cp.partaty 
                        from 
                                 dim_cliam as c 
                                 join dim_engine as e on c.chassisid = e.chassisid 
                                 join fact_claimparts as cp on cp.claimid = c.claimid 
                        where 
                                 extract (year from c.reportdate) = '%s' 
                                 and 
                                 extract (month from c.reportdate) = '%s' 
                                 and 
                                 extract (day from c.reportdate) = '%s' 
                                 and 
                                 (c.chassisid = '%s' or e.engineserialno = '%s')
                                 """% (year,month,day,chassisid,engineserialno))
      df=cursor.fetchall()
      cursor.close()
      data = []
      if df:
         for record in df:
            r = {'claimid' : record[0].strip(), 'dealerstory' : record[1].strip(),'propart' : record[2].strip(), 'proamount' : record[3].strip(),'compaignid' : record[4].strip(), 'bulletlink' : record[5].strip(),'partno' : record[6].strip(), 'partdesc' : record[7].strip(),'partmat' : record[8].strip(), 'partsource' : record[9].strip(), 'partaty' : record[10].strip()}
            data.append(r)
      cursor.close()
      return data
   except Exception as e:
      db_logger.exception(e)
      return []

#fault code information
def fault_code_information(chassisid,engineserialno,eventdate):
   try:
      claimdate   = parse(eventdate)
      year        = claimdate.strftime('%Y')
      month       = claimdate.strftime('%m')
      day         = claimdate.strftime('%d')
      claimdate   = claimdate.strftime("%m/%d/%y %H:%M")
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      cursor.execute("""select 
                                 distinct 
                                 f.faultcode, f.faultdesc 
                        from 
                                 fact_faultcode f 
                                 join dim_chassis c on f.chassisid = c.chassisid 
                                 join dim_engine e on c.chassisid  = e.chassisid 
                                 join fact_timeline ft on ft.chassisid = c.chassisid 
                        Where 
                                 extract(year from f.faultdate) = '%s' 
                                 and 
                                 extract(month from f.faultdate) = '%s' 
                                 and 
                                 extract(day from f.faultdate) = '%s' 
                                 and 
                                 (c.chassisid = '%s' or e.engineserialno = '%s')
                                 """% (year,month,day,chassisid,engineserialno))
      df=cursor.fetchall()
      cursor.close()
      data = []
      if df:
         for record in df:
            r = {'faultcode' : record[0].strip(), 'faultdesc' : record[1].strip()}
            data.append(r)
      cursor.close()
      return data
   except Exception as e:
      db_logger.exception(e)
      return []

