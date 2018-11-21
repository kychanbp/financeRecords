import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
data = pd.read_csv("sampleData.csv")
#print(data)
#data = data.astype(object).where(pd.notnull(data), None)

#connect to sqlite
db = sqlite3.connect("records")

for index, row in data.iterrows():
    date = datetime.strptime(row['Date'], "%d/%m/%Y").date()
    #print(row['Remarks'])
    if pd.isna(row['Remarks']) == True:
        query = 'INSERT INTO Entry (Date, Category, Accounts, Cash_Flow) VALUES ("{}", "{}", "{}", {})'.format(date, row['Category'], row['Accounts'], row['Cash Flow'])
    else:
        query = 'INSERT INTO Entry (Date, Category, Accounts, Cash_Flow, Remarks) VALUES ("{}", "{}", "{}", {}, "{}")'.format(date, row['Category'], row['Accounts'], row['Cash Flow'], row['Remarks'])

    try:
        cur = db.cursor()
        cur.execute(query)
    except:
        print(index)

db.commit()
