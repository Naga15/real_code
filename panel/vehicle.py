from django.conf import settings
import psycopg2
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import logging
db_logger = logging.getLogger('django_auth')

#chassis information
def chassis_information(shortvin):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      query = ("""SELECT  
                  ce.shortvin, ce.enginefamilyname, ce.engineserialno, ce.enginemodelyear, 
                  ce.breakdownengineconfiguration, c.currentmileage, ce.hprating,
                  ce.truckmodel, ce.currentsoftwarelevel, ce.lastsoftwarelevel, 
                  c.transmissionconfiguration,c.aftertreatmentsoftwarelevel, c.rearaxleratio
               FROM dim_chassis as c 
                  JOIN dim_engine ce ON c.shortvin = ce.shortvin  
                  WHERE c.shortvin = '%s'
                  or ce.engineserialno = '%s'
                  """ % (shortvin, shortvin))
      cursor.execute(query)
      df=cursor.fetchone()
      cursor.close()
      record = {}
      if(df):
         record['shortvin']                    = df[0] if df[0] else ''
         record['enginefamilyname']      = df[1] if df[1] else ''
         record['engineserialno']    = df[2] if df[2] else ''
         record['enginemodelyear']                  = df[3] if df[3] else ''
         record['breakdownengineconfiguration']  = df[4] if df[4] else ''
         record['currentmileage']  = df[5] if df[5] else ''
         record['hprating']                = df[6] if df[6] else ''
         record['truckmodel']                = df[7] if df[7] else ''
         record['currentsoftwarelevel']                 = df[8] if df[8] else ''
         record['lastsoftwarelevel']               = df[9] if df[9] else ''
         record['transmissionconfiguration']            = df[10] if df[10] else ''
         record['aftertreatmentsoftwarelevel']                  = df[11] if df[11] else ''
         record['rearaxleratio']               = df[12] if df[12] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#search chassis timeline
def search_chassis_timeline(shortvin, engineserialno, engineonly):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      if engineonly == 1:
         query = (""" 
         SELECT 
         t.shortvin, t.eventid, e.eventdesc, t.timedate, t.timeday, t.timeweek, t.timecalendarweek, t.mileage, t.mileagekm,
         t.enginehours, t.engineonly 
         FROM fact_timeline t
         JOIN dim_event e on t.eventid = e.eventid
         JOIN dim_engine ce on t.shortvin = ce.shortvin
         WHERE (t.shortvin = '%s' or ce.engineserialno = '%s') AND
         ((t.engineonly = 1 and t.eventid in (3,4,5,7)) or t.engineonly is null and t.eventid 
         not in (3,4,5,7)) 
         ORDER BY t.eventid """ % (shortvin, engineserialno))
         #print(query)
         cursor.execute(query)
      else:
         query = ("""  
         SELECT  
         t.shortvin, t.eventid, e.eventdesc, t.timedate, t.timeday, t.timeweek, t.timecalendarweek, t.mileage, t.mileagekm, 
         t.enginehours, t.engineonly  
         FROM fact_timeline t 
         JOIN dim_event e ON t.eventid = e.eventid 
         JOIN dim_engine ce ON t.shortvin = ce.shortvin 
         WHERE t.shortvin = '%s' or ce.engineserialno = '%s' 
         order by t.timedate """ % (shortvin, engineserialno))
         #print(query)
         cursor.execute(query)

      df=cursor.fetchall()
      cursor.close()
      return df
   except Exception as e:
      db_logger.exception(e)
      return []

#chassis event information
def chassis_event_information(eventid):
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

#CEP Data information
def cep_data_information(shortvin, engineserialno):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      query = (""" 
               SELECT 
               ce.shortvin, ce.engineserialno, ce.enginefamilyname, ce.enginemodelyear, 
               ce.breakdownengineconfiguration, ce.hprating, ce.truckmodel, 
               ce.currentsoftwarelevel, ce.lastsoftwarelevel, c.currentmileage 
               FROM dim_chassis c  
               JOIN dim_engine ce ON c.shortvin = ce.shortvin 
               WHERE  
               c.shortvin = '%s'  
               OR 
               ce.engineserialno = '%s' 
               """ % (shortvin, engineserialno))
      cursor.execute(query)
      df=cursor.fetchone()
      cursor.close()
      record = {}
      if (df):
         record['shortvin'] = df[0] if df[0] else ''
         record['engineserialno'] = df[1] if df[1] else ''
         record['enginefamilyname'] = df[2] if df[2] else ''
         record['enginemodelyear'] = df[3] if df[3] else ''
         record['breakdownengineconfiguration'] = df[4] if df[4] else ''
         record['currentmileage'] = df[5] if df[5] else ''
         record['hprating'] = df[6] if df[6] else ''
         record['truckmodel'] = df[7] if df[7] else ''
         record['currentsoftwarelevel'] = df[8] if df[8] else ''
         record['lastsoftwarelevel'] = df[9] if df[9] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#Plant Data information
