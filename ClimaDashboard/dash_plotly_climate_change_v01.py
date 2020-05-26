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
df_aggr_tem = pd.read_sql_table("mean_temp_aggregate", postgreSQLConnection)
df_pr = pd.read_sql_table("precipitation", postgreSQLConnection)
df_aggr_pr = pd.read_sql_table("rain_aggregate_sum", postgreSQLConnection)
df_sta = pd.read_sql_table("climastations", postgreSQLConnection)
df_pheno = pd.read_sql_table("phenodata", postgreSQLConnection)

# pandas data frame
df_pheno['day_of_year']= df_pheno['obs_date'].dt.dayofyear

# create app_dash as app
app = dash.Dash(__name__)

# create variable for dropdown as ...
stations1 = df_tem['stationname'].unique()
stations2 = df_aggr_pr['station_code'].unique()
plant = df_pheno['plantname'].unique()

# create layout
app.layout = html.Div(

    html.Div([
        html.H1("Climate Change Dashboard"),

        dcc.Markdown("""
        ## Climate change in Switzerland from 1980
        """),

        html.Div([
            dcc.Markdown(""" 
            ### Filter temperature by station
            """),
            html.Div([
                dcc.Dropdown(id='select-stat-temp',
                             options=[{'label': v, 'value': v} for v in stations1],
                             multi=True,
                             value=['Adelboden']),
                dcc.Markdown("""
                ## Chart 1
                """),
                dcc.Graph(id='graph1'),
            ]),

            html.Div([
                dcc.Markdown(""" 
                ### Filter precipitation by station
                """),
                dcc.Dropdown(id='select-stat-pr',
                             options=[{'label': v, 'value': v} for v in stations2],
                             multi=True,
                             value=['ABO']),
                dcc.Markdown("""
                ## Chart 2
                """),
                dcc.Graph(id='graph2')
            ])
        ]),

        html.Div([
            dcc.Markdown("""
            ## Phenology
            ### Filter by plant
            """),
            dcc.Dropdown(id='select-plant',
                         options=[{'label': v, 'value': v} for v in plant],
                         multi=True,
                         value=['Cherry tree']),

            dcc.Markdown("""
            ## Chart 3
            """),
            dcc.Graph(id='graph3')
        ])
    ])
)


@app.callback(Output('graph1', 'figure'),
              [Input('select-stat-temp', 'value')])
def make_figure(select_type):
    dff = df_tem[(df_tem['stationname'].isin(select_type))]

    fig = px.scatter(
        dff,
        x='date',
        y='mean_temperature',
        template='plotly_dark',
        color_discrete_sequence=["red"],
        title='xyz'
    )

    fig.update_layout(
        title="Temperature in celsius degrees",
        xaxis_title="Years",
        yaxis_title="Mean Temperature"
    )

    return fig

@app.callback(Output('graph2', 'figure'),
              [Input('select-stat-pr', 'value')])
def make_figure(select_type):
    dff = df_aggr_pr[(df_aggr_pr['station_code'].isin(select_type))]

    fig = px.bar(
        dff,
        x='year',
        y='total_rain',
        template='plotly_dark',
        color_discrete_sequence=["blue"],
        title='xyz'
    )

    fig.update_layout(
        title="Annual precipitation",
        xaxis_title="Years",
        yaxis_title="Sum in millimeters"
    )

    return fig

@app.callback(Output('graph3', 'figure'),
              [Input('select-plant', 'value')])
def make_figure(select_type):
    dff = df_pheno[(df_pheno['plantname'].isin(select_type))]

    fig = px.scatter(
        dff,
        x='obs_date',
        y='day_of_year',
        color='stage',
        template='plotly_dark',
        title='xyz'
    )

    fig.update_layout(
        title="Station Adelboden",
        xaxis_title="Years",
        yaxis_title="Day of year"
    )

    return fig


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
