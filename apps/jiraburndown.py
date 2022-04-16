import pandas as pd
import numpy as np
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

# SAMPLE CONTENT WITH CALL BACK DECORATOR
# GRAPH PREPARED WITH PLOTLY EXPRESS

mydatestart = datetime.strftime(
    datetime.today() - timedelta(days=7), '%m-%d-%Y')
mydatestart = '03-26-2021'
today = datetime.strftime(datetime.today(), '%m-%d-%Y')

client = pymongo.MongoClient()
db = client.qareports


def get_jiraburndown():
    global dataframeJBD
    # FETCH FROM MONGO DB (FROM CURRENT DATE TO LAST 7 DAYS)
    das = list(db.jiraburndownreport.find(
        {'date': {'$gte': '03-08-2021'}}, {'date': 1, '_id': 0}))

    findcolumns = list(db.jiraburndownreport.find(
        {'date': {'$gte': '03-08-2021'}}, {'report': 1, '_id': 0}))
    cols = [dval.keys() for dval in [d['report'] for d in findcolumns][0]][0]

    dates = [d['date'] for d in das]

    # CONVERTING DATE FORMAT FROM MONTH-DATE-YEAR to MONTH-DATE
    conv = [datetime.strptime(d, "%m-%d-%Y").date() for d in dates]

    dates = [datetime.strftime(c, "%m-%d") for c in conv]
    dates[-1] = 'Today'

    # CREATING AS DICTIONARY FOR SLIDER - TO USE IN MARKS
    mytotaldates = {i: x for i, x in enumerate(dates)}
    mytotaldates = OrderedDict(sorted(mytotaldates.items()))

    # USING KEYS TO SELECTION MIN, MAX AND VALUES
    ja = (list(mytotaldates.keys()))

    dataframeJBD = 5
    return conv, mytotaldates, ja, cols


# CALL GET JIRA BURNDOWN FUNCTION AND GET REQUIRED VALUES FOR EXEUCTION
conv, mytotaldates, a, jiracols = get_jiraburndown()


layout = html.Div(children=[

    # html.Div(children=[html.H1('Panorama Reporting Dashboard')], style={'text-align':'center'}),

    html.Div(children=[html.H5('JIRA Burndown Report')],
             style={'text-align': 'center'}),

    html.Br(),

    html.Div(children=[
        dcc.Slider(id='Dateslider', min=a[0], max=a[-1], marks=mytotaldates, value=a[-1]
                   )], style={'width': '50%', 'margin-left': '25%'}),

    html.Hr(style={"background-color": "#808080"}),

    dcc.Loading(id="loading", type="cube", fullscreen="true", style={'backgroundColor': 'transparent', 'backdrop-filter': 'blur(px)'},
                children=[
        html.Br(),

        html.Div(children=[
            dash_table.DataTable(
                id='JiraBurnDown',
                export_format="xlsx",
                style_as_list_view=True,
                export_headers='display',
                # sort_action="native",
                # sort_mode="multi",
                style_cell={
                    'textAlign': 'center',
                    'font-family': 'Verdana',
                    'fontSize': 13,
                    'color': 'white',
                    'backgroundColor': '#616D7E',
                    'padding': '15px 5px'},
                style_header={
                    'backgroundColor': 'rgb(51, 51, 77)'
                },
                style_data_conditional=[{
                    'if': {
                        'column_id': 'RTotal',
                    },
                    'backgroundColor': 'rgb(51, 51, 77)',
                    'color': 'white',
                },
                    {
                    'if': {
                        'row_index': dataframeJBD,
                    },
                    'backgroundColor': 'rgb(51, 51, 77)',
                    'color': 'white',
                }]
            )
        ]),
        # html.Div(children=[
        #     dash_table.DataTable(
        #         id='JiraBurnDown', columns = [{"name":i, "id":i} for i in jiracols],style_cell={'textAlign': 'left'},
        #     )], style={"padding":'10px', 'border': '1px solid #808080'}),

        html.Br(),

        html.Div(children=[
            dcc.Graph(id="JiraLineChart")
        ], style={'overflowX': 'scroll'})
    ])
])


@app.callback(
    Output('JiraBurnDown', 'data'),
    Output('JiraBurnDown', 'columns'),
    [Input('Dateslider', 'value')])
def rangerselection(val):
    valcont = datetime.strftime(conv[val], '%m-%d-%Y')
    # return f'Contains:{valcont}'
    data = list(db.jiraburndownreport.find(
        {'date': valcont}, {'_id': 0, 'report': 1}))
    jiracols = [dval.keys() for dval in [d['report'] for d in data][0]][0]
    columns = [{"name": i, "id": i} for i in jiracols]
    df = pd.DataFrame(data=data[0]['report'])
    dataframeJBD = int(len(df) - 1)
    return df.to_dict('records'), columns


@app.callback(
    Output('JiraLineChart', 'figure'),
    [Input('Dateslider', 'value')])
def updategraph(mydateval):
    datevalue = datetime.strftime(conv[mydateval], '%m-%d-%Y')
    data = list(db.jiraburndownreport.find(
        {'date': datevalue}, {'_id': 0, 'report': 1}))
    df = pd.DataFrame(data=data[0]['report'])
    df = df.iloc[:-1]

    fig = px.line(df, x='Due_Date', y=list(df.columns)[1:-1])
    fig.update_layout(height=500, width=1500)
    return fig


# if __name__ == '__main__':
#     app.run_server(debug=False, use_reloader=True)
