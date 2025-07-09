import pandas as pd
import numpy as np
from dateutil.parser import parse
import time
import matplotlib.pyplot as plt
#from scipy import integrate
import datetime
# import math
from pandas import DataFrame

####################Data Pre-processing(interpolation)

######raw data
# data = pd.read_csv("D:\\Ruoyu\CESMII\\Data\\data_by_month_89teeth_zp40\\202212_data\\watts_20221222.csv",usecols=[1,2])
# print(data)
# data_list = data.values.tolist()
#
# ##############################
# # point = []
# # value = []
# # time = []
# # for i in range(len(data)-1):
# #     c = data_list[i][0]
# #     if  c == 'Aact':
# #         point.append(i)
# #         time.append(data_list[i][2])
# #         try:
# #             value.append(float(data_list[i][1]))
# #         except ValueError:
# #             value.append('unavailable')
# #
# #
# #
# # # time_2 = []
# # # for i in range(len(time)):
# # #     time_tem = time[i].strftime("%m/%d/%Y, %H:%M:%S")
# # #     time_2.append(time_tem)
# #
# # joint = np.hstack((time,value))
# # time_new = np.array(time)[:,np.newaxis]
# # value_new = np.array(value)[:,np.newaxis]
# # joint = np.concatenate([time_new,value_new],axis=1)
# #
# # result = DataFrame(joint,columns = ["UTC_Time","value"])
# # result.to_csv('D:\\Ruoyu\\CESMII\\Data\\202204_data\\query_data\\202204_Aact.csv')
# # #
# # #
# # #
# # #
# # # ################################
# # #
# # value = data['value']
# # # for i in range(len(value)):
# # #     if value.T.values[i] =='unavailable':
# # #         print(i)
# # #         value.T.values[i] = value.T.values[i-1]
# # #         print(value.T.values[i] )
# # #     else: i = i+1
# #
# #
# data['UTC_Time'] = pd.to_datetime(data['UTC_Time'])
# data.set_index('UTC_Time',inplace=True)
# data.index
# print(data.index)
# index = pd.date_range('2022-12-12 0:02:01', '2022-12-12 23:59:56', freq='S')
# data = data[~data.index.duplicated()]
# data = data.reindex(index)
#
# #####Fill NA/NaN values using the propagate last valid observation forward to next valid backfill
# data.fillna(method = 'ffill',inplace = True)
# print(data)
#
# data.to_csv('D:\\Ruoyu\CESMII\\Data\\data_by_month_89teeth_zp40\\202212_data\\watts_20221222_preprocessing.csv')

#



######################Job Level identification job level 1
# #Load feed rate and aact dataset
fd = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\F_20211130_update.csv",usecols=[0,1])#,usecols=[1,2])
nr = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\Aact_20211130_preprocessing.csv",usecols=[0,1])#,usecols=[1,2])

# obtain the parameter value and coressponding time
feed_rate = fd['value']
time_1 = fd['UTC_Time']
#time_1 = fd["Unnamed: 0"]


# for i in range(len(feed_rate)):
#     if feed_rate.T.values[i] =='NaN':
#         #print(i)
#         feed_rate.T.values[i].replace(np.nan, 0)
#         #print(feed_rate.T.values[i] )
#     else: i = i+1

no_rev = nr['value']
#time_2 = nr['UTC_Time']
time_2 = nr["Unnamed: 0"]

# for i in range(len(no_rev)):
#     if no_rev.T.values[i] =='NaN':
#         #print(i)
#         no_rev.T.values[i].replace(np.nan, 0)
#         #print(no_rev.T.values[i] )
#     else: i = i+1







########################First round job level 1 identification
start = []
end = []
inverse_list = feed_rate.T.values[:]#.tolist()
inverse_list_1 = [float(inverse_list) for inverse_list in inverse_list]
inverse_list_2 = inverse_list_1[::-1]
inverse = inverse_list_2.index(120)

