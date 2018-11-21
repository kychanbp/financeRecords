import sqlite3
import pandas as pd 
import calendar
from datetime import datetime
from datetime import date

#connect to sqlite
db = sqlite3.connect("records")

#function to get records
def records(db, table1, table2, start_date, end_date):
    table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    start_date =  datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    fiat = pd.merge(table1, table2, on=['Accounts'])
    fiat['Date'] = pd.to_datetime(fiat['Date'])
    fiat['Date'] = fiat['Date'].dt.date
    fiat = fiat[(fiat['Date'] >= start_date) & (fiat['Date'] <= end_date)]
    fiat = fiat.sort_values(by=['Date'])

    return fiat
    
#function to calculate a, l, e
def acctVar(db, table1, table2, start_date, end_date):
    #table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    #table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    start_date =  datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    fiat = pd.merge(table1, table2, on=['Accounts'])
    fiat['Date'] = pd.to_datetime(fiat['Date'])
    fiat['Date'] = fiat['Date'].dt.date
    fiat = fiat[(fiat['Date'] >= start_date) & (fiat['Date'] <= end_date)]

    results = fiat.groupby('Statements').sum()['Cash_Flow']
    Assets = results['Assets']
    Liabilities = results['Liabilities']
    Equities = Assets + Liabilities
    return Assets, Liabilities, Equities

#function to calculate the trend of a, l, e
def trendAcct(db, table1, table2):
    table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    dates = table1['Date'].tolist()
    dates = list(set(dates))
    dates.sort()

    results = []
    for date in dates[1:]:
        rollData = acctVar(db, table1, table2, dates[0], date)
        temp = {}
        temp['Date'] = date
        temp['Assets'] = rollData[0]
        temp['Liabilities'] = rollData[1]
        temp['Equities'] = rollData[2]
        results.append(temp)
    
    return pd.DataFrame(results)



#function to calculate monthly spending
def spending(db, table1, table2, start_date, end_date):
    #dt = datetime.strptime(dt, '%Y-%m-%d')
    #start_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[0])
    #end_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])

    start_date =  datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    fiat = pd.merge(table1, table2, on=['Accounts'])

    fiat['Date'] = pd.to_datetime(fiat['Date'])
    fiat['Date'] = fiat['Date'].dt.date

    fiat = fiat[(fiat['Date'] >= start_date) & (fiat['Date'] <= end_date)]

    return fiat['Cash_Flow'].sum()

#function to calculate monthly spending pattern
def spending_pattern(db, table1, table2, start_date, end_date):
    #dt = datetime.strptime(dt, '%Y-%m-%d')
    #start_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[0])
    #end_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])

    start_date =  datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    fiat = pd.merge(table1, table2, on=['Accounts'])

    fiat['Date'] = pd.to_datetime(fiat['Date'])
    fiat['Date'] = fiat['Date'].dt.date

    fiat = fiat[(fiat['Date'] >= start_date) & (fiat['Date'] <= end_date)]
    fiat['Cash_Flow'] = fiat['Cash_Flow']*-1 #excluded income (multipied -1)
    fiat = fiat.groupby('Category')['Accounts','Cash_Flow'].sum()
    fiat.reset_index(inplace=True)
    return fiat

#function to get account summary
def account_summary(db,table1, table2 ):
    table1 = pd.read_sql_query("SELECT * FROM {}".format(table1), db)
    table2 = pd.read_sql_query("SELECT * FROM {}".format(table2), db)

    fiat = pd.merge(table1, table2, on=['Accounts'])

    fiat['Date'] = pd.to_datetime(fiat['Date'])
    fiat['Date'] = fiat['Date'].dt.date

    fiat = fiat.groupby('Accounts').sum()
    fiat.reset_index(inplace=True)

    return fiat
print(account_summary(db, "Entry", "Statm"))
#print(spending_pattern(db, "Entry", "Statm", "2018-11-01", "2018-11-30"))