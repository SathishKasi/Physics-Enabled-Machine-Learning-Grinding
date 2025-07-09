from keras.models import *
from keras.layers import *
import keras
from keras.optimizers import *
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from keras import backend as K
import tensorflow as tf
raw_data =  pd.read_csv("D:\\Ruoyu\\CESMII\\Data\\Only_zp40_train.csv", header=None)#usecols=['Stock Removal per Flank','Vw','Radial Infeed','Feed Rate','Cycles','Revs','Qw',	'CUMUL Rotation Time (min)','CUMUL  Machining Time (min)','CUMUL  Dressing Time (min)','ADAM Machining Energy','ADAM Dressing Energy'])
#data = raw_data.values

df = shuffle(raw_data)
df_data = raw_data.values

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

# max_time = np.max(df_data[:,12])
# min_time = np.min(df_data[:,12])
# df_data[:,12] = (df_data[:,12]-min_time)/(max_time-min_time)

# max_energy = np.max(df_data[:,13])
# min_energy = np.min(df_data[:,13])
# df_data[:,13] = (df_data[:,13]-min_energy)/(max_energy-min_energy)


training_data = df_data[:108,:]
val_data = df_data[108:,:]

##############################DNN

physcis_output = df_data[:,6]

train_input_data = training_data[:,1:6]
train_output_data = training_data[:,13:]
train_physcis_output = physcis_output[:108]
train_physcis_output = train_physcis_output.reshape((108,1))


val_input_data = val_data[:,1:6]
val_output_data = val_data[:,13:]
val_physcis_output = physcis_output[108:]
val_physcis_output = val_physcis_output.reshape((4,1))

def create_model():
    #model = Sequential()
    inputs = Input(shape=(5,))
    inputs2 = Input(shape=(1,))
    x1 = Dense(20, activation='relu')(inputs)
    #x2 = Concatenate()([x1, inputs2])
    x3 = Dense(10, activation='relu')(x1)
    #x4 = Dense(4, activation='relu')(x3)
    #x4 = Dense(10, activation='relu')(x3)
    x4 = Concatenate()([x3,inputs2])
    x5 = Dense(2)(x4)
    model = Model([inputs,inputs2], x5)

    model.compile(loss='mean_absolute_error', optimizer=tf.keras.optimizers.Adam(0.001))
    return model
model = create_model()
history = model.fit(x=[train_input_data,train_physcis_output], y= train_output_data, batch_size=10, epochs=50,validation_data=([val_input_data,val_physcis_output ],val_output_data))
#history = model.fit(x=[train_input_data], y= train_output_data, batch_size=50, epochs=2000,validation_data=([val_input_data],val_output_data))
print(model.summary())
epochs=range(len(history.history['loss']))
predictions = (model.predict([val_input_data,val_physcis_output]))
#predictions = (model.predict([test_input_data,test_physcis_output]))
# print(mean_absolute_error(predictions, val_output_data))
# model.save('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\only_zp40.h5')





##############   1D CNN Model

#########inputdata reshape
# train_input_data_reshape = train_input_data.reshape(train_input_data.shape[0],train_input_data.shape[1],1)
# val_input_data_reshape = val_input_data.reshape(val_input_data.shape[0],val_input_data.shape[1],1)
#
# print(train_input_data_reshape.shape)
# print(val_input_data_reshape.shape)
#
# def create_1dcnn_model():
#     #model = Sequential()
#     inputs = Input(shape=(5,1))
#     inputs2 = Input(shape=(1,))
#     x1 = Conv1D(filters=64, kernel_size=3, activation='relu', name="Conv1D_1")(inputs)
#     #x2 = Concatenate()([x1, inputs2])
#     #x3 = Conv1D(filters=32, kernel_size=3, activation='relu', name="Conv1D_1")(x1)
#     x4 = MaxPooling1D(pool_size=2, name="MaxPooling1D")(x1)
#     x5 = Flatten()(x4)
#     x6 = Dense(10, activation='relu')(x5)
#     x7 = Concatenate()([x6,inputs2])
#     x8 = Dense(2)(x7)
#     model = Model(input=[inputs,inputs2], output=x8)
#
#     model.compile(loss='mean_absolute_error', optimizer=Adam(0.001))
#     return model
# model = create_1dcnn_model()
# history = model.fit(x=[train_input_data_reshape,train_physcis_output], y= train_output_data, batch_size=20, epochs=1000,validation_data=([val_input_data_reshape,val_physcis_output ],val_output_data))
# #history = model.fit(x=[train_input_data], y= train_output_data, batch_size=50, epochs=2000,validation_data=([val_input_data],val_output_data))
#
# predictions = (model.predict([val_input_data_reshape,train_physcis_output]))
# #predictions = (model.predict([test_input_data,test_physcis_output]))
# print(mean_absolute_error(predictions, val_output_data))
######################
# print(val_output_data)
# print(predictions)
#
# # predictions[:,0] = predictions[:,0]*(max_time-min_time) + min_time
# # predictions[:,1] = predictions[:,1]*(max_energy-min_energy) + min_energy
# # predictions[:,2] = predictions[:,2]*(max_dress_time-min_dress_time) + min_dress_time
# # predictions[:,3] = predictions[:,3]*(max_machine-min_machine) + min_machine
# # predictions[:,4] = predictions[:,4]*(max_dress-min_dress) + min_dress
# #print(predictions)
# #np.savetxt('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_prediction_new.csv', predictions, delimiter = ',')
# # np.savetxt('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_prediction8_middle.csv', predictions, delimiter = ',')
# model.save('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\6_2_input_checkpoint\\bottom_2_new.h5')
# plt.figure()
# plt.plot(epochs,history.history['loss'],'b',label='Training loss')
# plt.plot(epochs,history.history['val_loss'],'r',label='Validation loss')
# plt.title('Traing and Validation loss')
# plt.legend()
# plt.show()

# loss_train = history.history['loss']
# loss_val = history.history['val_loss']
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\loss_plot\\middle_1_train_loss.csv', loss_train,delimiter = ',')
# np.savetxt('D:\\Ruoyu\\CESMII\\Data\\hybrid_model_results\\loss_plot\\middle_1_val_loss.csv', loss_val, delimiter = ',')


########################### Conventional Machine Learning Algorithms

# train_input_data = training_data[:,1:7]
# train_output_data = training_data[:,13:]
#
# val_input_data = val_data[:,1:7]
# val_output_data = val_data[:,13:]
#############SVR
# from sklearn.svm import SVR
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
#
# regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.1))
# regr.fit(train_input_data, train_output_data)
#
# y_pred = regr.predict(val_input_data)
#
# print(val_output_data)
# print(y_pred)
# print(mean_absolute_error(y_pred, val_output_data))
#############Decision Tree
# from sklearn.tree import DecisionTreeRegressor
#
# regr_1 = DecisionTreeRegressor(max_depth=6)
# regr_1.fit(train_input_data, train_output_data)
#
# y_pred = regr_1.predict(val_input_data)
#
# print(val_output_data)
# print(y_pred)
# print(mean_absolute_error(y_pred, val_output_data))
#################Random Forest
# from sklearn.ensemble import RandomForestRegressor
#
#
# regr_2 = RandomForestRegressor(max_depth=4, random_state=0)
# regr_2.fit(train_input_data, train_output_data)
#
# y_pred = regr_2.predict(val_input_data)
#
# print(val_output_data)
# print(y_pred)
# print(mean_absolute_error(y_pred, val_output_data))

