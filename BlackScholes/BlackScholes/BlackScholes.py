import numpy as np
from scipy.stats import norm
import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import date

def program():
    x = input("Enter Your Company Ticker:")

    stock = yf.Ticker(x)
    opt = stock.options
    print(opt)

    y = input("Choose Your Date(YYYY-MM-DD):")
    opt1 = stock.option_chain(date=y).calls
    df = pd.DataFrame(opt1)

    def new_func(df):
        print(df[df.columns[0:3]])

    new_func(df)
    z = int(input("Choose Your Option Contract(0-n):"))

    print("Gathering Data.....")
    print("Generating BlackScholes Model Fair Value.....")

    delta = datetime.strptime(y, '%Y-%m-%d') - datetime.today()
    delta = delta.days

    current_price = stock.history().tail(1)['Close'].iloc[0]
    current_price = round(current_price, 2)

    i = opt1['openInterest'][z]
    r = i/10000
    S = current_price
    K = opt1['strike'][z]
    T = delta/365
    sigma = opt1['impliedVolatility'][z]

    def blackScholes(r, S, K, T, sigma, type='C'):
        "Calculate BS Option Price for a Call/Put"
        d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        try:
            if type == "C":
                price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
            elif type == "P":
                price = k*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
            return price
        except:
            print("Please Confirm All Option Parameters Above!!")

    print("Current Ask Price: ", opt1['ask'][z])
    print("Current Open Interest: ",r)
    print("Strike Price: ", K)
    print("Current Stock Price: ", round(S, 2))
    print("Expires in: ", delta, "days")
    print("Option Price is: ", round(blackScholes(r, S, K, T, sigma, type="C"), 2) )
    
    def y_n():
        j = input("Check Another Option Chain(Y/n): ")

        if j.lower() == 'y':
            print("------------------------------------")
            program()
        elif j.lower() == 'n':
            exit()
        else:
            print("Invalid Input, Try Again!")
            y_n()
    y_n()
program()







