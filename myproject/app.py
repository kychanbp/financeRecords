from .server import app, server
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import calendar
from datetime import datetime
from datetime import date

import sqlite3
import pandas as pd 

import myproject.functions as func

dt = datetime.now()

#connect to sqlite
db = sqlite3.connect("records")
table1 = pd.read_sql_query("SELECT * FROM {}".format('Entry'), db)
table2 = pd.read_sql_query("SELECT * FROM {}".format('Statm'), db)
category = table1['Category'].unique()
accounts = table1['Accounts'].unique()

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Entry', value='tab-1'),
        dcc.Tab(label='Dashboard', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

tab_1 = html.Div([
    #row
    #html.Div(className = "row", children = [html.H1('Data Entry')]),

    #row
    html.Div(
        className = "row",
        children = [
            dcc.DatePickerRange(
                id='dateRange',
                display_format='Y-M-D',
                start_date = date(dt.year, dt.month, 1),
                end_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])
            )
        ]
    ),

    #row
    html.Div(
        className = "row",
        children = [
            html.Div(
                className = "two columns",
                children = [html.H6("Category")]
            ),

            html.Div(
                className = "four columns",
                children = [
                    dcc.Dropdown(
                        id='category',
                        options=[{'label': s[0], 'value': str(s[1])}for s in zip(category, category)],
                        multi=False,
                        clearable=True
                        )
                ]
            ),

            html.Div(
                className = "two columns",
                children = [html.H6("Account")]
            ),

            html.Div(
                className = "four columns",
                children = [
                    dcc.Dropdown(
                        id='account',
                        options=[{'label': s[0], 'value': str(s[1])}for s in zip(accounts, accounts)],
                        multi=False,
                        clearable=True
                        )
                ]
            ),


        ]
    ),

    html.Div(
        className = "row",
        children = [
            html.Div(className = "two columns", children = [html.Div(html.H6('Cash Flow'))]),
            html.Div(
                className = "four columns",
                children = [
                    dcc.Input(
                        id = "cashFlow",
                        placeholder='Enter a value...',
                        type='number',
                        value=0,
                        debounce=True
                    ),
                    
                ]
            ),
            html.Div(className = "two columns", children = [html.Div(html.H6('Remarks'))]),
            html.Div(
                className = "four columns",
                children = [
                    dcc.Input(
                        id = "remarks",
                        placeholder='Enter a value...',
                        type='text',
                        value='Default',
                        debounce=True
                    ),
                    
                ]
            ),
                
            
        ]
    ),

    #row
    html.Div(
        className = "row",
        children = [
            html.Button('Submit', id='button')
        ]
    ),

    html.Div(id='output-container-button', children = 'Waiting'),

    #row
    html.Div(html.H2('Records')),

    #row
    html.Div(
        className = "row",
        children = [
            html.Div(
                className="twlve columns",
                children = html.Div([
                    dash_table.DataTable(id = 'records'),
                    ]
                )
            )
        ]
    )

])

tab_2 = html.Div([
    #row
    html.Div(
        className = "row",
        children = [
            dcc.DatePickerRange(
                id='dateRange',
                display_format='Y-M-D',
                start_date = date(dt.year, dt.month, 1),
                end_date = date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])
            )
        ]
    ),

    #row
    html.Div(
        className = 'row',
        children = [
            html.Div(
                className = 'columns',
                children = [dcc.Graph(id = 'bullet')]
            )
        ]
    ),


    #row
    html.Div(
        className = "row",
        children = [
            html.Div(
                className = "six columns",
                children = [dcc.Graph(id = 'trend')]
            ),
            html.Div(
                className = "six columns",
                children = [dcc.Graph(id = 'pattern')]
            )
        ]
    ),

    #row
    html.Div(
        className = "row",
        children = [
            html.Div(
                className = "twelve columns",
                children = [dash_table.DataTable(id = 'breakdown')]
            )
        ]
    ),

    
])

@app.callback(dash.dependencies.Output('tabs-content', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-2':
        return tab_2
    elif tab == 'tab-1':
        return tab_1

from . import callbacks