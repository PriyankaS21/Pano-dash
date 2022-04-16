import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import json
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output
import sys
import json
import pymongo
from datetime import datetime, timedelta, datetime, date
from collections import OrderedDict
from time import sleep
from app import app

conn = pymongo.MongoClient(host='localhost', port=27017)
db = conn.qareports


# dateslist = []
# sevenlist = []
# n = 0
# while n < 7:
#     sevendays = datetime.strftime(datetime.date(
#         datetime.now()) - timedelta(days=n), '%m-%d')
#     fullseven = datetime.strftime(datetime.date(
#         datetime.now()) - timedelta(days=n), '%m-%d-%Y')
#     dateslist.append(sevendays)
#     sevenlist.append(fullseven)
#     n += 1

# # dateslist = ['03-29', '03-28', '03-27', '03-26', '03-25', '03-24', '03-23']
# sevenlist.reverse()
# dateslist.reverse()
# dateslist[-1] = 'Today'

# datesdict = {i: val for i, val in enumerate(dateslist)}
# datesdict = OrderedDict(sorted(datesdict.items()))

# key = list(datesdict.keys())

with open('panodash.json', 'r') as pdj:
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
    'width': 'auto',
    'padding-left': '26px',
    'border-top-color': '#FF4D00',
}

# CONTENT THAT REQUIRED ON TAB 1 SELECTION
children_container1 = [
    html.Div(className='row', children=[
        html.Div([
            html.Div([html.P('OldCount')]),

            html.Div([html.Div(id='olddisplay')],
                     style={"font-size": "30px"}),
        ], style={"border": "1px solid #FF4D00", "background-color": "rgb(42, 52, 60)", "margin-left": "20px", "padding-left": "25px", "padding-right": "25px", 'text-align': 'center', "border-radius": "7px", "color": "white"}),

        html.Div([
            html.Div([html.P('NewCount')]),

            html.Div([html.Div(id='newdisplay')],
                     style={"font-size": "30px"}),
        ], style={"border": "1px solid #FF4D00", "background-color": "rgb(42, 52, 60)", "margin-left": "20px", "padding-left": "25px", "padding-right": "25px", 'text-align': 'center', "border-radius": "7px", "color": "white"}),

        html.Div(children=[
            dcc.Dropdown(
                id='1sttabdropdowns',
                # options = [{"label":r, "value":r} for r in opt[3]['ExcelSheets']],
                # value = opt[3]['ExcelSheets'][1],
            )
        ], style={'width': '60%', 'padding-left': '10px', 'padding-left': '290px'}),
    ]),

    html.Br(),

    html.Div(children=[
        dcc.Graph(id="QaBarChart")
    ]),

    html.Br(),

    html.Div(children=[
        dash_table.DataTable(
            id="qatable",
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            # style_as_list_view=True,
            style_table={'maxHeight': '1750px', 'maxWidth': '500px',
                         'overflowY': 'scroll', 'overflowX': 'scroll'},
            # style_cell = {
            #   'font-family':'Verdana',
            #   'fontSize':10,
            # },
            style_cell={
                'textAlign': 'center',
                'font-family': 'Verdana',
                'fontSize': 10,
                'color': 'black',
                'backgroundColor': 'white',
                'padding': '15px 5px'
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
                    'backgroundColor': 'rgb(227, 225, 225)',
                    'color': 'black',
                }
            ],
            style_header={
                # 'backgroundColor': 'rgb(230, 230, 230)',
                'backgroundColor': 'rgb(51, 51, 77)',
                'fontWeight': 'bold',
                'fontSize': 12,
                'color': 'white'
            }
        )
    ]),
]

