from .server import app

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import sqlite3

import myproject.functions as func

@app.callback(
    dash.dependencies.Output("bullet",'figure'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_bullet(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    spending = func.spending(db, "Entry", "Statm", start_date, end_date)
    #data = [{'Spending':[spending], 'Range':[5000, 8000], 'Marker':[10000]}]
    #fig = ff.create_bullet(data, markers='Marker', measures='Spending', ranges='Range')

    
    data = (
    {"label": "Spending", "sublabel": "HKD",
    "range": [-12000, -8000, -5000, 10000], "performance": [spending, 0], "point": [-10000]},
    )
    

    fig = ff.create_bullet(
        data, titles='label', subtitles='sublabel', markers='point',
        measures='performance', ranges='range', horizontal_spacing=None)
    
    return fig

@app.callback(
    dash.dependencies.Output("trend",'figure'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_trend(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")

    df = func.trendAcct(db, "Entry", "Statm", end_date)

    line_assets = go.Scatter(x=df['Date'],
                        y=df['Assets'],
                        showlegend=True,
                        mode='lines',
                        name='Assets'
                        )
    

    line_liabilities = go.Scatter(x=df['Date'],
                        y=df['Liabilities'],
                        showlegend=True,
                        mode='lines',
                        name='Liabilities'
                        )
    
    line_equities = go.Scatter(x=df['Date'],
                        y=df['Equities'],
                        showlegend=True,
                        mode='lines',
                        name='Equities'
                        )

    data = [line_assets, line_liabilities, line_equities]
    layout = dict(xaxis = dict(zeroline = False,
                            linewidth = 1,
                            mirror = True),
                yaxis = dict(zeroline = False, 
                            linewidth = 1,
                            mirror = True),
                title = 'Change in Assets, Liabilities, Equities'
                )

    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    dash.dependencies.Output("pattern",'figure'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_pattern(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    spending = func.spending_pattern(db, "Entry", "Statm", start_date, end_date)

    pie = go.Pie(labels=spending['Category'].tolist(), values=spending['Cash_Flow'].tolist())
    data = [pie]

    layout = dict(title = 'Spending Pattern')

    fig = dict(data=data, layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output("breakdown",'columns'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_breakdown_columns(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.account_summary(db, "Entry","Statm", end_date)
    columns=[{"name": i, "id": i} for i in df.columns]
    return columns


@app.callback(
    dash.dependencies.Output("breakdown",'data'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_breakdown_rows(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.account_summary(db, "Entry","Statm", end_date)
    data=df.to_dict('records')
    return data

@app.callback(
    dash.dependencies.Output("receivables",'columns'),
    [dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_receivables_columns(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.account_receivables(db, "Entry","Statm", end_date)
    columns=[{"name": i, "id": i} for i in df.columns]
    return columns


@app.callback(
    dash.dependencies.Output("receivables",'data'),
    [
dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_receivables_rows(start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.account_receivables(db, "Entry","Statm", end_date)
    data=df.to_dict('records')
    return data

@app.callback(
    dash.dependencies.Output("records",'columns'),
    [dash.dependencies.Input('button', 'n_clicks'),
    dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_records_columns(n_clicks, start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.records(db, "Entry","Statm",start_date, end_date)
    columns=[{"name": i, "id": i} for i in df.columns]
    return columns


@app.callback(
    dash.dependencies.Output("records",'data'),
    [dash.dependencies.Input('button', 'n_clicks'),
    dash.dependencies.Input('dateRange', 'start_date'),
    dash.dependencies.Input('dateRange', 'end_date')])
def update_records_rows(n_clicks, start_date, end_date):
    #connect to sqlite
    db = sqlite3.connect("records")
    df = func.records(db, "Entry","Statm",start_date, end_date)
    data=df.to_dict('records')
    return data[-20:]

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    state=[dash.dependencies.State('category', 'value'),
    dash.dependencies.State('account', 'value'),
    dash.dependencies.State('cashFlow', 'value'), 
    dash.dependencies.State('remarks', 'value')])
def push_record(n_clicks, category, account, cashFlow, remarks):
    #connect to sqlite
    db = sqlite3.connect("records")
    if category is None or account is None or cashFlow == 0:
        query = "No value"

    else:
        if remarks == 'Default':
            query = 'INSERT INTO Entry (Category, Accounts, Cash_Flow) VALUES ("{}", "{}", {})'.format(category, account, cashFlow)
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            db.close()
        elif remarks != 'Default' or remarks == '':
            query = 'INSERT INTO Entry (Category, Accounts, Cash_Flow, Remarks) VALUES ("{}", "{}", {}, "{}")'.format(category, account, cashFlow, remarks)
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            db.close()

    return query