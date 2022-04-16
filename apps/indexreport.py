import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash, json
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output
import sys, json, pymongo
from datetime import datetime, timedelta, datetime, date
from collections import OrderedDict
from time import sleep
from app import app

conn = pymongo.MongoClient(host='localhost', port=27017)
db = conn.qareports

dateslist = []
sevenlist = []
n = 0
while n < 7:
    sevendays = datetime.strftime(datetime.date(datetime.now()) - timedelta(days=n), '%m-%d')
    fullseven = datetime.strftime(datetime.date(datetime.now()) - timedelta(days=n), '%m-%d-%Y')
    dateslist.append(sevendays)
    sevenlist.append(fullseven)
    n += 1

# dateslist = ['03-29', '03-28', '03-27', '03-26', '03-25', '03-24', '03-23']
sevenlist.reverse()
dateslist.reverse()
dateslist[-1] = 'Today'

datesdict = {i: val for i, val in enumerate(dateslist)}
datesdict = OrderedDict(sorted(datesdict.items()))

key = list(datesdict.keys())

with open('panoindex.json', 'r') as pdj:
    opt = json.load(pdj)

tabs_styles = {
    'height': '50px',
    'padding-left': '110px',
    'display': 'flex'
}
tab_style = {
    'padding-left': '26px',
    'width': 'auto',
}
tab_selected_style = {
    'fontWeight': 'bold',
    'width':'auto',
    'padding-left': '26px',
    'border-top-color': '#FF4D00',
}