for i in range(len(time_1)-inverse):
    print(i)
    if float(feed_rate.T.values[i]) == 115:# the feed rate of job level 1 is 115
        new_list = feed_rate.T.values[i:len(time_1)].tolist()
        new_list_1  = [float(new_list) for new_list in new_list]
        end_point = new_list_1.index(120)
        t = (parse(time_1.T.values[end_point+i]) - parse(time_1.T.values[i])).total_seconds()
        if  10000 > t > 4500:
            start.append(i)
            end.append(end_point+i)
        else: continue
    else: i = i + 1
# print(start)
# print(end)
start_point = []
end_point = []
for i in range(len(start)):
    time_start_point = time_1[start[i]]
    time_end_point = time_1[end[i]]
    start_point.append(time_start_point)
    end_point.append(time_end_point)
print(start_point)
print(end_point)
# #######################################################
np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20221130_start_1_time.csv', start_point, delimiter = ',',fmt="%s")
np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20221130_end_1_time.csv', end_point, delimiter = ',',fmt="%s")
# #
np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20211130_start_1.csv', start, delimiter = ',')
np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20211130_end_1.csv', end, delimiter = ',')
# # # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # #cross validation with the number of revolution
start = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20211130_start_1.csv")
end = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20211130_end_1.csv")
# # #
aact_list = time_2.T.values.tolist()
f_list = time_1.T.values.tolist()
start_1= []
end_1 = []
#
#
#
for i in range(len(start)):
    #print(i)
    time_start_point = aact_list.index(f_list[int(start.T.values[:,i])])
    time_end_point = aact_list.index(f_list[int(end.T.values[:,i])])
    no_start_value = no_rev.T.values[time_start_point]
    no_end_value = no_rev.T.values[time_end_point]
    jump = 0
    for j in range(time_start_point,time_end_point):
        no_j_value = no_rev.T.values[j]
        if  abs(no_j_value - no_rev.T.values[j+1]) > 340:  # count the sudden jump which can be used to identify the number of revolution
            jump = jump+1
        else:
            j = j+1

    if jump == 2:

        start_1.append(start.T.values[:,i])
        end_1.append(end.T.values[:,i])
    else: continue

start_point_1 = []
end_point_1 = []
for i in range(len(start_1)):
    time_start_point = time_1[start_1[i]]
    time_end_point = time_1[end_1[i]]
    start_point_1.append(time_start_point)
    end_point_1.append(time_end_point)
