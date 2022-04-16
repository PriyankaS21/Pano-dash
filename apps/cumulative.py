from inspect import stack
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from app import app

# app = dash.Dash(__name__)

dframe = pd.ExcelFile('apps\\Cumulative_Weekly_Status.xlsx')


def get_totals():
    sheets = dframe.sheet_names

    relCount = {}

    for sheet in sheets[:-1]:
        df = dframe.parse(sheet_name=sheet)
        # relCount[sheet] =
        sumvalue = df[['Total', 'Executed (Cumulative)', 'Passed (Cumulative)',
                       'Failed (Cumulative)', 'Blocked (Cumulative)']].sum()

        relCount[sheet] = sumvalue.to_dict()

    return relCount


dataC = get_totals()
result = {}
for key in (dataC.keys()):
    if ('Env' in result):
        result['Env'].append(key)
    else:
        result['Env'] = [key]

    if ('Count' in result):
        result['Count'].append(dataC[key]['Total'])
    else:
        result['Count'] = [dataC[key]['Total']]

df = pd.DataFrame(data=result)

dfln = dframe.parse(sheet_name='R8 DEFECT Stat')

envrons = df['Env'].unique()

layout = html.Div(children=[
    html.Div(([
        dcc.Dropdown(
            id='environment-selector',
            options=[{'label': i, 'value': i} for i in envrons],
            value='R8 QA Stat'
        ),
    ])),
    dcc.Loading(id="loading-1", type="cube", fullscreen="true",
                style={
                    'backgroundColor': 'transparent',
                    'backdrop-filter': 'blur(1px)'
                },
                children=[
                    html.Div([
                        dcc.Graph(id='lineburnchart')
                    ]),
                    html.Div([
                        dcc.Graph(id='piechart001', hoverData={
                            'points': [{'label': 'R8 PILOT Stat'}]}),
                    ], style={"display": "inline-block", 'width': '49%'}),
                    html.Div([
                        dcc.Graph(id='piechart002')
                    ], style={"display": "inline-block", 'width': '48%'}),

                    html.Div([
                        dcc.Graph(
                            id="barGraph001"
                        )
                    ], style={'overflowX': 'scroll'}),

                    html.Br(),

                    html.Div([
                        dcc.Graph(
                            id="lineGraphDefect",
                        )
                    ], style={'overflowX': 'scroll'}),

                    html.Br(),

                    html.Div([
                        dash_table.DataTable(
                            id='cumulativetable001',
                            # filter_action="native",
                            sort_action="native",
                            sort_mode="multi",

                            style_table={
                                'overflowX': 'scroll'},
                            style_cell={'textAlign': 'center', 'font-family': 'Verdana', 'fontSize': 9,
                                        'color': 'white', 'backgroundColor': '#616D7E', 'padding': '15px 5px'},
                            style_cell_conditional=[
                                {'textAlign': 'left'}
                            ],
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(195, 195, 195)',
                                    'color': 'black',
                                }
                            ],
                            style_header={
                                # 'backgroundColor': 'rgb(230, 230, 230)',
                                'backgroundColor': 'rgb(51, 51, 77)',
                                'fontWeight': 'bold',
                                'fontSize': 12
                            }

                        )
                    ])
                ]),
])


@app.callback(
    Output('lineburnchart', 'figure'),
    [Input('environment-selector', 'value')]
)
def updateLine01(valuelineone):
    dfline = dframe.parse(sheet_name=valuelineone)
    # dfline['Target'] = 250
    dfline = dfline[['Date', 'Execution Burn Rate']]

    fig = px.line(dfline, x='Date', y='Execution Burn Rate',
                  title='Execution Burn Rate Trend')
    fig.add_shape(type='line', line_color="red", line_width=3, opacity=1,
                  x0=0, x1=1, xref="paper", y0=250, y1=250, yref="y")
    return fig


@app.callback(
    Output('piechart001', 'figure'),
    [Input('environment-selector', 'value')],
)
def updatePie01(valueone):

    fig = px.pie(df, values='Count', names='Env',
                 title='Environment Total Count',
                 hover_name=df['Env'])
    return fig


