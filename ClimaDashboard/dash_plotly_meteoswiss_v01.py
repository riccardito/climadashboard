import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd

from sqlalchemy import create_engine

# Connection string
alchemyEngine = create_engine('postgresql+psycopg2://ricci:asdf1234@84.75.194.146/ricci', pool_recycle=3600)
postgreSQLConnection = alchemyEngine.connect()

# import data as df
df_tem = pd.read_sql_table("temperature", postgreSQLConnection)
df_pr = pd.read_sql_table("precipitation", postgreSQLConnection)
df_sta = pd.read_sql_table("climastations", postgreSQLConnection)

# create app_dash as app
app = dash.Dash(__name__)

# create variable for dropdown as ...
stations = df_sta['STATION_NAME'].unique()

# create layout
app.layout = html.Div(

    html.Div([
        html.H1("Clima Visualization"),
        dcc.Markdown("""
        ## Climate change in Switzerland from 1980 
        ### Filter by station
        """),

        html.Div([
            dcc.Dropdown(id='select-type',
                         options=[{'label': v, 'value': v} for v in stations],
                         multi=True,
                         value=['Adelboden', 'Engelberg'])
        ]),

        html.Div([
            html.Div([
                dcc.Markdown("""
                ## Chart 1
                """),
                dcc.Graph(id='graph1'),
            ]),

            html.Div([
                dcc.Markdown("""
                ## Chart 2
                """),
                dcc.Graph(id='graph2')
            ]),
        ]),

        # html.Div([
        #     dcc.Markdown("""
        #     ## Phenology
        #     ### Filter by plant
        #     """),
        #     dcc.Dropdown(id='select-type2',
        #                  options=[{'label': v, 'value': v} for v in gender],
        #                  multi=True,
        #                  value=['female', 'male']),
        #     dcc.Graph(id='graph3')
        # ])
    ])
)


@app.callback(Output('graph1', 'figure'),
              [Input('select-type', 'value')])
def make_figure(select_type):
    dff1 = df_tem[(df_tem['stationname'].isin(select_type))]

    fig = px.scatter(
        dff1,
        x='date',
        y='mean_temperature',
        template='plotly_dark',
        color_discrete_sequence=["red"],
        title='Temperature celsius degrees'
    )

    fig.update_layout(
        title="Temperature in celsius degrees",
        xaxis_title="Years",
        yaxis_title="mean Temperature"
    )

    return fig


@app.callback(Output('graph2', 'figure'),
              [Input('select-type', 'value')])
def make_figure2(select_type):
    dff2 = df_pr[(df_pr['stationname'].isin(select_type))]

    fig = px.scatter(
        dff2,
        x='date',
        y='precipitation_sum',
        template='plotly_dark',
        color_discrete_sequence=["blue"],
        title='Precipitation per day'
    )

    fig.update_layout(
        title="Precipitation per day",
        xaxis_title="Years",
        yaxis_title="Sum in millimeters"
    )

    return fig


# @app.callback(Output('graph3', 'figure'),
#               [Input('select-type2', 'value')])
# def make_figure3(select_type):
#     dff = df[(df['sex'].isin(select_type))]
#
#     fig = px.scatter(
#         dff,
#         x='bmi',
#         y='charges',
#         color='sex',
#         template='presentation',
#     )
#
#     return fig


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