print(start_point_1)
print(end_point_1)
print(start_1)
print(end_1)
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20220320_start_1_new.csv', start_2, delimiter = ',')
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20220320_end_1_new.csv', end_2, delimiter = ',')
# # # # # # # #
# # # # # # # # ################Job Level 2
# # # # # # # #
# # # # # # #
# start_2 = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20220320_end_1_new.csv")
# #
# end = []
# a = start_2.T.values[:]
# b = a.tolist()
# c = b[0]
#
# ##############
# # new_list = feed_rate.T.values[2095:len(time_1)].tolist()
# # #end_point = new_list.index(115.0)+2095
# # end_point = new_list.index(120.0)+2095
# # d = c[1]
# ####################
# new_list = feed_rate.T.values[len(time_1)-1].tolist()
# #end_point = new_list.index(115.0)+2095
# #end_point = new_list.index(120.0)
#
#
#
# ###############
# for i in range(len(start_2)):
#     print(i)
#     new_list = feed_rate.T.values[int(c[i]):len(time_1)].tolist()
#     #new_list_1  = [int(new_list) for new_list in new_list]
#     end_point = new_list.index(120.0)
#     t = (parse(time_1.T.values[end_point+int(c[i])]) - parse(time_1.T.values[int(c[i])])).total_seconds()
#     if  8000 > t > 1000:
#
#         end.append(end_point+c[i])
#     else: continue
#
# print(end)
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20211114_end_2nd.csv', end, delimiter = ',')
# # # #
# # # #
# # # # ###############Job Level 3
# # # #
# start_3 = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20220109_end_2nd.csv")
#
# end = []
# a = start_3.T.values[:]
# b = a.tolist()
# c = b[0]
#
# for i in range(len(start_3)):
#     print(i)
#     new_list = feed_rate.T.values[int(c[i]):len(time_1)].tolist()
#     #new_list_1  = [int(new_list) for new_list in new_list]
#     end_point = new_list.index(130.0)
#     t = (parse(time_1.T.values[end_point+int(c[i])]) - parse(time_1.T.values[int(c[i])])).total_seconds()
#     if  3420 > t > 3300:
#
#         end.append(end_point+c[i])
#     else: continue
#
# print(end)
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\result\\20220109_end_3rd.csv', end, delimiter = ',')
#
# #
# #
# #
# #
# # ################Job Level 4
# start_4 = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\20211130_end_3rd.csv")
# end_4 = []
# a = start_4.values[:]
# b = a.tolist()
# c = b[0]
#
# uact = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_month_89teeth_zp40\\202111_data\\Uact_20211130_preprocessing.csv")
# uact_value = uact["Unnamed: 0"]
# uact_list = uact_value.values[:].tolist()
#
# for i in range(len(start_4)):
#     print(i)
#     aa = f_list[int(start_4.values[i])]
#     time_start_point_4 = uact_list.index(f_list[int(start_4.values[i])])
#     time_end_point_4 = time_start_point_4 + 1680
#     no_start_value = no_rev.values[time_start_point_4]
#     no_end_value = no_rev.values[time_end_point_4]
#     if abs(no_end_value-no_start_value) < 5 :
#        end_4.append(time_end_point_4)
#
# end_point_4 = []
# for i in range(len(end_4)):
#     time_end_point = time_1[end_4[i]]
#     end_point_4.append(time_end_point)
#
# print(end_point_4)
# for i in range(len(start_4)):
#     print(i)
#     new_list = feed_rate.T.values[int(c[i]):len(time_1)].tolist()
# # The feed rate value is 130
#     end_point = new_list.index(130.0)
#     t = (parse(time_1.T.values[end_point+int(c[i])]) - parse(time_1.T.values[int(c[i])])).total_seconds()
# # The total time range for job level 4
#     if  2000 > t > 1200:
#
#         end.append(end_point+c[i])
#     else: continue


#np.savetxt('D:\\Ruoyu\\CESMII\\Data\\202111_data\\20211130_end_4.csv', end, delimiter = ',')
#
#
#
#
#
#
# #################################Spindle Energy Calculation
#
from scipy import integrate
# cc = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\202201_data\\Ccurrent_56cycle_preprocessing.csv",usecols=[0,1])#,usecols=[1,2])
#
# c_current = cc['value'].values.tolist()
# c_current_time = cc['Unnamed: 0'].values.tolist()
#
# start = '1/21/2022 18:07:00'
# end = '1/21/2022 18:33:00'
#
# job_level_start_point = c_current_time.index(start)
# job_level_end_point = c_current_time.index(end)
#
#
# time_1 = datetime.datetime.strptime(start, '%m/%d/%Y %H:%M:%S')
# time_2 = datetime.datetime.strptime(end, '%m/%d/%Y %H:%M:%S')
# period = (time_2 - time_1).seconds
#
# parameter_value = c_current[job_level_start_point:job_level_end_point]
#
# parameter_value_1  = [float(parameter_value) for parameter_value in parameter_value]
#
# parameter_value_2 = np.array(parameter_value_1)
#
#
#
# time_point = np.linspace(job_level_start_point,job_level_end_point,num=job_level_end_point-job_level_start_point)
#
# sp = integrate.trapz(parameter_value_2,time_point)
#
# ##########
# sp_energy = sp*400*period/3600
# print(sp_energy)




################################ Adam machining and dressing time energy calculation

###########################U_actual count (dress time account)

# ua = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\Uact_20220922_preprocessing.csv",usecols=[0,1])
# u_act = ua['value'].values.tolist()
# u_act_time = ua['Unnamed: 0'].values.tolist()
# #Initialize total time(seconds)
# seconds = 0
# #Initialize time period within each job level
# dress_time =[]
# u_act_point = []

