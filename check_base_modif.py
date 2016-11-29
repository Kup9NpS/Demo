#-*- coding: utf-8 -*-
import os, time
import io
import csv
import win32com.client


def insert_into_base(modif, base, type, wheel_formula, baseTY, stand_number1, 
                     stand_number2, pos_number,stand_number3,stand_number4):
  connection = win32com.client.Dispatch(r'ADODB.Connection')
  DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=c:\\SCADA\\îìðîí\\Report source\\ÁàçàÀâòî.mdb;'
  recordset = win32com.client.Dispatch(r'ADODB.Recordset')
  connection.Open(DSN)
  print 'debug'
  query = 'INSERT INTO bases (modif, base, type, wheel_formula, baseTY, stand_number1, \
                              stand_number2, pos_number,stand_number3,stand_number4 ) \
                              VALUES ("{}","{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}" ,"{}" )'.format(
                              modif, base, type, wheel_formula, baseTY, stand_number1, 
                              stand_number2, pos_number,stand_number3,stand_number4)
  recordset.Open(query, connection, 1, 3)
  print 'debug'
 
path_to_watch = r"C:\\ftpfolder\\modif"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep(2)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  if added:
     try:
       os.chdir(path_to_watch) 
       with io.open(added[0], 'rb') as f:
          print "debug"
          fieldnames = ['modif', 'base', 'type', 'wheel_formula', 'baseTY', 'stand_number1', 
                              'stand_number2', 'pos_number','stand_number3','stand_number4']
          for row in csv.DictReader(f, fieldnames=fieldnames, delimiter = ";", quoting= csv.QUOTE_NONE ):
            print row
            stand_number4,wheel_formula,stand_number1,stand_number3,stand_number2,baseTY,pos_number,base, modif,type = row.values()
            print modif, base, type, wheel_formula, baseTY
            insert_into_base(modif, base, type, wheel_formula, baseTY, stand_number1, stand_number2, pos_number,stand_number3,stand_number4)
     except:
       pass
  before = after
