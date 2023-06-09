# -*- coding: utf-8 -*-
"""ALDA2022_P22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CE14KUt8eWmVg_EOjV1maV2LxQg_R4Ex

# Stock Price Forecasting in an Inflationary market using Artificial Neural Networks

P22: Kartik Rawool, Aadil Tajani, Kaustubh Deshpande
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import cufflinks as cf
cf.go_offline()
plt.style.use('seaborn')
sns.set(rc={'figure.figsize':(13.7,10.27)})

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
uploaded = files.upload()

"""Let's take a look at the dataset"""

df = pd.read_csv('GOOG.csv')
# df = df.set_index('Date')
df.head()

"""Dataset Columns Info"""

df.info()

"""Getting the max and min close values from each year"""

agg = pd.DataFrame()
agg['Date'] = pd.to_datetime(df['Date'])
agg['Close'] = df.Close
agg.groupby(agg.Date.dt.year).agg({'Close': ['min', 'max']})

"""**Now lets take a look at the return of Google's share.**
A return is the change in price of an asset, investment, or project over time, which may be represented in terms of price change or percentage change.
A positive return represents a profit while a negative return marks a loss.
"""

df['Return'] = df.Close.pct_change()
df.head()

"""Statistics of the dataset"""

df.describe()

sns.lineplot(data=df, x='Date', y='Close')
# plt.axes().xaxis.set_minor_locator(df.Date.DayLocator())
# sns.regplot(data=df, x='Date', y='Close', order=3)

df = pd.read_csv('AAPL.csv')

agg = pd.DataFrame()
agg['Date'] = pd.to_datetime(df['Date'])
agg['Close'] = df.Close
agg.groupby(agg.Date.dt.year).agg({'Close': ['min', 'max']})
df['Return'] = df.Close.pct_change()
df.head()
df.describe()
plt.figure()
plt.title("Apple close prices")
sns.lineplot(data=df, x='Date', y='Close')


df = pd.read_csv('AMZN.csv')

agg = pd.DataFrame()
agg['Date'] = pd.to_datetime(df['Date'])
agg['Close'] = df.Close
agg.groupby(agg.Date.dt.year).agg({'Close': ['min', 'max']})
df['Return'] = df.Close.pct_change()
df.head()
df.describe()
plt.figure()
plt.title("AMZN close prices")
sns.lineplot(data=df, x='Date', y='Close')


df = pd.read_csv('SPY.csv')

agg = pd.DataFrame()
agg['Date'] = pd.to_datetime(df['Date'])
agg['Close'] = df.Close
agg.groupby(agg.Date.dt.year).agg({'Close': ['min', 'max']})
df['Return'] = df.Close.pct_change()
df.head()
df.describe()
plt.figure()
plt.title("SPY close prices")
sns.lineplot(data=df, x='Date', y='Close')


df = pd.read_csv('GOOG_RSI.csv')
# df = df.set_index('Date')
df.head()

df.info()

plt.figure()
plt.title("GOOG RSI")
sns.lineplot(data=df, x='Date', y='RSI')

pip install yfinance

import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.metrics import mean_squared_error

stock_data_goog = yf.download('GOOG', start='2004-08-19', end='2022-10-18')
stock_data_goog.head()

plt.figure(figsize=(15, 8))
plt.title('Stock Prices History')
plt.plot(stock_data_goog['Close'], color='r')
plt.xlabel('Date')
plt.ylabel('Prices ($)')

#Scaling the closing prices
close_prices = stock_data_goog['Open']
values = close_prices.values

scaler = MinMaxScaler(feature_range=(-1,1))
scaled_data = scaler.fit_transform(values.reshape(-1,1))
scaled_data

training_data_len = math.ceil(len(values)* 0.95)

def load_data(stock, look_back):
    data_raw = scaled_data # convert to numpy array
    data = []
    
    # create all possible sequences of length look_back
    for index in range(len(data_raw) - look_back): 
        data.append(data_raw[index: index + look_back])
    
    data = np.array(data);
    test_set_size = int(np.round(0.2*data.shape[0]));
    train_set_size = data.shape[0] - (test_set_size);
    
    x_train = data[:train_set_size,:-1,:]
    y_train = data[:train_set_size,-1,:]
    
    x_test = data[train_set_size:,:-1]
    y_test = data[train_set_size:,-1,:]
    
    return [x_train, y_train, x_test, y_test]

