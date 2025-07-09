import pyodbc
import numpy as np
from pandas import DataFrame
server = 'itamco-mtconnect.database.windows.net'
database = 'MTConnectData'
username = 'MTConnectData'
password = 'MTConnect2021'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query
cursor.execute("SELECT TOP (10000000) [machineid],[name],[value],[recordtimestamp] FROM [dbo].[VwMTConnectData] where recordtimestamp > '2022-12-12 00:00:00.000'and recordtimestamp < '2022-12-12 23:59:59.000' and name = 'Aact' and machineid = 'M5209' ;")
row = cursor.fetchone()
#print(row[2])
list = []
while row:
    print(row)
    row = cursor.fetchone()
    list.append(row)

point = []
value = []
time = []
for i in range(len(list)-1):
        point.append(i)
        time.append(list[i][3])
        try:
            value.append(float(list[i][2]))
        except ValueError:
            value.append('unavailable')



time_2 = []
for i in range(len(time)):
    time_tem = time[i].strftime("%m/%d/%Y, %H:%M:%S")
    time_2.append(time_tem)

joint = np.hstack((time_2,value))
time_new = np.array(time)[:,np.newaxis]
value_new = np.array(value)[:,np.newaxis]
joint = np.concatenate([time_new,value_new],axis=1)
#################################################
data = DataFrame(joint,columns = ["UTC_Time","value"])
data.to_csv('D:\\Ruoyu\CESMII\\Data\\data_by_month_89teeth_zp40\\202212_data\\Aact_20221212.csv')




###########################################
# point = []
# value = []
# time = []
# for i in range(len(list)-1):
#     c = list[i][1]
#     if  c == 'F':
#         point.append(i)
#         time.append(list[i][3])
#         try:
#             value.append(float(list[i][2]))
#         except ValueError:
#             value.append('unavailable')
#             #value.append(float(list[i-1][2]))
#
#
# time_2 = []
# for i in range(len(time)):
#     time_tem = time[i].strftime("%m/%d/%Y, %H:%M:%S")
#     time_2.append(time_tem)
#
# joint = np.hstack((time_2,value))
# time_new = np.array(time)[:,np.newaxis]
# value_new = np.array(value)[:,np.newaxis]
# joint = np.concatenate([time_new,value_new],axis=1)
################################################