def plant_data_information(shortvin, engineserialno):
   try:
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      query = (""" 
              SELECT  
              ce.shortvin, c.transmissionconfiguration, c.application, 
              c.currentmileage,c.aftertreatmentsoftwarelevel, 
              c.rearaxleratio  
              FROM dim_chassis c  
              JOIN dim_engine ce ON c.shortvin = ce.shortvin WHERE  
              c.shortvin = '%s'  
              OR  
              ce.engineserialno = '%s'  
              """ % (shortvin, engineserialno))
      cursor.execute(query)
      df=cursor.fetchall()
      cursor.close()
      record = {}
      if(df):
         record['shortvin']                    = df[0] if df[0] else ''
         record['transmissionconfiguration']               = df[1] if df[1] else ''
         record['application']    = df[2] if df[2] else ''
         record['currentmileage']                  = df[3] if df[3] else ''
         record['aftertreatmentsoftwarelevel']  = df[4] if df[4] else ''
         record['rearaxleratio']               = df[5] if df[5] else ''
      return record
   except Exception as e:
      db_logger.exception(e)
      return []

#Claim information
def claim_information(shortvin, engineserialno, eventdate):
   try:
      claimdate   = parse(eventdate)
      year        = claimdate.strftime('%Y')
      month       = claimdate.strftime('%m')
      day         = claimdate.strftime('%d')
      claimdate   = claimdate.strftime("%m/%d/%y %H:%M")
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      query = (""" 
              SELECT  
              cl.claimid, cl.dealerstory, cl.propart, cl.prolabor, cl.proamount, cl.campaignid,  
              cl.bulletlink, cp.partno, cp.partdesc, cp.partamt, cp.partsource, cp.partqty 
              FROM dim_claim cl  
              JOIN dim_engine ce on cl.shortvin = ce.shortvin  
              JOIN dim_claimparts cp on cp.claimid = cl.claimid 
              WHERE  
              extract(year from cl.reportdate) = '%s'  
              AND  
              extract(month from cl.reportdate) = '%s'  
              AND  
              extract(day from cl.reportdate) = '%s'  
              AND  
              (cl.shortvin = '%s' OR ce.engineserialno = '%s')"""
               % (year, month, day, shortvin, engineserialno))
      cursor.execute(query)
      df=cursor.fetchall()
      cursor.close()
      data = []
      if df:
         for record in df:
            r = {
                  'claimid': record[0].strip(),
                  'dealerstory': record[1].strip(),
                  'propart': record[2],
                  'prolabor': record[3],
                  'proamount': record[4],
                  'campaignid': record[5].strip(),
                  'bulletlink': record[6].strip(),
                  'partno': record[7].strip(),
                  'partdesc': record[8].strip(),
                  'partamount': record[9],
                  'partsource': record[10].strip(),
                  'partqty': record[10].strip(),
               }
            data.append(r)
      return data
   except Exception as e:
      db_logger.exception(e)
      return []

#fault code information
def fault_code_information(shortvin,engineserialno,eventdate):
   try:
      claimdate   = parse(eventdate)
      year        = claimdate.strftime('%Y')
      month       = claimdate.strftime('%m')
      day         = claimdate.strftime('%d')
      claimdate   = claimdate.strftime("%m/%d/%y %H:%M")
      con = psycopg2.connect(database = settings.AUTHENTICATION_DATABASE_NAME, host=settings.AUTHENTICATION_HOST, port=settings.AUTHENTICATION_PORT, user =settings.AUTHENTICATION_USERNAME,password=settings.AUTHENTICATION_PASSWORD)
      cursor=con.cursor()
      query = ("""  
               SELECT DISTINCT  
               f.faultcode, f.faultdesc, f.mileage  
               from dim_faultcode f  
               JOIN dim_chassis c on f.shortvin = c.shortvin  
               JOIN dim_engine ce on c.shortvin = ce.shortvin   
               WHERE  
               extract(year from f.faultdate) = '%s'  
               AND  
               extract(month from f.faultdate) = '%s'  
               AND  
               extract(day from f.faultdate) = '%s'  
               AND  
               (c.shortvin = '%s' OR ce.engineserialno = '%s')"""
               % (year, month, day, shortvin, engineserialno))
      cursor.execute(query)
      df=cursor.fetchall()
      cursor.close()
      data = []
      if df:
         for record in df:
            r = {
                  'faultcode' : record[0].strip(),
                  'faultdesc' : record[1].strip(),
                  'mileage': record[2],
                 }
            data.append(r)
      return data
   except Exception as e:
      db_logger.exception(e)
      return []

