import win32com.client
import win32api
import csv
import io
from datetime import datetime

def get_field_names(recordset):
  field_names = [field.Name for field in recordset.Fields]
  return field_names

def has_rows(recordset):
  try:
    recordset.MoveFirst()
  except:
    return False
  return True

today = str(datetime.strftime(datetime.now(),"%d.%m.%Y"))
connection = win32com.client.Dispatch(r'ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:\\SCADA\\îìðîí\\ÀÇÓðàë.mdb;'
connection.Open(DSN)
recordset = win32com.client.Dispatch(r'ADODB.Recordset')
SQL = 'SELECT * FROM ×åòâåðòàÿ as four WHERE four.Äàòà = "{}" union \
SELECT * FROM Ïÿòàÿ as five WHERE five.Äàòà = "{}" union \
SELECT * FROM Âòîðàÿ as two WHERE two.Äàòà = "{}"'.format(today,today,today)
recordset.Open(SQL, connection, 1, 3)

field_names = get_field_names(recordset)
fieldnames = []
for name in field_names:
      if isinstance(name , unicode):
        name   = name .strip()

        if len(name  )==0:
           
          name   = None
        
        else:
            
          name  = name .encode("mbcs")
      fieldnames.append(name )
print fieldnames
with io.open('date.csv', 'wb') as f:
      result = csv.writer(f, delimiter = ";")
      result.writerow(fieldnames)
rows =list(zip(*recordset.GetRows(128)))
for set in rows:
   report = []  
   for row in set:
      if isinstance(row, unicode):
        row  = row.strip()

        if len(row )==0:
           
          row  = None
        
        else:
            
          row = row .encode("mbcs")
      report.append(row)
   with io.open('date.csv', 'ab') as f:
      result = csv.writer(f, delimiter = ";")
      result.writerow(report)
 

