import numpy as np
import pandas as pd
from keras.models import load_model
from keras.layers import *
from keras.optimizers import *


######### total stock is the sole input
total_stock = 0.02




######### Calculate other input parameters
var_dim = total_stock*5.26


######## The range of the revolution and cycle
revolution = [1,2,3]
cycle = [1,2,3,4]

radial_infeed_list = []
revolution_list =[]
cycle_list = []

for i in range(len(revolution)):
    for j in range(len(cycle)):
        com = revolution[i]*cycle[j]
        LF_stock = var_dim / (10.52 * com)
        radial_infeed = LF_stock * 2.39
        if radial_infeed < 0.005 and cycle[j] >= revolution[i]:
            radial_infeed_list.append(round(radial_infeed,4))
            revolution_list.append(revolution[i])
            cycle_list.append(cycle[j])

feed_rate_list = []
radial_infeed_list_update = []
#q_w_list = []
revolution_list_update = []
cycle_list_update = []
for k in range(130,200,1):
    for n in range(len(radial_infeed_list)):
        if 5< k * radial_infeed_list[n] * 10.72 < 6:
            #q_w_list.append(k * radial_infeed_list[n]*10.72)
            feed_rate_list.append(k)
            radial_infeed_list_update.append(radial_infeed_list[n])
            revolution_list_update.append(revolution_list[n])
            cycle_list_update.append(cycle_list[n])

################Generate physics output
physics_output_list =[]
for m in range(len(radial_infeed_list_update)):
    physics_output = radial_infeed_list_update[m] * feed_rate_list[m]/60
    physics_output_list.append(physics_output)

Total_Stock_list = []
for o in range(len(physics_output_list)):
    Total_Stock_list.append(total_stock)

###################Merge six input parameters together
Model_Input_Data =np.stack((Total_Stock_list,radial_infeed_list_update,feed_rate_list,cycle_list_update,revolution_list_update,physics_output_list), axis=1)
print(Model_Input_Data)

###################Load pretrained hybrid model parameters and make predictions (first value is total energy and second value is total time)
model = load_model('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\6_2_input_checkpoint\\bottom_infusion.h5')
predictions = model.predict([Model_Input_Data[:,:5],Model_Input_Data[:,5:6]])
predictions[:,0] = predictions[:,0]*3600000
min_row = np.where(predictions==np.min(predictions[:,0]))[0]
optimized_input_parameters = Model_Input_Data[min_row,:]
print(predictions)
print("The Total stock is %d" % Model_Input_Data[min_row,1])