@app.callback(
    Output('piechart002', 'figure'),
    [Input('piechart001', 'hoverData'),
     Input('environment-selector', 'value')],
)
def updatePie02(hoverData, value):
    if hoverData:
        dataD = get_totals()
        mydata = dataD[hoverData['points'][0]['label']]
        mydata = {'State': list(mydata.keys()), 'Count': list(mydata.values())}
        df001 = pd.DataFrame(data=mydata)
        fig001 = px.pie(df001, values='Count', names='State',
                        title=hoverData['points'][0]['label'] + ' State Count')
        return fig001
    else:
        dataD = get_totals()
        mydata = dataD[value]
        mydata = {'State': list(mydata.keys()), 'Count': list(mydata.values())}
        df001 = pd.DataFrame(data=mydata)
        fig001 = px.pie(df001, values='Count', names='State',
                        title=hoverData['points'][0]['label'] + ' State Count')
        return fig001


@app.callback(
    Output('barGraph001', 'figure'),
    [Input('piechart001', 'hoverData'),
     Input('environment-selector', 'value')]
)
def updateBar01(hoverData, value):
    if hoverData:
        dfBar = dframe.parse(sheet_name=hoverData['points'][0]['label'])
        dfBar = dfBar[['Date', 'Executed (Cumulative)', 'Passed (Cumulative)',
                       'Failed (Cumulative)', 'Blocked (Cumulative)']]
        # figbar = px.bar(dfBar, x=['Executed (Cumulative)', 'Passed (Cumulative)',
        #                           'Failed (Cumulative)', 'Blocked (Cumulative)'],
        #                 y='Date', orientation='h', opacity=0.9, barmode='group', title=hoverData['points'][0]['label'] + ' Detail Date Count')
        figbar = px.bar(dfBar, y=['Executed (Cumulative)', 'Passed (Cumulative)',
                                  'Failed (Cumulative)', 'Blocked (Cumulative)'],
                        x='Date', orientation='v', opacity=0.9, barmode='group', title=hoverData['points'][0]['label'] + ' Detail Date Count')
        figbar.update_layout(height=500, width=1750, uniformtext_minsize=4,
                             uniformtext_mode='hide', yaxis=dict(tickmode="array"), bargap=0.6)
        figbar.update_xaxes(tickangle=0, automargin=True)
        return figbar
    else:
        dfBar = dframe.parse(sheet_name=value)
        dfBar = dfBar[['Date', 'Executed (Cumulative)', 'Passed (Cumulative)',
                       'Failed (Cumulative)', 'Blocked (Cumulative)']]
        # figbar = px.bar(dfBar, x=['Executed (Cumulative)', 'Passed (Cumulative)',
        #                           'Failed (Cumulative)', 'Blocked (Cumulative)'],
        #                 y='Date', orientation='h', opacity=0.9, barmode='group', title=hoverData['points'][0]['label'] + ' Detail Date Count')
        figbar = px.bar(dfBar, y=['Executed (Cumulative)', 'Passed (Cumulative)',
                                  'Failed (Cumulative)', 'Blocked (Cumulative)'],
                        x='Date', orientation='v', opacity=0.9, barmode='group', title=hoverData['points'][0]['label'] + ' Detail Date Count')
        figbar.update_layout(height=500, width=1750, uniformtext_minsize=4,
                             uniformtext_mode='hide', yaxis=dict(tickmode="array"), bargap=0.6)
        figbar.update_xaxes(tickangle=0, automargin=True)
        return figbar


@app.callback(
    Output('lineGraphDefect', 'figure'),
    [Input('environment-selector', 'value')]
)
def updateLastLineGraph(value):
    figlline = px.line(dfln, x='DATES',
                       y=['NEW_QA', 'NEW_PILOT', 'REOPENED', 'RESOLVED', 'CLOSED',
                          'TOTAL_RESOLVED', 'TOTAL_UNRESOLVED', 'UNRESOLVED_BAD_DUEDATE'],
                       title='Cumulative Defect Stats')
    figlline.update_layout(height=500, width=1200)
    # figlline.update_xaxes(tickangle=0, automargin=True)
    return figlline


@app.callback(
    Output('cumulativetable001', 'data'),
    Output('cumulativetable001', 'columns'),
    Output('cumulativetable001', 'export_format'),
    Output('cumulativetable001', 'style_table'),
    [Input('environment-selector', 'value')]
)
def updatetablecumu(value):
    df = dframe.parse(sheet_name=value)
    cols = list(df.columns)

    columns = [{'name': i, 'id': i} for i in cols]

    if len(df) > 0:
        excel = 'xlsx'
        style_table = {
            'overflowX': 'scroll'
        }
    else:
        excel = ''
        style_table = {'display': 'none'}

    return df.to_dict('records'), columns, excel, style_table


# if __name__ == '__main__':
#     app.run_server(debug=False, port=3000, use_reloader=True)