# CONTENT THAT REQUIRED ON TAB 1 SELECTION
children_container1 = [
    html.Div(className='row', children=[
        html.Div([
            html.Div([html.P('OldCount')]),

            html.Div([html.Div(id='iolddisplay')], style={"font-size": "30px"}),
        ], style={"border": "1px solid #FF4D00", "background-color": "rgb(42, 52, 60)", "margin-left": "20px",
                  "padding-left": "25px", "padding-right": "25px", 'text-align': 'center', "border-radius": "7px",
                  "color": "white"}),

        html.Div([
            html.Div([html.P('NewCount')]),

            html.Div([html.Div(id='inewdisplay')], style={"font-size": "30px"}),
        ], style={"border": "1px solid #FF4D00", "background-color": "rgb(42, 52, 60)", "margin-left": "20px",
                  "padding-left": "25px", "padding-right": "25px", 'text-align': 'center', "border-radius": "7px",
                  "color": "white"}),
    ]),

    html.Br(),

    html.Div(children=[
        dash_table.DataTable(
            id="idxtable",
            # filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={'maxHeight': '400px', 'overflowY': 'scroll', 'overflowX': 'scroll'},
            style_cell={
                'font-family': 'Verdana',
                'fontSize': 10,
            },
            style_cell_conditional=[
                {
                    'textAlign': 'left'
                }
            ],
            # fixed_rows={'headers': True},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
    ]),
]

layout = html.Div(children=[

    html.Div(className="row", children=[
        html.Div(children=[
            dcc.Dropdown(
                id='ifirstdropdown',
                options=[{"label": i, "value": i.lower()} for i in opt[0]['RELEASES']],
                value=opt[0]['RELEASES'][0]
            )], style={'width': '25%', 'padding': '10px'}),
        html.Div(children=[
            dcc.Dropdown(
                id='iseconddropdown',
            )], style=dict(width='25%', padding='10px')),
        html.Div(children=[
            dcc.Dropdown(
                id='ithirddropdown'
            )], style=dict(width='25%', padding='10px')),
    ], style=dict(display='flex', fontsize='5')),

    html.Br(),

    html.Div(className="row", children=[
        html.Div(children=[
            dcc.Slider(id='Dateslider', min=key[0], max=key[-1], marks=datesdict, value=key[-1]
                       )], style={'width': '50%', 'color': '#FF4D00'}),
        html.Div(children=[dcc.Tabs(id="itabs-styled-with-inline", value='tab1', children=[
                dcc.Tab(label='Overall Report', value='tab1', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
        ])
    ]),

    html.Hr(style={"background-color": "#FF4D00"}),

    dcc.Loading(id="loading-1", type="cube", fullscreen="true",
                style={'backgroundColor': 'transparent', 'backdrop-filter': 'blur(2px)'},
    children=[
        html.Div(id="itab-1-output"),
        ]
    ),

])


# CALL BACK FUNCTIONS FOR DROPDOWN
# INPUT - RELEASE NO
# OUTPUT - ENVIRONMENT BASED ON RELEASE {'LABEL', 'VALUE'}
@app.callback(
    Output('iseconddropdown', 'options'),
    Input('ifirstdropdown', 'value')
)
def sendfirstreturn(firstopt):
    return [{'label':j, 'value':j.lower()} for j in opt[1][firstopt.upper()]]

# INPUT - ENVIRONMENT {'LABEL', 'VALUE'}
# OUTPUT - DEFAULT VALUE (ENVIRONMENT)
@app.callback(
    Output('iseconddropdown', 'value'),
    Input('iseconddropdown', 'options')
)
def sendsecondreturn(secondopt):
    return secondopt[0]['value']

# INPUT - ENVIRONMENT NAME
# OUTPUT - DAYPART BASED ON ENV NAME {'LABEL':'VALUE'}
@app.callback(
    Output('ithirddropdown', 'options'),
    [Input('iseconddropdown', 'value'),
     Input('ifirstdropdown', 'value')])
def thirdreturnone(thirdoptval, firstdropval):
    return [{'label':k, 'value':k.lower()} for k in opt[2][f'{firstdropval.upper()} {thirdoptval.upper()}']]

# INPUT - DAYPART {'LABEL':'VALUE'}
# OUTPUT - DEFAULT VALUE (DAYPART)
@app.callback(
    Output('ithirddropdown', 'value'),
    Input('ithirddropdown', 'options')
)
def thirdreturntwo(thirdoptopt):
    return thirdoptopt[0]['value']

# INPUT - DAYPART NAME
# OUTPUT - DEFAULT VALUE ('DIFF SHEET' OR 'REGULAR SHEET') & DISABLE STATE ON CONDITION
@app.callback(
    [Output('ilastdropdown', 'disabled'),
    Output('ilastdropdown', 'value')],
    Input('ithirddropdown', 'value')
)
def finalreturn(val):
    if val.lower() == 'evening':
        return False, 'yes'
    else:
        return True, 'no'


@app.callback(
    Output('itab-1-output','children'),
    [Input('itabs-styled-with-inline', 'value')]
)
def tabreturn(tab):
    if tab == 'tab1':
        return children_container1


# CALL BACK FUNCTION FOR THE COUNTS TO DISPLAY
@app.callback(
    Output('iolddisplay', 'children'),
    Output('inewdisplay', 'children'),
    [Input('Dateslider', 'value'),
     Input('ifirstdropdown', 'value'),
     Input('iseconddropdown', 'value'),
     Input('ithirddropdown', 'value'),
     ])
def resultdata01return(dateval2, fstrel2, secenv2, thrddayp2):
    if datesdict[dateval2] == 'Today':
        datevalnow2 = datetime.strftime(datetime.date(datetime.now()), '%m-%d-%Y')
    else:
        datevalnow2 = datetime.strftime(datetime.strptime(sevenlist[dateval2], '%m-%d-%Y'), '%m-%d-%Y')

    countdata = list(db.indexreports.find(
        {'date': datevalnow2, 'release': fstrel2, 'region': secenv2, 'time': thrddayp2}, {'oldcount': 1, 'newcount': 1, '_id': 0}))
    if len(countdata) > 0:
        value01 = countdata[0]["oldcount"]
        value02 = countdata[0]["newcount"]
        return value01, value02
    else:
        return '00000', '00000'


# CALL BACK FUNCTION FOR TABLES
@app.callback(
    Output('idxtable', 'data'),
    Output('idxtable', 'columns'),
    Output('idxtable', 'export_format'),
    Output('idxtable', 'style_table'),
    [Input('Dateslider', 'value'),
     Input('ifirstdropdown', 'value'),
     Input('iseconddropdown', 'value'),
     Input('ithirddropdown', 'value'),
     ])
def resultdatareturn(dateval1, fstrel1, secenv1, thrddayp1):
    if datesdict[dateval1] == 'Today':
        datevalnow1 = datetime.strftime(datetime.date(datetime.now()), '%m-%d-%Y')
    else:
        datevalnow1 = datetime.strftime(datetime.strptime(sevenlist[dateval1], '%m-%d-%Y'), '%m-%d-%Y')

    outdata1 = list(db.indexreports.find(
            {'date': datevalnow1, 'release': fstrel1, 'region': secenv1, 'time': thrddayp1}, {'data': 1, '_id': 0}))

    try:
        content = (list(outdata1))[0]['data']
    except IndexError:
        content = []
        styletable = {'display': 'none'}
        excel = ''
    else:
        styletable = {'maxHeight': '400px', 'overflowY': 'scroll', 'overflowX': 'scroll'}
        excel = 'xlsx'

    df = pd.DataFrame(data=content)
    cols = list(df.columns)
    columns = [{"name": i, "id": i} for i in cols]

    if len(df) > 0:
        df = df.replace('<NA>', '', regex=True)
        df = df.replace(['None'], [''], regex=True)
        df.set_index('FileName')
    else:
        pass

    return df.to_dict('records'), columns, excel, styletable