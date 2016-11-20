import numpy as np
import pandas as pd
import quandl
import os.path
daily_stock_data_directory = 'C:\\Peace\\StockData\\Daily\\'
auth_key = ''   # input qundl key here.

def fetch_quandl_stock(my_securities):
    # fetch_quandl_stock will directly get a list of stocks with all historical data quandl has. 
    for tick in my_securities:
        tick_name = "WIKI/" + tick
        tick_data = quandl.get(tick_name, returns="pandas",authtoken = "sw1wiPPJnCGXBnPdZG2k")
        name_string = daily_stock_data_directory + tick + ".csv"
        tick_data.to_csv(name_string)
    return True

def read_local_stock_data(my_securities, **kwargs):
    # Parameter: my_securities, start_day, end_day
    # my_securities is a list of string. the string is the name of the stock
    # start_day is in a string form like "2016-11-18"
    # end_day is also in that format
    # the function will return a list of stock. each element is the stock data corresponding to that stock
    stock_data = []
    for tick in my_securities:
        # Read daily stock data from specific directory
        tick_directory = daily_stock_data_directory + tick + '.csv'
        if(not(os.path.isfile(tick_directory))):# file doen't exsite, need download
            fetch_quandl_stock([tick])
        # Read in csv, convert into panda
        tick_raw_data = pd.read_csv(tick_directory)
        # the datetime read in is string type currently, convert it into datetime type. Then reset index to Date
        date = pd.to_datetime(tick_raw_data['Date'], format = "%Y-%m-%d")
        tick_raw_data = tick_raw_data.drop("Date", 1)
        tick_raw_data['Date'] = date
        tick_data = tick_raw_data.set_index('Date')
    
    if kwargs is not None:
        if ('start_day' in kwargs.keys()) & ('end_day' not in kwargs.keys()):
            # return back data from start date to now
            start_date = kwargs['start_day']
            s_d = pd.to_datetime(start_date)
            if(s_d in tick_data.index):
                tick_data = tick_data.loc[s_d:]
                stock_data.append(tick_data)
            else:
                temp_str = s_d + " isn't a trading day of" +tick
                print(temp_str)
                return False
        elif (('start_day' not in kwargs.keys())&('end_day' in kwargs.keys())):
            # return data from the beginning of stock to end day
            end_date = kwargs['end_day']
            e_d = pd.to_datetime(end_date)
            if(e_d in tick_data.index):
                tick_data = tick_data.loc[:e_d]
                stock_data.append(tick_data)
            else:
                temp_str = e_d + " isn't a trading day of" +tick
                print(temp_str)
                return False
        elif (('start_day' in kwargs.keys())&('end_day' in kwargs.keys())):
            # return data between start and end day
            start_date = kwargs['start_day']
            end_date = kwargs['end_day']
            s_d = pd.to_datetime(start_date)
            e_d = pd.to_datetime(end_date)
            if (s_d in tick_data.index):
                if(e_d in tick_data.index):
                    tick_data = tick_data.loc[s_d:e_d]
                    stock_data.append(tick_data)
                else:
                    temp_str = e_d + " isn't a trading day of" +tick
                    print(temp_str)
                    return False
            else:
                temp_str = s_d + " isn't a trading day of" +tick
                print(temp_str)
                return False
    else:# so user doesn't input start and end day, we will just return all the data we got.
        pass
    stock_data.append(tick_data)

        
    return stock_data