# full_job_level_start_point = '10/31/2022 15:11:00'
# full_job_level_end_point = '10/31/2022 15:37:00'

# job_level_start_point = u_act_time.index(full_job_level_start_point)
# job_level_end_point = u_act_time.index(full_job_level_end_point)
# # The range is the time (seconds) within each detected job level
# for i in range(job_level_start_point,job_level_end_point):
#     if int(float(u_act[i])) < 306:    #when u-act value is smaller than 349 (89 teeth): 306 (109 teeth), we can regard the dressing process start
#         seconds= seconds+1
#         dress_time.append(u_act_time[i])
# print(seconds/60)
# print(dress_time)
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\dress_time.csv', dress_time)#, delimiter = ',')
# #
# #
# # #######################UPCE dressing and machining
# data = pd.read_csv("D:\\Ruoyu\CESMII\\Data\\data_by_month_89teeth_zp40\\202210_data\\watts_20221031_preprocessing.csv")
#
# adam_watt = data['value']
# adam_watt_value = adam_watt.values.tolist()
# time_adam_watt = data['Unnamed: 0']
# time_adam_watt_list = time_adam_watt.values.tolist()
# adam_dress_point = []
#
# # for j in range(len(dress_time)):
# #     tem = time_adam_watt_list.index(dress_time[j])
# #     adam_dress_point.append(tem)
# # #####line 339 time point in uact excel
# job_level_start_point = time_adam_watt_list.index(full_job_level_start_point)
# job_level_end_point = time_adam_watt_list.index(full_job_level_end_point)
# adam_total_point = list(range(job_level_start_point,job_level_end_point))
# adam_machining_point = [k for k in adam_total_point if k not in adam_dress_point]
#
# #########################dressing energy
# # dressing_end_point = []
# # for i in range(1,len(adam_dress_point)):
# #     if adam_dress_point[i] - adam_dress_point[i-1] != 1:
# #         dressing_end_point.append(adam_dress_point[i-1])
# #
# # if dressing_end_point == [] :
# #     dressing_end_point.append(adam_dress_point[-1])
# # dress_single_energy = []
#
# #########################test
# # tt = adam_dress_point.index(end_point[0])+1
# # tt1 = adam_dress_point[-1]+1
# # dress_energy_point = adam_watt[adam_dress_point[adam_dress_point.index(end_point[0])+1]:adam_dress_point[-1]+1]
#
# ###########################
#
#
#
# # for k in range(0,len(dressing_end_point)):
# #     if k == 0:
# #         dress_energy_point = adam_watt[adam_dress_point[0]:dressing_end_point[k]+1]
# #         dress_len = dressing_end_point[k] - adam_dress_point[0]
# #         dress_time_point = np.linspace(adam_dress_point[0], dressing_end_point[k], num=dress_len+1)
# #         dress_energy = integrate.trapz(dress_energy_point, dress_time_point)
# #         dress_single_energy.append(dress_energy)
# #     elif 0 < k < len(dressing_end_point):
# #         dress_energy_point = adam_watt[adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1]:dressing_end_point[k]+1]
# #         dress_len =  dressing_end_point[k] - adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1]
# #         dress_time_point = np.linspace(adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1],dressing_end_point[k], num=dress_len+1)
# #         dress_energy = integrate.trapz(dress_energy_point, dress_time_point)
# #         dress_single_energy.append(dress_energy)
# #     elif k == len(dressing_end_point):
# #         dress_energy_point = adam_watt[adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1]:adam_dress_point[-1]+1]
# #         dress_len = adam_dress_point[-1] - adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1]
# #         dress_time_point = np.linspace(adam_dress_point[adam_dress_point.index(dressing_end_point[k-1])+1],adam_dress_point[-1], num=dress_len+1)
# #         dress_energy = integrate.trapz(dress_energy_point, dress_time_point)
# #         dress_single_energy.append(dress_energy)
# # #
# # total_dressing_energy = sum(dress_single_energy)
# total_energy_point = adam_watt[job_level_start_point:job_level_end_point]
# job_level_len = job_level_end_point - job_level_start_point
# time_point = np.linspace(job_level_start_point,job_level_end_point,num=job_level_len)
# total_adam_energy = integrate.trapz(total_energy_point,time_point)
# #total_machining_energy = total_adam_energy - total_dressing_energy
# #
# # #print(total_energy_point)
# # #print(len)
# #
# #
# print(int(total_adam_energy ))
# print(int(total_machining_energy))
# print(int(total_dressing_energy))
####print(total_adam_energy)
# ################################ UPCE machining and dressing time energy calculation
#
# ##Just change the watts_pre-processing.csv file into wattsUPCE_pre-processing.csv file.
#
#
#
#
# ####################A_actual teeth_rotate_step count

