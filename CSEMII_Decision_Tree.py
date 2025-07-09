from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import svm

raw_data =  pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Proposed Database structure for Part 170 Manufacturing CNC Data - Sheet1_old_version.csv", header=None)#usecols=['Stock Removal per Flank','Vw','Radial Infeed','Feed Rate','Cycles','Revs','Qw',	'CUMUL Rotation Time (min)','CUMUL  Machining Time (min)','CUMUL  Dressing Time (min)','ADAM Machining Energy','ADAM Dressing Energy'])
#data = raw_data.values

df = shuffle(raw_data)
df_data = df.values

################Data Normolization
# max_job_level = np.max(data[:,0])
# min_job_level = np.min(data[:,0])
# data[:,0] = (data[:,0]-min_job_level)/(max_job_level-min_job_level)

#max_feed = np.max(df_data[:,3])
# max_feed = 175
# min_feed = np.min(df_data[:,3])
# df_data[:,3] = (df_data[:,3]-min_feed)/(max_feed-min_feed)


# max_rotation = np.max(df_data[:,7])
# min_rotation = np.min(df_data[:,7])
# df_data[:,7] = (df_data[:,7]-min_rotation)/(max_rotation-min_rotation)
#
# max_machine_time = np.max(df_data[:,8])
# min_machine_time = np.min(df_data[:,8])
# df_data[:,8] = (df_data[:,8]-min_machine_time)/(max_machine_time-min_machine_time)
#
# max_dress_time = np.max(df_data[:,9])
# min_dress_time = np.min(df_data[:,9])
# df_data[:,9] = (df_data[:,9]-min_dress_time)/(max_dress_time-min_dress_time)

max_time = np.max(df_data[:,12])
min_time = np.min(df_data[:,12])
df_data[:,12] = (df_data[:,12]-min_time)/(max_time-min_time)

max_energy = np.max(df_data[:,13])
min_energy = np.min(df_data[:,13])
df_data[:,13] = (df_data[:,13]-min_energy)/(max_energy-min_energy)


training_data = df_data[:280,:]
val_data = df_data[280:,:]
#test_data = df_data[290:,:]

physcis_output = df_data[:,6]

train_input_data = training_data[:,1:7]
train_output_data = training_data[:,12:13]
train_physcis_output = physcis_output[:280]
train_physcis_output = train_physcis_output.reshape((280,1))


val_input_data = val_data[:,1:7]
val_output_data = val_data[:,12:13]
val_physcis_output = physcis_output[280:]
val_physcis_output = val_physcis_output.reshape((21,1))

data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\test_6_input.csv", header=None)

test_data = data.values[:,:7]

#clf = tree.DecisionTreeRegressor()
clf = svm.SVR()
clf = clf.fit(train_input_data, train_output_data)
c = clf.predict(test_data)

print(c*(max_time-min_time) + min_time)

#print(val_output_data)