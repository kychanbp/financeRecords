import pandas as pd 
import sqlite3

data = pd.read_csv("sampleData.csv")

grouped = data.groupby(['Accounts', 'Statement', 'Subcategories']).size().reset_index()
statm = grouped[['Accounts', 'Statement', 'Subcategories']]
#print(statm)

#connect to sqlite
db = sqlite3.connect("records")

for index, row in statm.iterrows():
    query = 'INSERT INTO Statm (Accounts, Statements, Sub_Statements) VALUES ("{}", "{}", "{}")'.format(row['Accounts'], row['Statement'], row['Subcategories'])
    #print(query)
    try:
        cur = db.cursor()
        cur.execute(query)
    except:
        print(index)

db.commit()