look_back = 30
x_train, y_train, x_test, y_test = load_data(scaled_data, look_back)
print('x_train.shape = ',x_train.shape)
print('y_train.shape = ',y_train.shape)
print('x_test.shape = ',x_test.shape)
print('y_test.shape = ',y_test.shape)

# make training and test sets in torch
x_train = torch.from_numpy(x_train).type(torch.Tensor)
x_test = torch.from_numpy(x_test).type(torch.Tensor)
y_train = torch.from_numpy(y_train).type(torch.Tensor)
y_test = torch.from_numpy(y_test).type(torch.Tensor)

y_train.size(),x_train.size()

# Build model
input_dim = 1
hidden_dim = 32
num_layers = 2
output_dim = 1


# Here we define our model as a class
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTM, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.num_layers = num_layers

        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 32, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states! 
        out = self.fc(out[:, -1, :]) 
        # out.size() --> 100, 10
        return out
    
model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

loss_fn = torch.nn.MSELoss()

optimiser = torch.optim.Adam(model.parameters(), lr=0.01)
print(model)
print(len(list(model.parameters())))
for i in range(len(list(model.parameters()))):
    print(list(model.parameters())[i].size())

# Train model
num_epochs = 60
hist = np.zeros(num_epochs)

# Number of steps to unroll
seq_dim =look_back-1  

for t in range(num_epochs):
    # Initialise hidden state
    # Don't do this if you want your LSTM to be stateful
    #model.hidden = model.init_hidden()
    
    # Forward pass
    y_train_pred = model(x_train)

    loss = loss_fn(y_train_pred, y_train)
    if t % 10 == 0 and t !=0:
        print("Epoch ", t, "MSE: ", loss.item())
    hist[t] = loss.item()

    # Zero out gradient, else they will accumulate between epochs
    optimiser.zero_grad()

    # Backward pass
    loss.backward()

    # Update parameters
    optimiser.step()

plt.plot(hist, label="Training loss")
plt.legend()
plt.show()

np.shape(y_train_pred)

# make predictions
y_test_pred = model(x_test)

