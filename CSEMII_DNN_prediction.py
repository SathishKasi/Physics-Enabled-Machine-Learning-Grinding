from keras.models import load_model
from keras.layers import *
from keras.optimizers import *
import pandas as pd
import numpy as np

data = pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\test_6_input.csv", header=None)

test_data = data.values

raw_data =  pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Only_zp40_train.csv", header=None)#usecols=['Stock Removal per Flank','Vw','Radial Infeed','Feed Rate','Cycles','Revs','Qw',	'CUMUL Rotation Time (min)','CUMUL  Machining Time (min)','CUMUL  Dressing Time (min)','ADAM Machining Energy','ADAM Dressing Energy'])
df_data = raw_data.values


max_time = np.max(df_data[:,12])
min_time = np.min(df_data[:,12])


max_energy = np.max(df_data[:,13])
min_energy = np.min(df_data[:,13])


# max_feed = np.max(test_data[:,2])
# min_feed = np.min(test_data[:,2])
#test_data[:,2] = (test_data[:,2]-min_feed)/(max_feed-min_feed)

original_input = test_data[:,:5]

physics_output = test_data[:,5]
physics_output = physics_output.reshape((22,1))


model = load_model('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\only_zp40.h5')#,custom_objects={'TCN': TCN})
predictions = model.predict([original_input,physics_output])

predictions[:,0] = predictions[:,0]*3600000
#predictions[:,0] = predictions[:,0]*(max_time-min_time) + min_time
#predictions[:,0] = predictions[:,0]*(max_energy-min_energy) + min_energy
# predictions[:,2] = predictions[:,2]*(max_dress_time-min_dress_time) + min_dress_time
# predictions[:,3] = predictions[:,3]*(max_machine-min_machine) + min_machine
# predictions[:,4] = predictions[:,4]*(max_dress-min_dress) + min_dress

print(predictions)

np.savetxt('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\6_2_test_output\\only_zp40.csv', predictions, delimiter = ',')