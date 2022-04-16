import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import json
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys
import json
import pymongo
from datetime import datetime, timedelta, datetime, date
from collections import OrderedDict
from app import app
import urllib

mydatestart = datetime.strftime(
    datetime.today() - timedelta(days=7), '%Y-%m-%d')
today = datetime.strftime(datetime.today(), '%m-%d-%Y')

client = pymongo.MongoClient()
db = client.atom_daily_reports


def get_dataHealthCheck():

    datelist = []
    sevenlist = []
    n = 0
    while n < 7:
        sevendays = datetime.strftime(datetime.date(
            datetime.now()) - timedelta(days=n), '%m-%d')
        fullseven = datetime.strftime(datetime.date(
            datetime.now()) - timedelta(days=n), '%Y-%m-%d')
        datelist.append(sevendays)
        fullseven_datetimeobj = datetime.strptime(fullseven, '%Y-%m-%d')
        sevenlist.append(fullseven_datetimeobj)
        n += 1
    sevenlist.reverse()
    datelist.reverse()

    datesdict = {i: val for i, val in enumerate(datelist)}
    datesdict = OrderedDict(sorted(datesdict.items()))

    key = list(datesdict.keys())
    datelist[-1] = 'Today'

    return sevenlist, datelist, key


# CALL GET JIRA BURNDOWN FUNCTION AND GET REQUIRED VALUES FOR EXEUCTION
conv, mytotaldates, a = get_dataHealthCheck()


def getData(value, cnt, tablename):

    # Getting value from slider, and fetching the data according to date
    value = date.fromisoformat(value)
    valcont = datetime.strftime(value, '%Y-%m-%d')
    d1 = list(db.DataHealthCheck.find(
        {'date': valcont}, {'_id': 0, 'data': 1}))
    table_data = [d['data'] for d in d1]

    # check whether mongo document is empty or not, if empty return nan values
    if len(table_data) > 0:
        # GET THE TABLE
        df = table_data[0][cnt]
        df0 = pd.DataFrame(data=df)
        data = df0.to_dict('records')

        data_list = []
        for d in data:
            data_list.append(d[tablename])

        # check a particular table(for ex: "AART Status") is having data or not, if is  empty then return nan values
        if len(data_list) > 0:
            for key, value in df.items():
                dataf = pd.DataFrame.from_dict(value)
                cols = [i for i in sorted(dataf.columns)]

            col = [{"name": i, "id": i} for i in cols]
            style1 = {'padding': '10px'}
            style2 = {'color': '#FF4D00', 'margin-left': '90%'}
            return data_list, col, style1, style2
        else:
            style1 = {'display': 'none'}
            style2 = {'display': 'none'}
            return [], [], style1, style2
    else:
        style1 = {'display': 'none'}
        style2 = {'display': 'none'}
        return [], [], style1, style2