# CONTENT THAT REQUIRED ON TAB 2 SELECTION
children_container2 = [
    html.Div(children=[
        dcc.Dropdown(
            id='2ndtabdropdowns',
        )
    ], style={'width': '35%', 'padding-left': '10px', 'margin-left': '580px'}),

    # html.Div(children=[html.H1('Under Construction')])
    html.Div(children=[
        html.Div(children=[
            dash_table.DataTable(
                id='unhidesheet',
                filter_action="native",
                sort_action="native",
                sort_mode="multi",

                # style_cell={
                #             'font-family': 'Verdana',
                #             'fontSize': 10,
                # },
                style_cell={
                    'textAlign': 'center',
                    'font-family': 'Verdana',
                    'fontSize': 10,
                    'color': 'black',
                    'backgroundColor': 'white',
                    'padding': '15px 5px'
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
                        'backgroundColor': 'rgb(227, 225, 225)',
                        'color': 'black',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(51, 51, 77)',
                    'fontWeight': 'bold',
                    'fontSize': 12
                }
            )
        ])
    ])
]


layout = html.Div(children=[

    html.Div(className="row", children=[
        html.Div(children=[
            dcc.Dropdown(
                id='firstdropdown',
                options=[{"label": i, "value": i.lower()}
                         for i in opt[0]['RELEASES']],
                value=opt[0]['RELEASES'][0]
            )], style={'width': '25%', 'padding-left': '10px'}),
        html.Div(children=[
            dcc.Dropdown(
                id='seconddropdown',
            )], style={'width': '25%', 'padding-left': '10px'}),
        html.Div(children=[
            dcc.Dropdown(
                id='thirddropdown'
            )], style={'width': '25%', 'padding-left': '10px'}),
        html.Div(children=[
            dcc.Dropdown(
                id='lastdropdown',
                options=[{"label": 'Difference Sheet', "value": "yes"}, {
                    "label": "Regular Sheet", "value": "no"}],
            )], style={'width': '25%', 'padding-left': '10px'})
    ], style=dict(display='flex', fontsize='5')),

    html.Br(),

    html.Div(className="row", children=[
        html.Div(children=[
            dcc.DatePickerSingle(id='Dateslider', min_date_allowed=date(2021, 7, 1),
                                 max_date_allowed=datetime.date(
                                     datetime.now()),
                                 initial_visible_month=datetime.date(
                                     datetime.now()),
                                 date=datetime.date(datetime.now()), day_size=39)
        ], style={'width': '50%', 'padding-left': '10px'}),
        html.Div(children=[dcc.Tabs(id="tabs-styled-with-inline", value='tab1', children=[
            dcc.Tab(label='Overall Report', value='tab1',
                    style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='TestCase Report', value='tab2',
                    style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        ]),
    ]),

    html.Hr(style={"background-color": "#FF4D00"}),

    dcc.Loading(id="loading-1", type="cube", fullscreen="true", style={'backgroundColor': 'transparent', 'backdrop-filter': 'blur(2px)'},

                children=[
        html.Div(id="tab-1-output"),
    ]),
])

# CALL BACK FUNCTIONS FOR DROPDOWN
# INPUT - RELEASE NO
# OUTPUT - ENVIRONMENT BASED ON RELEASE {'LABEL', 'VALUE'}


@app.callback(
    Output('seconddropdown', 'options'),
    Input('firstdropdown', 'value')
)
def sendfirstreturn(firstopt):
    return [{'label': j, 'value': j.lower()} for j in opt[1][firstopt.upper()]]

# INPUT - ENVIRONMENT {'LABEL', 'VALUE'}
# OUTPUT - DEFAULT VALUE (ENVIRONMENT)


@app.callback(
    Output('seconddropdown', 'value'),
    Input('seconddropdown', 'options')
)
def sendsecondreturn(secondopt):
    return secondopt[0]['value']

# INPUT - ENVIRONMENT NAME
# OUTPUT - DAYPART BASED ON ENV NAME {'LABEL':'VALUE'}


@app.callback(
    Output('thirddropdown', 'options'),
    [Input('seconddropdown', 'value'),
     Input('firstdropdown', 'value')])
def thirdreturnone(thirdoptval, firstdropval):
    return [{'label': k, 'value': k.lower()} for k in opt[2][f'{firstdropval.upper()} {thirdoptval.upper()}']]

# INPUT - DAYPART {'LABEL':'VALUE'}
# OUTPUT - DEFAULT VALUE (DAYPART)


@app.callback(
    Output('thirddropdown', 'value'),
    Input('thirddropdown', 'options')
)
def thirdreturntwo(thirdoptopt):
    return thirdoptopt[0]['value']

# INPUT - DAYPART NAME
# OUTPUT - DEFAULT VALUE ('DIFF SHEET' OR 'REGULAR SHEET') & DISABLE STATE ON CONDITION


@app.callback(
    [Output('lastdropdown', 'disabled'),
     Output('lastdropdown', 'value')],
    Input('thirddropdown', 'value')
)
def finalreturn(val):
    if val.lower() == 'evening':
        return False, 'yes'
    else:
        return True, 'no'

# CALL BACK FUNCTIONS FOR TABS


@app.callback(
    Output('tab-1-output', 'children'),
    [Input('tabs-styled-with-inline', 'value')]
)
def tabreturn(tab):
    if tab == 'tab1':
        return children_container1
    elif tab == 'tab2':
        return children_container2

# CALL BACK FUNCTION FOR 1ST TAB DROP DOWN (THE DEFAULT VISIBLE SHEETS IN EXCEL)
# INPUT - ENVIRONMENT NAME
# OUTPUT - DEFAULT SHEETS {'LABEL':'VALUE'}


@app.callback(
    Output('1sttabdropdowns', 'options'),
    Input('seconddropdown', 'value')
)
def firsttabdropdown(enviname):
    return [{'label': w, 'value': w.lower()} for w in opt[3][enviname.upper()]]

# INPUT - DEFAULT SHEET NAME {'LABEL':'VALUE'}
# OUTPUT - VALUE ONLY


@app.callback(
    Output('1sttabdropdowns', 'value'),
    Input('1sttabdropdowns', 'options')
)
def firstabdropdownvalue(opt1val):
    return opt1val[0]['value']


# CALL BACK FUNCTION FOR 2ND TAB DROP DOWN (THE HIDEEN SHEETS IN EXCEL)
# INPUT - RELEASE NU AND ENVIRONMENT NAME
# OUTPUT - HIDE SHEET NAMES {'LABEL':'VALUE'}
@app.callback(
    Output('2ndtabdropdowns', 'options'),
    [Input('firstdropdown', 'value'),
     Input('seconddropdown', 'value')]
)
def secondtabdropdown(firstoption, secondoption):
    return [{'label': p, 'value': p.lower()} for p in opt[4][f'{firstoption.upper()} {secondoption.upper()}']]

# INPUT - HIDE SHEET NAMES {'LABEL':'VALUE'}
# OUTPUT - VALUE ONLY


@app.callback(
    Output('2ndtabdropdowns', 'value'),
    Input('2ndtabdropdowns', 'options')
)
def secondtabdropdownvalue(optsval):
    return optsval[0]['value']

# CALL BACK FUNCTION FOR GRAPHS


@app.callback(
    Output('QaBarChart', 'figure'),
    Output('QaBarChart', 'style'),
    [Input('Dateslider', 'date'),
     Input('firstdropdown', 'value'),
     Input('seconddropdown', 'value'),
     Input('thirddropdown', 'value'),
     Input('lastdropdown', 'value'),
     Input('1sttabdropdowns', 'value')]
)
def resultreturn(dateval, fstrel, secenv, thrddayp, frthdiff, lastradio):

    # if dateval == datetime.date(datetime.now()):
    #     datevalnow = datetime.strftime(
    #         datetime.date(datetime.now()), '%m-%d-%Y')
    # else:
    #     datevalnow = datetime.strftime(
    #         datetime.date(datetime.now()), '%m-%d-%Y')
    dateval = date.fromisoformat(dateval)
    datevalnow = datetime.strftime(dateval, '%m-%d-%Y')

    if lastradio.lower() == 'sit execution summary':
        print(datevalnow, fstrel, secenv, thrddayp, frthdiff, lastradio)

        outdata = list(db.executionreports.find({'date': datevalnow, 'release': fstrel, 'env': secenv,
                                                 'daypart': thrddayp, 'difference': frthdiff, 'sheet': lastradio.lower()}, {'data': 1, '_id': 0}))
        if len(outdata) > 0:
            # print(outdata)
            dfqa = pd.DataFrame(outdata[0]['data'])
            dfqa = dfqa.iloc[:-1]
            dfqa['% Executed'] = pd.Series(
                [val * 100 for val in dfqa['% Executed']])
            dfqa['% Passed'] = pd.Series(
                [val * 100 for val in dfqa['% Passed']])
            dfqa['Test Group'] = pd.Series(
                [val.replace('\n', '<br>') for val in dfqa["Test Group"].str.wrap(23)])
            print(dfqa)
            fig = px.bar(dfqa, x='Test Group',  y=[
                         '% Executed', '% Passed'], barmode='group')
            texts = [dfqa['% Executed'].to_list(), dfqa['% Passed'].to_list()]
            for i, t in enumerate(texts):
                fig.data[i].text = t
                fig.data[i].textposition = 'outside'
            fig.update_traces(
                texttemplate='%{text:.2s}%', textposition='outside')
            fig.update_layout(height=500, width=1750, uniformtext_minsize=4,
                              uniformtext_mode='hide', yaxis=dict(tickmode="array"), bargap=0.6)
            fig.update_yaxes(range=[0, 100])
            # fig.update_layout(bargap=0.20, bargroupgap=0.00)
            fig.update_xaxes(tickangle=0, automargin=True)
            # fig.update_traces(marker_line_width=1.5)

            style = {'overflowX': 'scroll'}
            return fig, style
        else:
            style = {'display': 'none'}
            return {}, style
    else:
        style = {'display': 'none'}
        return {}, style

    # return f"date:{datevalnow}, version:{fstrel}, environment:{secenv}, time:{thrddayp}, difference:{frthdiff}, item:{lastradio}"

# CALL BACK FUNCTION FOR TABLES


@app.callback(
    Output('qatable', 'data'),
    Output('qatable', 'columns'),
    Output('qatable', 'export_format'),
    Output('qatable', 'style_table'),
    [Input('Dateslider', 'date'),
     Input('firstdropdown', 'value'),
     Input('seconddropdown', 'value'),
     Input('thirddropdown', 'value'),
     Input('lastdropdown', 'value'),
     Input('1sttabdropdowns', 'value')])
def resultdatareturn(dateval1, fstrel1, secenv1, thrddayp1, frthdiff1, lastradio1):
    # if datesdict[dateval1] == 'Today':
    #     datevalnow1 = datetime.strftime(
    #         datetime.date(datetime.now()), '%m-%d-%Y')
    # else:
    #     datevalnow1 = datetime.strftime(datetime.strptime(
    #         sevenlist[dateval1], '%m-%d-%Y'), '%m-%d-%Y')
    dateval1 = date.fromisoformat(dateval1)
    datevalnow1 = datetime.strftime(dateval1, '%m-%d-%Y')

    if lastradio1.lower() == 'sit execution status':
        print(datevalnow1, fstrel1, secenv1, thrddayp1, frthdiff1, lastradio1)

        outdata1 = list(db.executionreports.find({'date': datevalnow1, 'release': fstrel1, 'env': secenv1,
                                                  'daypart': thrddayp1, 'difference': frthdiff1, 'sheet': lastradio1.lower()}, {'data': 1, '_id': 0}))

        try:
            content = (list(outdata1))[0]['data']
        except IndexError:
            content = []
            styletable = {'display': 'none'}
            excel = ''
        else:
            styletable = {'maxHeight': '700px',
                          'overflowY': 'scroll', 'overflowX': 'scroll'}
            excel = 'xlsx'

        df = pd.DataFrame(data=content)
        cols = list(df.columns)
        columns = [{"name": i, "id": i} for i in cols]

        if len(df) > 0:
            df = df.replace('<NA>', '', regex=True)
            df = df.replace(['None'], [''], regex=True)
            df.set_index('Assignee')
        else:
            pass

        return df.to_dict('records'), columns, excel, styletable

    elif lastradio1.lower() == 'sit execution summary':
        outdata2 = list(db.executionreports.find({'date': datevalnow1, 'release': fstrel1, 'env': secenv1,
                                                  'daypart': thrddayp1, 'difference': frthdiff1, 'sheet': lastradio1.lower()}, {'data': 1, '_id': 0}))

        try:
            content = (list(outdata2))[0]['data']
        except IndexError:
            content = []
            styletable = {'display': 'none'}
            xcel = ''
        else:
            styletable = {'maxHeight': '700px',
                          'overflowY': 'scroll', 'overflowX': 'scroll'}
            xcel = 'xlsx'

        df001 = pd.DataFrame(data=content)

        cols001 = list(df001.columns)
        columns001 = [{"name": o, "id": o} for o in cols001]

        return df001.to_dict('records'), columns001, xcel, styletable


# CALL BACK FUNCTION FOR THE COUNTS TO DISPLAY
@app.callback(
    Output('olddisplay', 'children'),
    Output('newdisplay', 'children'),
    [Input('Dateslider', 'date'),
     Input('firstdropdown', 'value'),
     Input('seconddropdown', 'value'),
     Input('thirddropdown', 'value'),
     Input('lastdropdown', 'value'),
     Input('1sttabdropdowns', 'value')])
def resultdata01return(dateval2, fstrel2, secenv2, thrddayp2, frthdiff2, lastradio2):
    # if datesdict[dateval2] == 'Today':
    #     datevalnow2 = datetime.strftime(
    #         datetime.date(datetime.now()), '%m-%d-%Y')
    # else:
    #     datevalnow2 = datetime.strftime(datetime.strptime(
    #         sevenlist[dateval2], '%m-%d-%Y'), '%m-%d-%Y')
    dateval2 = date.fromisoformat(dateval2)
    datevalnow2 = datetime.strftime(dateval2, '%m-%d-%Y')

    countdata = list(db.executionreports.find({'date': datevalnow2, 'release': fstrel2, 'env': secenv2, 'daypart': thrddayp2,
                                               'difference': frthdiff2, 'sheet': lastradio2.lower()}, {'oldcount': 1, 'newcount': 1, '_id': 0}))
    if len(countdata) > 0:
        value01 = countdata[0]["oldcount"]
        value02 = countdata[0]["newcount"]
        return value01, value02
    else:
        return '00000', '00000'

# CALL BACK FUNCTION FOR THE DROP DOWNS IN 2ND TAB


@app.callback(
    Output('unhidesheet', 'data'),
    Output('unhidesheet', 'columns'),
    Output('unhidesheet', 'export_format'),
    Output('unhidesheet', 'style_table'),
    [Input('Dateslider', 'date'),
     Input('firstdropdown', 'value'),
     Input('seconddropdown', 'value'),
     Input('thirddropdown', 'value'),
     Input('lastdropdown', 'value'),
     Input('2ndtabdropdowns', 'value')])
def resultdata02return(dateval3, fstrel3, secenv3, thrddayp3, frthdiff3, raditem1):
    # if datesdict[dateval3] == 'Today':
    #     datevalnow3 = datetime.strftime(
    #         datetime.date(datetime.now()), '%m-%d-%Y')
    # else:
    #     datevalnow3 = datetime.strftime(datetime.strptime(
    #         sevenlist[dateval3], '%m-%d-%Y'), '%m-%d-%Y')
    dateval3 = date.fromisoformat(dateval3)
    datevalnow3 = datetime.strftime(dateval3, '%m-%d-%Y')

    hiddendata = list(db.executionreportshiden.find({'date': datevalnow3, 'release': fstrel3, 'env': secenv3,
                                                     'daypart': thrddayp3, 'difference': frthdiff3, 'sheet': raditem1.lower()}, {'data': 1, '_id': 0}))

    try:
        content1 = (list(hiddendata))[0]['data']
    except IndexError:
        content1 = []
        style = {'display': 'none'}
        excels = ''
    else:
        style = {'maxHeight': '700px',
                 'overflowY': 'scroll', 'overflowX': 'scroll'}
        excels = 'xlsx'

    df = pd.DataFrame(data=content1)
    cols = list(df.columns)
    columns = [{"name": i, "id": i} for i in cols]

    return df.to_dict('records'), columns, excels, style
