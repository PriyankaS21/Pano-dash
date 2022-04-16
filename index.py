
# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

from app import app
from app import server

# from apps import jiraburndown, qareport, datahealthcheck, cumulative
from apps import qareport, datahealthcheck, cumulative

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
    "background-color": "#2a343c",
    "color": "white",
    "border-right": "1px solid #FF4D00"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("DXC Pano Dashboard"),
        html.Hr(style={"background-color": "#FF4D00"}),
        html.P("Track 11 Automation", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("QA Execution Report",
                            href="/QER", active="exact"),
                # dbc.NavLink("Jira Burndown Report",
                #             href="/JBD", active="exact"),
                dbc.NavLink("Health Check Report",
                            href="/HCR", active="exact"),
                dbc.NavLink("Cumulative Report",
                            href="/CR", active="exact"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/QER" or pathname == "/":
        return qareport.layout
        # return [
        # html.H4('QA Execution Reports', style={'textAlign':'left'}),
        # dcc.Graph(id='bargraph',
        #          figure=px.bar(df, barmode='group', x='Years',
        #          y=['Girls Kindergarten', 'Boys Kindergarten']))
        # ]
    # elif pathname == "/JBD":
    #     return jiraburndown.layout
        # return [
        # html.H4('Jira Burndown Report', style={'textAlign':'left'}),
        # dcc.Graph(id='bargraph',
        #          figure=px.bar(df, barmode='group', x='Years',
        #          y=['Girls Grade School', 'Boys Grade School']))
        # ]
    elif pathname == "/HCR":
        return datahealthcheck.layout
        # return [
        # html.H4('Health Check Report', s
        # tyle={'textAlign':'left'}),
        # dcc.Graph(id='bargraph',
        #          figure=px.bar(df, barmode='group', x='Years',
        #          y=['Girls High School', 'Boys High School']))
        # ]
    elif pathname == "/CR":
        return cumulative.layout
        # return dbc.Jumbotron(
        #     [
        #         html.H1("Under Construction", className="text-danger"),
        #         html.Hr()
        #     ]
        # )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=False, port=3000, use_reloader=True)