def getExcelString(data):
    dff = pd.DataFrame(data)
    excel_string = dff.to_csv(index=False, encoding='utf-8')
    excel_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(excel_string)
    return excel_string


 layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            # dcc.Slider(id='Dateslider',min=a[0],max=a[-1],marks=mytotaldates, value=a[-1]
            dcc.DatePickerSingle(id='Dateslider', min_date_allowed=date(2021, 7, 1),
                                 max_date_allowed=datetime.date(  
                datetime.now()),
                initial_visible_month=datetime.date(
                datetime.now()),
                date=datetime.date(datetime.now()), day_size=39)
        ], style={'width': '60%', 'margin-bottom': '3%', 'padding-left': '10px'}),
    ], style={'width': '100%', "border-bottom": '#FF4D00 solid', 'margin-bottom': '5%'}
    ),

    dcc.Loading(id="loading-1", type="cube", fullscreen="true", style={'backgroundColor': 'transparent', 'backdrop-filter': 'blur(2px)'},

                # Container for 1st row
                children=[

        # 1st table:- "AART Status"
        html.Div(children=[html.H4("AART Status"),
                           html.A(style={'color': '#FF4D00', 'margin-left': '90%'}, className="fas fa-download mr-2",
                                  id='download-link_at', download="AART_Status.csv", href="", target="_blank"),
                           dash_table.DataTable(
            id='aart_status',
            style_cell={'textAlign': 'center', 'minWidth': 95,
                        'maxWidth': 95, 'width': 95, },
            # defaults to 500
            fixed_rows={'headers': True, }, style_table={'height': 220, }
        )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-right': '3%', 'margin-left': '2%', }),


        # 2nd Table:- "Restriction Stats"
        html.Div(children=[
            html.Div(children=[html.H4("Restriction Stats")]),
            html.A(style={'color': '#FF4D00', 'margin-left': '88%'}, className="fas fa-download mr-2",
                   id='download-link_rs', download="Restriction_Stats.csv", href="", target="_blank"),
            dash_table.DataTable(
                id='restriction_stats',
                style_cell={'textAlign': 'center',
                            'minWidth': 95, 'maxWidth': 95, 'width': 95},
                # defaults to 500
                fixed_rows={'headers': True}, style_table={'height': 220}
            )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-right': '3%'}),

        # 3rd table:- "Policy Stats"
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[html.H4("Policy Stats")]), html.A(style={
                    'color': '#FF4D00', 'margin-left': '88%'}, className="fas fa-download mr-2", id='download-link_ps', download="Policy_Stats.csv", href="", target="_blank"),
                dash_table.DataTable(
                    id='policy_stats',
                    style_cell={'textAlign': 'center',
                                'minWidth': 95, 'maxWidth': 95, 'width': 95},
                    # defaults to 500
                    fixed_rows={'headers': True}, style_table={'height': 220}
                )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-right': '2%'})
        ]),

        # 4th table:- "Rider Stats"
        html.Div(children=[
            html.Div(children=[html.H4("Rider Stats")]), html.A(style={
                'color': '#FF4D00', 'margin-left': '88%'}, className="fas fa-download mr-2", id='download-link_riders', download="Rider_Stats.csv", href="", target="_blank"),
            dash_table.DataTable(
                id='rider_stats',
                style_cell={'textAlign': 'center', 'margin': '10px',
                            'minWidth': 95, 'maxWidth': 95, 'width': 95},
                # defaults to 500
                fixed_rows={'headers': True}, style_table={'height': 220}
            )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-right': '3%', 'margin-left': '2%', 'margin-top': '3%', 'margin-bottom': '5%'}),


        # 5th table:- "Resolving Error Stats"
        html.Div(children=[
            html.Div(children=[html.H4("Resolving Error Stats")]), html.A(style={
                'color': '#FF4D00', 'margin-left': '88%'}, className="fas fa-download mr-2", id='download-link_res', download="Resolving_Error_Stats.csv", href="", target="_blank"),
            dash_table.DataTable(
                id='resolvingError_stats',
                style_cell={'textAlign': 'center',
                            'minWidth': 95, 'maxWidth': 95, 'width': 95},
                fixed_rows={'headers': True}, style_table={'height': 220},
            )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-right': '3%', 'margin-top': '3%', 'margin-bottom': '5%'}),

        # 6th table:- "Error Trig Stats"
        html.Div(children=[
            html.Div(children=[html.H4("Error Trig Stats")]), html.A(style={
                'color': '#FF4D00', 'margin-left': '88%'}, className="fas fa-download mr-2", id='download-link_ets', download="Error_Trig_Stats.csv", href="", target="_blank"),
            dash_table.DataTable(
                id='errortrig_stats',
                style_cell={'textAlign': 'center',
                            'minWidth': 95, 'maxWidth': 95, 'width': 95},
                fixed_rows={'headers': True}, style_table={'height': 220}
            )], style={"padding": '10px', 'border': '1px solid #808080', "width": '30%', "float": 'left', 'margin-top': '3%', 'margin-bottom': '5%', 'margin-right': '2%'}),
    ])

])

# Fetch data for aart status table


@app.callback(
    Output('aart_status', 'data'),
    Output('aart_status', 'columns'),
    Output('aart_status', 'style'),
    Output('download-link_at', 'style'),
    [Input('Dateslider', 'date')])
def updateTable1(value):
    data_list, col, style1, style2 = getData(value, 0, 'AART Status')
    return data_list, col, style1, style2


# To export data from aart status table
@app.callback(
    dash.dependencies.Output('download-link_at', 'href'),
    [dash.dependencies.Input('aart_status', 'data')])
def update_download_link1(data):
    es = getExcelString(data)
    return es

# Fetch data for error stats table


@app.callback(
    Output('errortrig_stats', 'data'),
    Output('errortrig_stats', 'columns'),
    Output('errortrig_stats', 'style'),
    Output('download-link_ets', 'style'),
    [Input('Dateslider', 'date')])
def updateTable2(value):
    data_list, col, style1, style2 = getData(value, 1, 'ErrorTrig Stats')
    return data_list, col, style1, style2


# To export data from error stats table
@app.callback(
    dash.dependencies.Output('download-link_ets', 'href'),
    [dash.dependencies.Input('errortrig_stats', 'data')])
def update_download_link2(data):
    es = getExcelString(data)
    return es

# Fetch data for restriction stats table


@app.callback(
    Output('restriction_stats', 'data'),
    Output('restriction_stats', 'columns'),
    Output('restriction_stats', 'style'),
    Output('download-link_rs', 'style'),
    [Input('Dateslider', 'date')])
def updateTable3(value):
    data_list, col, style1, style2 = getData(value, 4, 'Restriction Stats')
    return data_list, col, style1, style2


# To export data from restriction stats table
@app.callback(
    dash.dependencies.Output('download-link_rs', 'href'),
    [dash.dependencies.Input('restriction_stats', 'data')])
def update_download_link3(data):
    es = getExcelString(data)
    return es

# Fetch data for policy stats table


@app.callback(
    Output('policy_stats', 'data'),
    Output('policy_stats', 'columns'),
    Output('policy_stats', 'style'),
    Output('download-link_ps', 'style'),
    [Input('Dateslider', 'date')])
def updateTable4(value):
    data_list, col, style1, style2 = getData(value, 2, 'Policy Stats')
    return data_list, col, style1, style2


# To export data from policy stats table
@app.callback(
    dash.dependencies.Output('download-link_ps', 'href'),
    [dash.dependencies.Input('policy_stats', 'data')])
def update_download_link4(data):
    es = getExcelString(data)
    return es

# Fetch data for rider stats table


@app.callback(
    Output('rider_stats', 'data'),
    Output('rider_stats', 'columns'),
    Output('rider_stats', 'style'),
    Output('download-link_riders', 'style'),
    [Input('Dateslider', 'date')])
def updateTable5(value):
    data_list, col, style1, style2 = getData(value, 5, 'Rider Stats')
    return data_list, col, style1, style2


# To export data from rider stats table
@app.callback(
    dash.dependencies.Output('download-link_riders', 'href'),
    [dash.dependencies.Input('rider_stats', 'data')])
def update_download_link5(data):
    es = getExcelString(data)
    return es

# Fetch data for resolving error stats table


@app.callback(
    Output('resolvingError_stats', 'data'),
    Output('resolvingError_stats', 'columns'),
    Output('resolvingError_stats', 'style'),
    Output('download-link_res', 'style'),
    [Input('Dateslider', 'date')])
def updateTable6(value):
    data_list, col, style1, style2 = getData(value, 3, 'Resolving Error Stats')
    return data_list, col, style1, style2

# To export data from resolving error stats table


@app.callback(
    dash.dependencies.Output('download-link_res', 'href'),
    [dash.dependencies.Input('resolvingError_stats', 'data')])
def update_download_link6(data):
    es = getExcelString(data)
    return es