# invert predictions
y_train_pred_inv = scaler.inverse_transform(y_train_pred.detach().numpy())
y_train_inv = scaler.inverse_transform(y_train.detach().numpy())
y_test_pred_inv = scaler.inverse_transform(y_test_pred.detach().numpy())
y_test_inv = scaler.inverse_transform(y_test.detach().numpy())

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(y_train_inv[:,0], y_train_pred_inv[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(y_test_inv[:,0], y_test_pred_inv[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

y_test_pred

"""### LSTM testing data vs predicted"""

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[len(stock_data_goog)-len(y_test):].index, y_test_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[len(stock_data_goog)-len(y_test):].index, y_test_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

"""### LSTM training data vs predicted"""

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

"""### LSTM with RSI and inflation rate"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:01:35 2022

@author: kades
"""


import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.metrics import mean_squared_error
import datetime

random_seed = 1
torch.manual_seed(random_seed)

import random
random.seed(random_seed)

import numpy as np
np.random.seed(random_seed)

inflation_pd= pd.read_csv ('inflation_report.csv')


dates_pd=pd.read_csv('dates.csv')
dates_pd["inflation"]=None

for i in range(len(dates_pd)):
    date=(dates_pd.iloc[[i], dates_pd.columns.get_loc('Date')].values)[0] +" 00:00:00"
    date = datetime.datetime.strptime(date, "%m/%d/%Y  %H:%M:%S")
    dates_pd.at[i, 'inflation']=inflation_pd.at[-inflation_pd.at[0,'Year']+date.year, str(date.month)]


stock_data_goog = yf.download('GOOG', start='2005-01-24', end='2022-10-18')
stock_data_goog.head()


stock_data_aapl = yf.download('AAPL', start='2005-01-24', end='2022-10-18')
stock_data_aapl.head()


stock_data_amzn = yf.download('AMZN', start='2005-01-24', end='2022-10-18')
stock_data_amzn.head()



stock_data_spy = yf.download('SPY', start='2005-01-24', end='2022-10-18')
stock_data_spy.head()



df_goog_rsi = pd.read_csv ('GOOG_RSI.csv')


goog_close=stock_data_goog['Close'].values
scaler_goog = MinMaxScaler(feature_range=(-1,1))
scaled_goog_data = scaler_goog.fit_transform(goog_close.reshape(-1,1))

aapl_close=stock_data_aapl['Close'].values
scaler_aapl = MinMaxScaler(feature_range=(-1,1))
scaled_aapl_data = scaler_aapl.fit_transform(aapl_close.reshape(-1,1))

amzn_close=stock_data_amzn['Close'].values
scaler_amzn = MinMaxScaler(feature_range=(-1,1))
scaled_amzn_data = scaler_amzn.fit_transform(amzn_close.reshape(-1,1))

spy_close=stock_data_spy['Close'].values
scaler_spy = MinMaxScaler(feature_range=(-1,1))
scaled_spy_data = scaler_spy.fit_transform(spy_close.reshape(-1,1))

goog_rsi=df_goog_rsi['RSI'].values
scaler_goog_rsi = MinMaxScaler(feature_range=(-1,1))
scaled_goog_rsi_data = scaler_spy.fit_transform(goog_rsi.reshape(-1,1))

inflation_rate=dates_pd['inflation'].values
scaler_inflation = MinMaxScaler(feature_range=(-1,1))
scaled_inflation_data = scaler_spy.fit_transform(inflation_rate.reshape(-1,1))





def exp_1_setup_data(data1, data2, inflation):
    data_out=[]
    for index in range(1, len(data1)):
        data_out.append([data2[index], data1[index-1], inflation[index], data1[index]])
    data_out = np.array(data_out);
    test_set_size = int(np.round(0.2*data_out.shape[0]));
    train_set_size = data_out.shape[0] - (test_set_size);
    
    x_train = data_out[:train_set_size,:-1] #previous day's goog value and RSI and Inflation rate
    y_train = data_out[:train_set_size,-1] #next day's goog value
    
    x_test = data_out[train_set_size:,:-1]  #previous day's goog value and RSI and Inflation rate
    y_test = data_out[train_set_size:,-1] #next day's goog value
    
    return [x_train, y_train, x_test, y_test]


def exp_2_setup_data(data1, data2, data3, output):
    data_out=[]
    for index in range(1, len(data1)):
        data_out.append([data1[index-1], data2[index-1], data3[index-1], output[index]])
    data_out = np.array(data_out);
    test_set_size = int(np.round(0.2*data_out.shape[0]));
    train_set_size = data_out.shape[0] - (test_set_size);
    
    x_train = data_out[:train_set_size,:-1]
    y_train = data_out[:train_set_size,-1]
    
    x_test = data_out[train_set_size:,:-1]
    y_test = data_out[train_set_size:,-1]
    
    return [x_train, y_train, x_test, y_test]

x_goog_train, y_goog_train, x_goog_test, y_goog_test=exp_1_setup_data(scaled_goog_data, scaled_goog_rsi_data, scaled_inflation_data)


x_corr_train, y_corr_train, x_corr_test, y_corr_test=exp_2_setup_data(scaled_aapl_data, scaled_amzn_data, scaled_spy_data, scaled_goog_data)


x_goog_train = torch.from_numpy(x_goog_train).type(torch.Tensor)
x_goog_test = torch.from_numpy(x_goog_test).type(torch.Tensor)
y_goog_train = torch.from_numpy(y_goog_train).type(torch.Tensor)
y_goog_test = torch.from_numpy(y_goog_test).type(torch.Tensor)

x_corr_train = torch.from_numpy(x_corr_train).type(torch.Tensor)
x_corr_test = torch.from_numpy(x_corr_test).type(torch.Tensor)
y_corr_train = torch.from_numpy(y_corr_train).type(torch.Tensor)
y_corr_test = torch.from_numpy(y_corr_test).type(torch.Tensor)


# Build model
input_dim = 1
hidden_dim = 32*16*3
num_layers =  1
output_dim = 1


# Here we define our model as a class
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTM, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.num_layers = num_layers

        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 32, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states! 
        out = self.fc(out[:, -1, :]) 
        # out.size() --> 100, 10
        return out

model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

model2 = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

loss_fn = torch.nn.MSELoss()

loss_fn2 = torch.nn.MSELoss()

optimiser = torch.optim.Adam(model.parameters(), lr=0.01)
print(model)
print(len(list(model.parameters())))
for i in range(len(list(model.parameters()))):
    print(list(model.parameters())[i].size())
    

num_epochs = 110
hist1 = np.zeros(num_epochs)
hist2 = np.zeros(num_epochs)
# Number of steps to unroll
 

for t in range(num_epochs):
    # Initialise hidden state
    # Don't do this if you want your LSTM to be stateful
    #model.hidden = model.init_hidden()
    
    # Forward pass
    y_train_pred = model(x_goog_train)

    loss = loss_fn(y_train_pred, y_goog_train)
    if t % 10 == 0 and t !=0:
        print("Epoch ", t, "MSE: ", loss.item())
    hist1[t] = loss.item()

    # Zero out gradient, else they will accumulate between epochs
    optimiser.zero_grad()

    # Backward pass
    loss.backward()

    # Update parameters
    optimiser.step()
    
# for t in range(num_epochs):
#     # Initialise hidden state
#     # Don't do this if you want your LSTM to be stateful
#     #model.hidden = model.init_hidden()
    
#     # Forward pass
#     y_train_pred2 = model2(x_corr_train)

#     loss = loss_fn2(y_train_pred2, y_corr_train)
#     if t % 10 == 0 and t !=0:
#         print("Epoch ", t, "MSE: ", loss.item())
#     hist2[t] = loss.item()

#     # Zero out gradient, else they will accumulate between epochs
#     optimiser.zero_grad()

#     # Backward pass
#     loss.backward()

#     # Update parameters
#     optimiser.step()

plt.plot(hist1, label="Training loss")
plt.legend()
plt.show()

# plt.plot(hist2, label="Training loss")
# plt.legend()
# plt.show()

# make predictions
y_test_pred = model(x_goog_test)

# invert predictions
y_train_pred_inv = scaler_goog.inverse_transform(y_train_pred.detach().numpy())
y_train_inv = scaler_goog.inverse_transform(y_goog_train.detach().numpy())
y_test_pred_inv = scaler_goog.inverse_transform(y_test_pred.detach().numpy())
y_test_inv = scaler_goog.inverse_transform(y_goog_test.detach().numpy())

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(y_train_inv[:,0], y_train_pred_inv[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(y_test_inv[:,0], y_test_pred_inv[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[len(stock_data_goog)-len(y_goog_test):].index, y_test_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[len(stock_data_goog)-len(y_goog_test):].index, y_test_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction with RSI and Inflation')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction with RSI ONLY')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

def exp_1_setup_data(data1, data2):
    data_out=[]
    for index in range(1, len(data1)):
        data_out.append([data2[index], data1[index-1], data1[index]])
    data_out = np.array(data_out);
    test_set_size = int(np.round(0.2*data_out.shape[0]));
    train_set_size = data_out.shape[0] - (test_set_size);
    
    x_train = data_out[:train_set_size,:-1] #previous day's goog value and RSI
    y_train = data_out[:train_set_size,-1] #next day's goog value
    
    x_test = data_out[train_set_size:,:-1]  #previous day's goog value and RSI
    y_test = data_out[train_set_size:,-1] #next day's goog value
    
    return [x_train, y_train, x_test, y_test]


def exp_2_setup_data(data1, data2, data3, output):
    data_out=[]
    for index in range(1, len(data1)):
        data_out.append([data1[index-1], data2[index-1], data3[index-1], output[index]])
    data_out = np.array(data_out);
    test_set_size = int(np.round(0.2*data_out.shape[0]));
    train_set_size = data_out.shape[0] - (test_set_size);
    
    x_train = data_out[:train_set_size,:-1]
    y_train = data_out[:train_set_size,-1]
    
    x_test = data_out[train_set_size:,:-1]
    y_test = data_out[train_set_size:,-1]
    
    return [x_train, y_train, x_test, y_test]

x_goog_train, y_goog_train, x_goog_test, y_goog_test=exp_1_setup_data(scaled_goog_data, scaled_goog_rsi_data)


x_corr_train, y_corr_train, x_corr_test, y_corr_test=exp_2_setup_data(scaled_aapl_data, scaled_amzn_data, scaled_spy_data, scaled_goog_data)


x_goog_train = torch.from_numpy(x_goog_train).type(torch.Tensor)
x_goog_test = torch.from_numpy(x_goog_test).type(torch.Tensor)
y_goog_train = torch.from_numpy(y_goog_train).type(torch.Tensor)
y_goog_test = torch.from_numpy(y_goog_test).type(torch.Tensor)

x_corr_train = torch.from_numpy(x_corr_train).type(torch.Tensor)
x_corr_test = torch.from_numpy(x_corr_test).type(torch.Tensor)
y_corr_train = torch.from_numpy(y_corr_train).type(torch.Tensor)
y_corr_test = torch.from_numpy(y_corr_test).type(torch.Tensor)


# Build model
input_dim = 1
hidden_dim = 32*10
num_layers =  1
output_dim = 1


# Here we define our model as a class
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTM, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.num_layers = num_layers

        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 32, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states! 
        out = self.fc(out[:, -1, :]) 
        # out.size() --> 100, 10
        return out

model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

model2 = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

loss_fn = torch.nn.MSELoss()

loss_fn2 = torch.nn.MSELoss()

optimiser = torch.optim.Adam(model.parameters(), lr=0.01)
optimiser2 = torch.optim.Adam(model2.parameters(), lr=0.01)

print(model)
print(len(list(model.parameters())))
for i in range(len(list(model.parameters()))):
    print(list(model.parameters())[i].size())
    

num_epochs = 120
hist1 = np.zeros(num_epochs)
hist2 = np.zeros(num_epochs)
# Number of steps to unroll
 

for t in range(num_epochs):
    # Initialise hidden state
    # Don't do this if you want your LSTM to be stateful
    #model.hidden = model.init_hidden()
    
    # Forward pass
    y_train_pred = model(x_goog_train)

    loss = loss_fn(y_train_pred, y_goog_train)
    if t % 10 == 0 and t !=0:
        print("Epoch ", t, "MSE: ", loss.item())
    hist1[t] = loss.item()

    # Zero out gradient, else they will accumulate between epochs
    optimiser.zero_grad()

    # Backward pass
    loss.backward()

    # Update parameters
    optimiser.step()
    
for t in range(num_epochs):
    # Initialise hidden state
    # Don't do this if you want your LSTM to be stateful
    #model.hidden = model.init_hidden()
    
    # Forward pass
    y_train_pred2 = model2(x_corr_train)

    loss = loss_fn2(y_train_pred2, y_corr_train)
    if t % 10 == 0 and t !=0:
        print("Epoch ", t, "MSE: ", loss.item())
    hist2[t] = loss.item()

    # Zero out gradient, else they will accumulate between epochs
    optimiser2.zero_grad()

    # Backward pass
    loss.backward()

    # Update parameters
    optimiser2.step()

plt.plot(hist1, label="Training loss")
plt.legend()
plt.show()

plt.plot(hist2, label="Training loss")
plt.legend()
plt.show()

"""### Results of LSTM with RSI"""

# make predictions
y_test_pred = model(x_goog_test)

# invert predictions
y_train_pred_inv = scaler_goog.inverse_transform(y_train_pred.detach().numpy())
y_train_inv = scaler_goog.inverse_transform(y_goog_train.detach().numpy())
y_test_pred_inv = scaler_goog.inverse_transform(y_test_pred.detach().numpy())
y_test_inv = scaler_goog.inverse_transform(y_goog_test.detach().numpy())

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(y_train_inv[:,0], y_train_pred_inv[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(y_test_inv[:,0], y_test_pred_inv[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[len(stock_data_goog)-len(y_goog_test):].index, y_test_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[len(stock_data_goog)-len(y_goog_test):].index, y_test_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction with RSI')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

"""### Results of LSTM with correlated stock"""

# make predictions
y_test_pred = model2(x_corr_test)

# invert predictions
y_train_pred_inv = scaler_goog.inverse_transform(y_train_pred2.detach().numpy())
y_train_inv = scaler_goog.inverse_transform(y_corr_train.detach().numpy())
y_test_pred_inv = scaler_goog.inverse_transform(y_test_pred.detach().numpy())
y_test_inv = scaler_goog.inverse_transform(y_corr_test.detach().numpy())

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(y_train_inv[:,0], y_train_pred_inv[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(y_test_inv[:,0], y_test_pred_inv[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[len(stock_data_goog)-len(y_corr_test):].index, y_test_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[len(stock_data_goog)-len(y_corr_test):].index, y_test_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction with Correlated Stocks')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()

# Visualising the results
figure, axes = plt.subplots(figsize=(15, 6))
axes.xaxis_date()

axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_inv, color = 'red', label = 'Real Google Stock Price')
axes.plot(stock_data_goog[:len(y_train_inv)].index, y_train_pred_inv, color = 'blue', label = 'Predicted Google Stock Price')

#axes.xticks(np.arange(0,394,50))
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
#plt.savefig('google_pred.png')
plt.show()