# a = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\data_by_week_zpi25\\Aact_20220922_preprocessing.csv",usecols=[0,1])
# a_act = a['value']
# time_a_act = a['Unnamed: 0']
# a_act_list = a_act.T.values.tolist()
# time_a_act_list = time_a_act.T.values.tolist()
# aact_job_level_start_point = time_a_act_list.index(full_job_level_start_point)
# aact_job_level_end_point = time_a_act_list.index(full_job_level_end_point)
# job_level_time = time_a_act_list[aact_job_level_start_point:aact_job_level_end_point+1 ]
# a_value = a_act_list[aact_job_level_start_point:aact_job_level_end_point+1 ]
#
# point_r = 0
# r_time =[]
# for l in range(1,len(a_value)-1):
#     if a_value[l-1] - a_value [l+1] != 0  and abs(a_value[l] - a_value [l+1]) < 100:
#         r_time.append(l)
#
#
# for m in range(1,len(r_time)):
#     if r_time[m] - r_time[m-1] == 1:
#         point_r = point_r + 1
#
#
#
# print(point_r/60)
# print(r_time)
#
#
# ###################Teeth Gap Time
#
# gap_time=[]
# total_gap_time = []
# total_gap_time.append(job_level_time[0:r_time[0]+1])
# total_gap_time.append(job_level_time[r_time[-1]:])
# for k in range(0,len(r_time)-1):
#     if r_time[k+1] - r_time[k] != 1:
#         gap_time = job_level_time[r_time[k]:r_time[k+1]]
#         total_gap_time.append(gap_time)
#     else:
#         k = k+1
#
#
# teeth_rotate_num = len(total_gap_time) -1
# average_time = point_r/teeth_rotate_num
# print(teeth_rotate_num)
# print(average_time)


############################Get time for teeth gap then calculate energy
# data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\202112_data\\Uact_20211202_preprocessing.csv")#,usecols=[1,2])
# data['value'] = data.value.astype(float)
# uact_value = data['value']
# uact_time = data['Unnamed: 0'].T.values.tolist()
# data.info()
# energy_start_time = total_gap_time[0][0]
# energy_end_time = total_gap_time[0][-1]
# energy_start_point = uact_time.index(energy_start_time)
# energy_end_point = uact_time.index(energy_end_time)
# uact_value_scope = uact_value[energy_start_point:energy_end_point+1]
# len = len(total_gap_time[0])
# time_scope = np.linspace(energy_start_point, energy_end_point, num=len)
# p = integrate.trapz(uact_value_scope,time_scope)




# total_energy = []
# for i in range(len(total_gap_time)):
#         energy_start_time = total_gap_time[i][0]
#         energy_end_time = total_gap_time[i][-1]
#         energy_start_point = uact_time.index(energy_start_time)
#         energy_end_point = uact_time.index(energy_end_time)
#         parameter_value = uact_value[energy_start_point:energy_end_point+1]
#         length = len(total_gap_time[i])
#         time_point = np.linspace(energy_start_point,energy_end_point,num=length)
#
#         p = integrate.trapz(parameter_value,time_point)
#         total_energy.append(p)
#
# total_energy_sum = sum(total_energy)
# print(total_energy_sum)

