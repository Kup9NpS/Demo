#-*- coding: utf-8 -*-
import os, time
import io
import csv
import win32com.client


def insert_into_base(vin_num, modif_num):
  connection = win32com.client.Dispatch(r'ADODB.Connection')
  DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=c:\\SCADA\\îìðîí\\Report source\\ÁàçàÀâòî.mdb;'
  recordset = win32com.client.Dispatch(r'ADODB.Recordset')
  connection.Open(DSN)
  print 'debug'
  query = 'INSERT INTO vin (modif, vin) VALUES ("{}","{}" )'.format(vin_num,modif_num)
  recordset.Open(query, connection, 1, 3)
  print 'debug'
 
path_to_watch = r"C:\\ftpfolder\\vin_code"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep(10)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  if added:
     try:
       os.chdir(path_to_watch) 
       with io.open(added[0], 'rb') as f:
          print "debug"
          fieldnames = ['modif','vin']
          for row in csv.DictReader(f, fieldnames=fieldnames, delimiter = ";", quoting= csv.QUOTE_NONE ):
            first,second = row.values()
            print first,second
            insert_into_base(first, second)
     except:
       pass
  before = after