# #####################Starting tooth changes between job levels
#
# data = pd.read_csv("D:\\Ruoyu\\CESMII\\January 2022 Data\\Aact_pre-processing.csv")
#
# aact = data['Value']
# aact_value = aact.T.values.tolist()
# time_a_act = data['Unnamed: 0']
# time_a_act_list = time_a_act.T.values.tolist()
# next_job_level_start = []
# for i in range(280368,280420):
#     if  abs(aact_value[i] -aact_value[i+10]) < 1:
#         next_job_level_start.append(i)
#         break
#     else:
#         i = i+1
# print(next_job_level_start)
# change_start_point = time_a_act_list[280368]
# change_end_point = time_a_act_list[i]
# change_start_time = datetime.datetime.strptime(change_start_point, '%m/%d/%Y %H:%M:%S')
# change_end_time = datetime.datetime.strptime(change_end_point, '%m/%d/%Y %H:%M:%S')
# change_time = (change_end_time - change_start_time).seconds
# print(change_start_time)
# print(change_end_time)
# print(change_time)





#############  Ignore The following parts        ########################



#############################Plot figure (need to be updated)

# data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Nov_1_to Nov 11 data_Pre-processing\\F_pre-processing.csv",usecols=[1])#,usecols=[1,2])
#
# data.info()
# #data = pd.DataFrame.to_numpy(data)
# index = pd.date_range('2021-11-01 18:19:27', '2021-11-10 08:24:03', freq='S')
# print(data.Value)
#
# print(data.Value[6350])
#
#
# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         pass
#
#     try:
#         import unicodedata
#         unicodedata.numeric(s)
#         return True
#     except (TypeError, ValueError):
#         pass
#
#     return False
# #
# #
# for i in range (len(data)):
#     #if  data.Value[i].isdigit() == True :
#     if is_number(data.Value[i]) == True :
#             data.Value[i] == data.Value[i]
#     else : data.Value[i] = 0
# data.info()
#data = pd.DataFrame(data)


# plt.plot(data.Value[0:10])
# plt.title('Feed Rate')
# plt.show()


###############################################Integration Calculation
########load different parameter(ccurrent, uactual, watts and more)
# data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Nov_1_to Nov 11 data_Pre-processing\\Ccurrent_pre-processing.csv",usecols=[0,1])#,usecols=[1,2])
#
# data.info()
# print(data)
# y = data['Value']
#
# parameter_value = y[729139:732799]
#
# time_point = np.linspace(729139,732798,num=3660)
# ########calculate integration value
# p = integrate.trapz(parameter_value,time_point)
#
# ##########
# p1 = p*400*1.01
# print(p1)
# q = 15240
# e = p/q
# print(e)
#
# plt.plot(job_level)
# plt.xlabel('Time')
# # locs, labels=plt.xticks()
# # x_ticks = []
# # new_xticks= t
# # plt.xticks(locs,new_xticks)
# plt.ylabel('Watts')
# plt.show()


###############################Uact calculation
# data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Nov_1_to Nov 11 data_Pre-processing\\Uact_pre-processing.csv")#,usecols=[1,2])
# uact = []
# print (len(data))
# a = data['Value']
#
# for i in range(0,len(a)):
#     if int(float(a[i])) < 349:
#         uact.append(a[i])
#
# print(uact)
# t1 = parse(time_1.T.values[74596])
# t2 = parse(time_1.T.values[76898])
# t3 = (t2-t1).total_seconds()

#######################################################
# Dresser energy dressing intervals integretion over Uact
# cut_point = []
# for i in range(len(dress_time)-1):
#     time_1 = datetime.datetime.strptime(dress_time[i], '%m/%d/%Y %H:%M:%S')
#     time_2 = datetime.datetime.strptime(dress_time[i+1], '%m/%d/%Y %H:%M:%S')
#     if (time_2 - time_1).seconds != 1:
#         cut_point.append(i)
#     else:
#         i = i +1
#
# print(cut_point)
# for j in range(len(cut_point)):
#     dresser_start_point = cut_point[]
#     dresser_end_point =  cut_point[j]
#     time_point = np.linspace(729139,732798,num=3660)
#     p = integrate.trapz(parameter_value,time_point)
