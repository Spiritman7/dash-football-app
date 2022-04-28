# -*- coding: utf-8 -*-

import dash
from dash import Dash, dash_table
import requests
from flask_caching import Cache
import pandas as pd
import numpy as np
import time
from dash_extensions import Lottie
import datetime as dt
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import os

API_KEY = os.getenv("API_KEY")

# Initiate app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title="Football App (Dash)")

# Set up carousels
carousel_style = {"max-height": "200px", "max-width": "200px", "margin-left": "20%"}
carousel_slides = dbc.Carousel(
    # Filter carousels by league in callback: See
    # "https://community.plotly.com/t/update-image-carousels-using-callbacks /55482/3"
    id="carousel-slides-1",
    items=[
        # Premier League
        {"key": "1", "src": "assets/images/premier_league/arsenal.png", "img_style": carousel_style},
        {"key": "2", "src": "assets/images/premier_league/aston_villa.png", "img_style": carousel_style},
        {"key": "3", "src": "assets/images/premier_league/brentford.png", "img_style": carousel_style},
        {"key": "4", "src": "assets/images/premier_league/brighton.png", "img_style": carousel_style},
        {"key": "5", "src": "assets/images/premier_league/burnley.png", "img_style": carousel_style},
        {"key": "6", "src": "assets/images/premier_league/chelsea.png", "img_style": carousel_style},
        {"key": "7", "src": "assets/images/premier_league/crystal palace.png", "img_style": carousel_style},
        {"key": "8", "src": "assets/images/premier_league/everton.png", "img_style": carousel_style},
        {"key": "9", "src": "assets/images/premier_league/leeds.png", "img_style": carousel_style},
        {"key": "10", "src": "assets/images/premier_league/leicester.png", "img_style": carousel_style},
        {"key": "11", "src": "assets/images/premier_league/liverpool.png", "img_style": carousel_style},
        {"key": "12", "src": "assets/images/premier_league/man_utd.png", "img_style": carousel_style},
        {"key": "13", "src": "assets/images/premier_league/man_city.png", "img_style": carousel_style},
        {"key": "14", "src": "assets/images/premier_league/newcastle.png", "img_style": carousel_style},
        {"key": "15", "src": "assets/images/premier_league/norwich.png", "img_style": carousel_style},
        {"key": "16", "src": "assets/images/premier_league/southampton.png", "img_style": carousel_style},
        {"key": "17", "src": "assets/images/premier_league/spurs.png", "img_style": carousel_style},
        {"key": "18", "src": "assets/images/premier_league/watford.png", "img_style": carousel_style},
        {"key": "19", "src": "assets/images/premier_league/west ham.png", "img_style": carousel_style},
        {"key": "20", "src": "assets/images/premier_league/wolves.png", "img_style": carousel_style},

        # La Liga
        {"key": "21", "src": "assets/images/la_liga/alaves.png", "img_style": carousel_style},
        {"key": "22", "src": "assets/images/la_liga/athletico_madrid.png", "img_style": carousel_style},
        {"key": "23", "src": "assets/images/la_liga/barcelona.png", "img_style": carousel_style},
        {"key": "24", "src": "assets/images/la_liga/bilbao.png", "img_style": carousel_style},
        {"key": "25", "src": "assets/images/la_liga/cadiz.png", "img_style": carousel_style},
        {"key": "26", "src": "assets/images/la_liga/celta vigo.png", "img_style": carousel_style},
        {"key": "27", "src": "assets/images/la_liga/elche.png", "img_style": carousel_style},
        {"key": "28", "src": "assets/images/la_liga/espanyol.png", "img_style": carousel_style},
        {"key": "29", "src": "assets/images/la_liga/getafe.png", "img_style": carousel_style},
        {"key": "30", "src": "assets/images/la_liga/granada.png", "img_style": carousel_style},
        {"key": "31", "src": "assets/images/la_liga/levante.png", "img_style": carousel_style},
        {"key": "32", "src": "assets/images/la_liga/mallorca.png", "img_style": carousel_style},
        {"key": "33", "src": "assets/images/la_liga/osasuna.png", "img_style": carousel_style},
        {"key": "34", "src": "assets/images/la_liga/rayo vallecano.png", "img_style": carousel_style},
        {"key": "35", "src": "assets/images/la_liga/real_betis.png", "img_style": carousel_style},
        {"key": "36", "src": "assets/images/la_liga/real_madrid.png", "img_style": carousel_style},
        {"key": "37", "src": "assets/images/la_liga/real_sociedad.png", "img_style": carousel_style},
        {"key": "38", "src": "assets/images/la_liga/sevilla.png", "img_style": carousel_style},
        {"key": "39", "src": "assets/images/la_liga/valencia.png", "img_style": carousel_style},

        # Serie A
        {"key": "41", "src": "assets/images/serie_a/ac_milan.png", "img_style": carousel_style},
        {"key": "42", "src": "assets/images/serie_a/atalanta.png", "img_style": carousel_style},
        {"key": "43", "src": "assets/images/serie_a/bologna.png", "img_style": carousel_style},
        {"key": "44", "src": "assets/images/serie_a/cagliri.png", "img_style": carousel_style},
        {"key": "45", "src": "assets/images/serie_a/empoli.png", "img_style": carousel_style},
        {"key": "46", "src": "assets/images/serie_a/fiorentina.png", "img_style": carousel_style},
        {"key": "47", "src": "assets/images/serie_a/genoa.png", "img_style": carousel_style},
        {"key": "48", "src": "assets/images/serie_a/inter_milan.png", "img_style": carousel_style},
        {"key": "49", "src": "assets/images/serie_a/juventus.png", "img_style": carousel_style},
        {"key": "50", "src": "assets/images/serie_a/lazio.png", "img_style": carousel_style},
        {"key": "51", "src": "assets/images/serie_a/napoli.png", "img_style": carousel_style},
        {"key": "52", "src": "assets/images/serie_a/roma.png", "img_style": carousel_style},
        {"key": "53", "src": "assets/images/serie_a/salernitana.png", "img_style": carousel_style},
        {"key": "54", "src": "assets/images/serie_a/sampdoria.png", "img_style": carousel_style},
        {"key": "55", "src": "assets/images/serie_a/sassuolo.png", "img_style": carousel_style},
        {"key": "56", "src": "assets/images/serie_a/spezia.png", "img_style": carousel_style},
        {"key": "57", "src": "assets/images/serie_a/torino .png", "img_style": carousel_style},
        {"key": "58", "src": "assets/images/serie_a/udinese.png", "img_style": carousel_style},
        {"key": "59", "src": "assets/images/serie_a/venezia.png", "img_style": carousel_style},
        {"key": "60", "src": "assets/images/serie_a/verona.png", "img_style": carousel_style},

        # Ligue 1
        {"key": "61", "src": "assets/images/ligue_1/angers.png", "img_style": carousel_style},
        {"key": "62", "src": "assets/images/ligue_1/bordeaux.png", "img_style": carousel_style},
        {"key": "63", "src": "assets/images/ligue_1/clermont.png", "img_style": carousel_style},
        {"key": "64", "src": "assets/images/ligue_1/estac.png", "img_style": carousel_style},
        {"key": "65", "src": "assets/images/ligue_1/lens.png", "img_style": carousel_style},
        {"key": "66", "src": "assets/images/ligue_1/lille.png", "img_style": carousel_style},
        {"key": "67", "src": "assets/images/ligue_1/lorient.png", "img_style": carousel_style},
        {"key": "68", "src": "assets/images/ligue_1/lyon.png", "img_style": carousel_style},
        {"key": "69", "src": "assets/images/ligue_1/marseille.png", "img_style": carousel_style},
        {"key": "70", "src": "assets/images/ligue_1/metz.png", "img_style": carousel_style},
        {"key": "71", "src": "assets/images/ligue_1/monaco.png", "img_style": carousel_style},
        {"key": "72", "src": "assets/images/ligue_1/montpellier.png", "img_style": carousel_style},
        {"key": "73", "src": "assets/images/ligue_1/nantes.png", "img_style": carousel_style},
        {"key": "74", "src": "assets/images/ligue_1/nice.png", "img_style": carousel_style},
        {"key": "75", "src": "assets/images/ligue_1/psg.png", "img_style": carousel_style},
        {"key": "76", "src": "assets/images/ligue_1/reims.png", "img_style": carousel_style},
        {"key": "77", "src": "assets/images/ligue_1/rennes .png", "img_style": carousel_style},
        {"key": "78", "src": "assets/images/ligue_1/saint_etienne.png", "img_style": carousel_style},
        {"key": "79", "src": "assets/images/ligue_1/stade_brestois.png", "img_style": carousel_style},
        {"key": "80", "src": "assets/images/ligue_1/strasbourg.png", "img_style": carousel_style},

        # Bundesliga 1
        {"key": "81", "src": "assets/images/bundesliga/bayern.png", "img_style": carousel_style},
        {"key": "82", "src": "assets/images/bundesliga/bayern_lev.png", "img_style": carousel_style},
        {"key": "83", "src": "assets/images/bundesliga/bielefeld.png", "img_style": carousel_style},
        {"key": "84", "src": "assets/images/bundesliga/bochum.png", "img_style": carousel_style},
        {"key": "85", "src": "assets/images/bundesliga/borussia.png", "img_style": carousel_style},
        {"key": "86", "src": "assets/images/bundesliga/borussia_mochengladbach.png", "img_style": carousel_style},
        {"key": "87", "src": "assets/images/bundesliga/fc augsburg.png", "img_style": carousel_style},
        {"key": "88", "src": "assets/images/bundesliga/frankfurt.png", "img_style": carousel_style},
        {"key": "89", "src": "assets/images/bundesliga/hertha_berlin.png", "img_style": carousel_style},
        {"key": "90", "src": "assets/images/bundesliga/hoffenheim.png", "img_style": carousel_style},
        {"key": "91", "src": "assets/images/bundesliga/koln.png", "img_style": carousel_style},
        {"key": "92", "src": "assets/images/bundesliga/mainz.png", "img_style": carousel_style},
        {"key": "93", "src": "assets/images/bundesliga/rb_leipzig.png", "img_style": carousel_style},
        {"key": "94", "src": "assets/images/bundesliga/sc_freiburg.png", "img_style": carousel_style},
        {"key": "95", "src": "assets/images/bundesliga/sgf.png", "img_style": carousel_style},
        {"key": "96", "src": "assets/images/bundesliga/union_berlin.png", "img_style": carousel_style},
        {"key": "97", "src": "assets/images/bundesliga/vfb_stuggart.png", "img_style": carousel_style},
        {"key": "98", "src": "assets/images/bundesliga/wolfsburg.png", "img_style": carousel_style},
    ],
    controls=False,
    ride="carousel",
    interval=2300,
    indicators=False,

)

# Design layout
app.layout = dbc.Container([
    dbc.Card(
        dbc.CardBody([

            # Header
            dbc.Row(
                dbc.Col([
                    html.Div(
                        html.H1("Football App")
                    )], width=4)
                , justify="center")
        ])),

    dbc.Row([
        dbc.Col([
            html.H4("Preface"),
            dcc.Markdown("""\
 Welcome to my football dashboard!
"""),
            html.Br()
        ]),

    ], justify="center"),

    dbc.Row([
        dbc.Col([
            Lottie(
                options=dict(loop=True, autoplay=True), width="25%", height="45%",
                url="https://assets9.lottiefiles.com/packages/lf20_bvxz04bd.json"
                # url="https://assets6.lottiefiles.com/packages/lf20_rwwvwgka.json"
                # See more @ "https://www.dash-extensions.com/getting-started/installation"
            ),
        ])
    ]),

    # Preface animation
    # dbc.Card(
    #     dbc.CardBody([
    #
    #     ])),
    html.Br(),
    html.Br(),

    # Row 1, Col 1
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H3("League Table Standings", className="card-title"),
                    # html.P("This card has some text content, but not much else"),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                ]),

            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Select a league:"),
                    dcc.Dropdown(
                        id="dropdown_1"
                        , options=[{"label": "Premier League", "value": "Premier League"},
                                   {"label": "Bundesliga", "value": "Bundesliga"},
                                   {"label": "La Liga", "value": "La Liga"},
                                   {"label": "Serie A", "value": "Serie A"},
                                   {"label": "Ligue 1", "value": "Ligue 1"}
                                   ]
                        , placeholder="Select a league"
                        , value="Premier League"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    carousel_slides,
                ], width=3),

                # Row 1, Col 2

                dbc.Col([
                    html.Label("League"),
                    dash_table.DataTable(
                        id="df_1",
                        page_current=0,
                        page_size=20,
                        style_header={
                            'backgroundColor': '#DADAD9',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            # 1. Premier League colour codes

                            {  # UEFA Champions League
                                'if': {
                                    'filter_query': '{Position} < 5 && {League}="Premier League"',
                                },
                                'backgroundColor': '#9CD08F',
                                'color': 'white'
                            },
                            {  # UEFA Europa League
                                'if': {
                                    'filter_query': '{Position} = 5 && {League}="Premier League"',
                                },
                                'backgroundColor': '#DC8056',
                                'color': 'white'
                            },
                            {  # UEFA Conference League
                                'if': {
                                    'filter_query': '{Position} = 6 && {League}="Premier League"',
                                },
                                'backgroundColor': '#B5A240',
                                'color': 'white'
                            },

                            {  # Relegation
                                'if': {
                                    'filter_query': '{Position} > 17 && {League}="Premier League"',
                                },
                                'backgroundColor': '#FF4136',
                                'color': 'white'
                            },

                            # 2. Bundesliga colour codes

                            {  # UEFA Champions League
                                'if': {
                                    'filter_query': '{Position} < 5 && {League}="Bundesliga"',
                                },
                                'backgroundColor': '#9CD08F',
                                'color': 'white'
                            },
                            {  # UEFA Europa League
                                'if': {
                                    'filter_query': '{Position} = 5 && {League}="Bundesliga"',
                                },
                                'backgroundColor': '#DC8056',
                                'color': 'white'
                            },
                            {  # UEFA Conference League
                                'if': {
                                    'filter_query': '{Position} = 6 && {League}="Bundesliga"',
                                },
                                'backgroundColor': '#B5A240',
                                'color': 'white'
                            },

                            {  # Relegation
                                'if': {
                                    'filter_query': '{Position} > 15 && {League}="Bundesliga"',
                                },
                                'backgroundColor': '#FF4136',
                                'color': 'white'
                            },

                            # 3. La Liga colour codes

                            {  # UEFA Champions League
                                'if': {
                                    'filter_query': '{Position} < 5 && {League}="La Liga"',
                                },
                                'backgroundColor': '#9CD08F',
                                'color': 'white'
                            },
                            {  # UEFA Europa League
                                'if': {
                                    'filter_query': '{Position} = 5 && {League}="La Liga"',
                                },
                                'backgroundColor': '#DC8056',
                                'color': 'white'
                            },
                            {  # UEFA Conference League
                                'if': {
                                    'filter_query': '{Position} = 6 && {League}="La Liga"',
                                },
                                'backgroundColor': '#B5A240',
                                'color': 'white'
                            },

                            {  # Relegation
                                'if': {
                                    'filter_query': '{Position} > 17 && {League}="La Liga"',
                                },
                                'backgroundColor': '#FF4136',
                                'color': 'white'
                            },

                            # 4. Serie A colour codes

                            {  # UEFA Champions League
                                'if': {
                                    'filter_query': '{Position} < 5 && {League}="Serie A"',
                                },
                                'backgroundColor': '#9CD08F',
                                'color': 'white'
                            },
                            {  # UEFA Europa League
                                'if': {
                                    'filter_query': '{Position} = 5 && {League}="Serie A"',
                                },
                                'backgroundColor': '#DC8056',
                                'color': 'white'
                            },
                            {  # UEFA Conference League
                                'if': {
                                    'filter_query': '{Position} = 6 && {League}="Serie A"',
                                },
                                'backgroundColor': '#B5A240',
                                'color': 'white'
                            },

                            {  # Relegation
                                'if': {
                                    'filter_query': '{Position} > 17 && {League}="Serie A"',
                                },
                                'backgroundColor': '#FF4136',
                                'color': 'white'
                            },

                            # 5. Ligue 1 colour codes

                            {  # UEFA Champions League
                                'if': {
                                    'filter_query': '{Position} < 4 && {League}="Ligue 1"',
                                },
                                'backgroundColor': '#9CD08F',
                                'color': 'white'
                            },
                            {  # UEFA Europa League
                                'if': {
                                    'filter_query': '{Position} = 4 && {League}="Ligue 1"',
                                },
                                'backgroundColor': '#DC8056',
                                'color': 'white'
                            },
                            {  # UEFA Conference League
                                'if': {
                                    'filter_query': '{Position} = 5 && {League}="Ligue 1"',
                                },
                                'backgroundColor': '#B5A240',
                                'color': 'white'
                            },

                            {  # Relegation
                                'if': {
                                    'filter_query': '{Position} > 17 && {League}="Ligue 1"',
                                },
                                'backgroundColor': '#FF4136',
                                'color': 'white'
                            },

                        ]
                    )
                ])
            ]),

        ])),
    html.Br(),
    html.Br(),
    html.Br(),

    # Row 2A, Col 1
    dbc.Card(
        dbc.CardBody([
            html.H3("Top Goal Scorers", className="card-title"),
            # html.P("This card has some text content, but not much else"),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Label("Select a league:"),
                    dcc.Dropdown(
                        id="dropdown_2"
                        , options=[{"label": "Premier League", "value": "Premier League"},
                                   {"label": "Bundesliga", "value": "Bundesliga"},
                                   {"label": "La Liga", "value": "La Liga"},
                                   {"label": "Serie A", "value": "Serie A"},
                                   {"label": "Ligue 1", "value": "Ligue 1"},
                                   {"label": "All", "value": "All"}

                                   ]
                        , placeholder="Select a league"
                        , value="Premier League"
                    )
                ], width=3),

                # Row 2A, Col 2
                dbc.Col([
                    html.Label("Top Goal Scorers"),
                    dash_table.DataTable(
                        id="df_2",
                        page_current=0,
                        page_size=10,
                        style_header={
                            'backgroundColor': '#DADAD9',
                            'fontWeight': 'bold'
                        },
                    )
                ])
            ]),
            html.Br(),
            html.Br(),
            html.Br(),

            # Row 2B
            dbc.Row([
                dcc.Graph(id='graph_for_df_2'),

            ])])),
    html.Br(),
    html.Br(),
    html.Br(),

    # Row 3A, Col 1
    dbc.Card(
        dbc.CardBody([
            html.H3("Top Assists", className="card-title"),
            # html.P("This card has some text content, but not much else"),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Label("Select a league:"),
                    dcc.Dropdown(
                        id="dropdown_3"
                        , options=[{"label": "Premier League", "value": "Premier League"},
                                   {"label": "Bundesliga", "value": "Bundesliga"},
                                   {"label": "La Liga", "value": "La Liga"},
                                   {"label": "Serie A", "value": "Serie A"},
                                   {"label": "Ligue 1", "value": "Ligue 1"},
                                   {"label": "All", "value": "All"}

                                   ]
                        , placeholder="Select a league"
                        , value="Premier League"
                    )
                ], width=3),

                # Row 3A, Col 2
                dbc.Col([
                    html.Label("Top Assists"),
                    dash_table.DataTable(
                        id="df_3",
                        page_current=0,
                        page_size=10,
                        style_header={
                            'backgroundColor': '#DADAD9',
                            'fontWeight': 'bold'
                        },
                    )
                ])
            ]),
            html.Br(),
            html.Br(),
            html.Br(),

            # Row 3B
            dbc.Row([
                dcc.Graph(id='graph_for_df_3'),
            ])
        ])),

    html.Br(),
    html.Br(),
    html.Br(),

    # Football article summarization
    dbc.Card(
        dbc.CardBody([
            Lottie(
                options=dict(loop=True, autoplay=True), width="25%",
                url="https://assets6.lottiefiles.com/packages/lf20_rwwvwgka.json"
            )

        ])),

    # Treemap
    # html.Div([
    #     dcc.Graph(id='treemap')
    # ]),

    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([

            html.Div(
                [
                    html.H4("Developments",
                            style={"margin-top": "0"}),
                    dcc.Markdown(
                        """\

 Next release should be a version that contains:
 - Total goals scored (treemap)
 - Total assists per team (treemap)
 - Total goalkeeping saves
 - Total yellow/red cards per team
 - Top dribbles 
 - Top shots on target
 - Top goal contribution (goals + assists)
 - Top scorers (every week - animated bar graph)
 - Top assists (every week - animated bar graph)
 - Most home/away goals scored + conceded 
 - Most/least clean sheets


Embedding treemap visualizations would require utilising asynchronous modules to run multiple HTTP/API requests in 
parallel, like: 
- [asyncio](https://docs.python.org/3/library/asyncio.html) 
- [aiohttp](https://github.com/aio-libs/aiohttp) 

The current synchronous method requires each API request to complete before advancing to the next request, 
which is a frustrating wait-time of over 10 mins to render the treemap. Future release will add this async feature. 


"""
                    ),
                ],
                style={
                    "width": "68%",
                    "margin-right": "0",
                    "padding": "10px",
                },
                className="development_container",
            )
        ]),

        dbc.Col([
            Lottie(
                options=dict(loop=True, autoplay=True), width="75%", height="65%",
                url="https://assets3.lottiefiles.com/packages/lf20_kt08qkuh.json"
            )

        ]),
    ])
])

cache = Cache(app.server, config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache-directory',
    'CACHE_IGNORE_ERRORS': 'True'
})
timeout = 360

# Design functional features

# Store dataframes in dcc.Store (recommended practice) - see
# "https://community.plotly.com/t/storing-a-dataframe-in-dcc-store/56230"


## Callback 1A
# Supress SettingWithCopyWarning message in console
pd.options.mode.chained_assignment = None


@app.callback(
    Output("df_1", "data"),
    Input("dropdown_1", "value"),

)
@cache.memoize(timeout=timeout)
def display_table_standing(value):
    if value is None:
        return None

    if value is not None:
        ############################################# 1. PREMIER LEAGUE ##############################################
        league_id = "39"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        df_e1 = df_e['league'].apply(pd.Series)
        df_e2 = df_e1['standings'].apply(pd.Series)
        df_e2.columns = ['data']
        df_e3 = df_e2['data'].apply(pd.Series)
        output = df_e2.explode('data').assign(Co2=lambda x:
        x['data'].str.get('rank')).reset_index(drop=True)
        d = output['data'].apply(pd.Series)
        teams = d['team'].apply(pd.Series)
        games = d['all'].apply(pd.Series)
        goals = games['goals'].apply(pd.Series)
        df = pd.DataFrame()
        df['Team'] = teams['name']
        df['MP'] = games['played']
        df['W'] = games['win']
        df['D'] = games['draw']
        df['L'] = games['lose']
        df['GF'] = goals['for']
        df['GA'] = goals['against']
        df['GD'] = d['goalsDiff']
        df['Pts'] = d['points']
        df['League'] = 'Premier League'
        df.index = np.arange(1, len(df) + 1)
        df['Position'] = df.index
        df = df[['Position', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'League']]
        # print(df.to_string(index=False))
        table_standings_df = df

        ############################################# 2. GERMAN BUNDESLIGA ##############################################
        league_id = "78"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        df_e1 = df_e['league'].apply(pd.Series)
        df_e2 = df_e1['standings'].apply(pd.Series)
        df_e2.columns = ['data']
        df_e3 = df_e2['data'].apply(pd.Series)
        output = df_e2.explode('data').assign(Co2=lambda x: x['data'].str.get('rank')).reset_index(drop=True)
        d = output['data'].apply(pd.Series)
        teams = d['team'].apply(pd.Series)
        games = d['all'].apply(pd.Series)
        goals = games['goals'].apply(pd.Series)
        df = pd.DataFrame()
        df['Team'] = teams['name']
        df['MP'] = games['played']
        df['W'] = games['win']
        df['D'] = games['draw']
        df['L'] = games['lose']
        df['GF'] = goals['for']
        df['GA'] = goals['against']
        df['GD'] = d['goalsDiff']
        df['Pts'] = d['points']
        df['League'] = 'Bundesliga'
        df.index = np.arange(1, len(df) + 1)
        df['Position'] = df.index
        df = df[['Position', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'League']]

        table_standings_df = pd.concat([table_standings_df, df])

        ####################################### 3. LA LIGA ##############################################
        league_id = "140"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        df_e1 = df_e['league'].apply(pd.Series)
        df_e2 = df_e1['standings'].apply(pd.Series)
        df_e2.columns = ['data']
        df_e3 = df_e2['data'].apply(pd.Series)
        output = df_e2.explode('data').assign(Co2=lambda x: x['data'].str.get('rank')).reset_index(drop=True)
        d = output['data'].apply(pd.Series)
        teams = d['team'].apply(pd.Series)
        games = d['all'].apply(pd.Series)
        goals = games['goals'].apply(pd.Series)
        df = pd.DataFrame()
        df['Team'] = teams['name']
        df['MP'] = games['played']
        df['W'] = games['win']
        df['D'] = games['draw']
        df['L'] = games['lose']
        df['GF'] = goals['for']
        df['GA'] = goals['against']
        df['GD'] = d['goalsDiff']
        df['Pts'] = d['points']
        df['League'] = 'La Liga'
        df.index = np.arange(1, len(df) + 1)
        df['Position'] = df.index
        df = df[['Position', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'League']]

        table_standings_df = pd.concat([table_standings_df, df])

        ####################################### 4. SERIE A ##############################################
        league_id = "135"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        df_e1 = df_e['league'].apply(pd.Series)
        df_e2 = df_e1['standings'].apply(pd.Series)
        df_e2.columns = ['data']
        df_e3 = df_e2['data'].apply(pd.Series)
        output = df_e2.explode('data').assign(Co2=lambda x: x['data'].str.get('rank')).reset_index(drop=True)
        d = output['data'].apply(pd.Series)
        teams = d['team'].apply(pd.Series)
        games = d['all'].apply(pd.Series)
        goals = games['goals'].apply(pd.Series)
        df = pd.DataFrame()
        df['Team'] = teams['name']
        df['MP'] = games['played']
        df['W'] = games['win']
        df['D'] = games['draw']
        df['L'] = games['lose']
        df['GF'] = goals['for']
        df['GA'] = goals['against']
        df['GD'] = d['goalsDiff']
        df['Pts'] = d['points']
        df['League'] = 'Serie A'
        df.index = np.arange(1, len(df) + 1)
        df['Position'] = df.index
        df = df[['Position', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'League']]

        table_standings_df = pd.concat([table_standings_df, df])

        ####################################### 5. LIGUE 1 ##############################################
        league_id = "61"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        df_e1 = df_e['league'].apply(pd.Series)
        df_e2 = df_e1['standings'].apply(pd.Series)
        df_e2.columns = ['data']
        df_e3 = df_e2['data'].apply(pd.Series)
        output = df_e2.explode('data').assign(Co2=lambda x: x['data'].str.get('rank')).reset_index(drop=True)
        d = output['data'].apply(pd.Series)
        teams = d['team'].apply(pd.Series)
        games = d['all'].apply(pd.Series)
        goals = games['goals'].apply(pd.Series)
        df = pd.DataFrame()
        df['Team'] = teams['name']
        df['MP'] = games['played']
        df['W'] = games['win']
        df['D'] = games['draw']
        df['L'] = games['lose']
        df['GF'] = goals['for']
        df['GA'] = goals['against']
        df['GD'] = d['goalsDiff']
        df['Pts'] = d['points']
        df['League'] = 'Ligue 1'
        df.index = np.arange(1, len(df) + 1)
        df['Position'] = df.index
        # df['Prospects'] = df['Position'].apply(lambda x: '⬇️'
        # if x > 17 else (
        #     '🏆' if x > 2 else ''))
        df = df[['Position', 'Team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'League']]

        table_standings_df = pd.concat([table_standings_df, df])

        df = table_standings_df
        if value == "Premier League":
            premier_league_table = df.loc[df['League'] == "Premier League"]
            premier_league_data = premier_league_table.to_dict('records')
            columns = [{"name": i, "id": i} for i in df.columns]
            return premier_league_data

        elif value == "Bundesliga":
            bundesliga_table = df.loc[df['League'] == "Bundesliga"]
            bundesliga_data = bundesliga_table.to_dict("records")
            return bundesliga_data

        elif value == "La Liga":
            la_liga_table = df.loc[df['League'] == "La Liga"]
            la_liga_data = la_liga_table.to_dict("records")
            return la_liga_data

        elif value == "Serie A":
            serie_a_table = df.loc[df['League'] == "Serie A"]
            serie_a_data = serie_a_table.to_dict("records")
            return serie_a_data

        elif value == "Ligue 1":
            ligue_1_table = df.loc[df['League'] == "Ligue 1"]
            ligue_1_data = ligue_1_table.to_dict("records")
            return ligue_1_data


## Callback 2A
@app.callback(
    Output("df_2", "data"),
    # Input('df_2', "page_current"),
    # Input('df_2', "page_size"),
    Input("dropdown_2", "value")
)
@cache.memoize(timeout=timeout)
def display_top_goal_scorers(value):
    # def display_top_goal_scorers(value, page_current, page_size):
    if value is None:
        return None
    if value is not None:

        ############################################# 1. PREMIER LEAGUE ##############################################
        league_id = "39"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Premier League'
        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]

        top_goals_df = final_df

        ######################################### 2. GERMAN BUNDESLIGA ##############################################
        league_id = "78"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Bundesliga'
        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]

        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 3. LA LIGA ##############################################
        league_id = "140"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'La Liga'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 4. SERIE A ##############################################
        league_id = "135"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e2 = goals_stats_df_e1.apply(pd.Series)
        goals_stats_df_e2.columns = ['data']
        goals_stats_df_e3 = goals_stats_df_e2['data'].apply(pd.Series)
        goals_stats_df_e4 = goals_stats_df_e3['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e4], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Serie A'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 5. LIGUE 1 ##############################################
        league_id = "61"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e2 = goals_stats_df_e1.apply(pd.Series)
        goals_stats_df_e2.columns = ['data']
        goals_stats_df_e3 = goals_stats_df_e2['data'].apply(pd.Series)
        goals_stats_df_e4 = goals_stats_df_e3['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e4], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Ligue 1'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        df = top_goals_df

        if value == "Premier League":
            premier_league_goals = df.loc[df['league'] == "Premier League"]
            premier_league_data = premier_league_goals.to_dict('records')
            columns = [{"name": i, "id": i} for i in df.columns]
            return premier_league_data

        elif value == "Bundesliga":
            bundesliga_goals = df.loc[df['league'] == "Bundesliga"]
            bundesliga_data = bundesliga_goals.to_dict("records")
            return bundesliga_data

        elif value == "La Liga":
            la_liga_goals = df.loc[df['league'] == "La Liga"]
            la_liga_data = la_liga_goals.to_dict("records")
            return la_liga_data

        elif value == "Serie A":
            serie_a_goals = df.loc[df['league'] == "Serie A"]
            serie_a_data = serie_a_goals.to_dict("records")
            return serie_a_data

        elif value == "Ligue 1":
            ligue_1_goals = df.loc[df['league'] == "Ligue 1"]
            ligue_1_data = ligue_1_goals.to_dict("records")
            return ligue_1_data

        elif value == "All":
            all_data = df.to_dict("records")
            return all_data


## Callback 2B
@app.callback(
    Output("graph_for_df_2", "figure"),
    Input("dropdown_2", "value")
)
@cache.memoize(timeout=timeout)
def update_top_goalscorers_graph(value):
    if value is not None:
        ############################################# 1. PREMIER LEAGUE ##############################################
        league_id = "39"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Premier League'
        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]

        top_goals_df = final_df

        ######################################### 2. GERMAN BUNDESLIGA ##############################################
        league_id = "78"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Bundesliga'
        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]

        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 3. LA LIGA ##############################################
        league_id = "140"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e1.columns = ['data']
        goals_stats_df_e2 = goals_stats_df_e1['data'].apply(pd.Series)
        goals_stats_df_e3 = goals_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'La Liga'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 4. SERIE A ##############################################
        league_id = "135"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e2 = goals_stats_df_e1.apply(pd.Series)
        goals_stats_df_e2.columns = ['data']
        goals_stats_df_e3 = goals_stats_df_e2['data'].apply(pd.Series)
        goals_stats_df_e4 = goals_stats_df_e3['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e4], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Serie A'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        ################################### 5. LIGUE 1 ##############################################
        league_id = "61"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_goals_stats_df_e1 = df_e['player'].apply(pd.Series)
        goals_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        goals_stats_df_e2 = goals_stats_df_e1.apply(pd.Series)
        goals_stats_df_e2.columns = ['data']
        goals_stats_df_e3 = goals_stats_df_e2['data'].apply(pd.Series)
        goals_stats_df_e4 = goals_stats_df_e3['goals'].apply(pd.Series)
        df_concat = pd.concat([player_goals_stats_df_e1, goals_stats_df_e4], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'total']]
        final_df['player'] = final_df['name']
        final_df['goals'] = final_df['total'].astype(int)
        final_df = final_df.drop(['total'], axis=1)
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'goals']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Ligue 1'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'goals', 'league']]
        top_goals_df = pd.concat([top_goals_df, final_df])

        df = top_goals_df

        if value == "Premier League":
            premier_league_goals = df.loc[df['league'] == "Premier League"]
            fig = px.bar(premier_league_goals, x='player', y='goals',
                         # hover_data=['lifeExp', 'gdpPercap'],
                         color='goals',
                         labels={'goals': 'total goals scored'}, height=550)
            return fig

        elif value == "Bundesliga":
            bundesliga_goals = df.loc[df['league'] == "Bundesliga"]
            fig = px.bar(bundesliga_goals, x='player', y='goals',
                         # hover_data=['lifeExp', 'gdpPercap'],
                         color='goals',
                         labels={'goals': 'total goals scored'}, height=550)
            return fig

        elif value == "La Liga":
            la_liga_goals = df.loc[df['league'] == "La Liga"]
            fig = px.bar(la_liga_goals, x='player', y='goals',
                         # hover_data=['lifeExp', 'gdpPercap'],
                         color='goals',
                         labels={'goals': 'total goals scored'}, height=550)
            return fig

        elif value == "Serie A":
            serie_a_goals = df.loc[df['league'] == "Serie A"]
            fig = px.bar(serie_a_goals, x='player', y='goals',
                         # hover_data=['lifeExp', 'gdpPercap'],
                         color='goals',
                         labels={'goals': 'total goals scored'}, height=550)
            return fig

        elif value == "Ligue 1":
            ligue_1_goals = df.loc[df['league'] == "Ligue 1"]
            fig = px.bar(ligue_1_goals, x='player', y='goals',
                         # hover_data=['lifeExp', 'gdpPercap'],
                         color='goals',
                         labels={'goals': 'total goals scored'}, height=550)
            return fig


## Callback 3A
@app.callback(
    Output("df_3", "data"),
    Input("dropdown_3", "value")
)
@cache.memoize(timeout=timeout)
def display_top_assists(value):
    # def display_top_assists(value, page_current, page_size):
    if value is None:
        return None
    if value is not None:
        ############################################# 1. PREMIER LEAGUE ##############################################
        league_id = "39"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
        assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        assists_stats_df_e1.columns = ['data']
        assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
        assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'assists']]
        final_df['assists'] = final_df['assists'].astype(int)
        final_df['player'] = final_df['name']
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'assists']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Premier League'
        final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]

        top_assists_df = final_df

        ######################################### 2. GERMAN BUNDESLIGA ##############################################
        league_id = "78"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
        assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        assists_stats_df_e1.columns = ['data']
        assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
        assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'assists']]
        final_df['assists'] = final_df['assists'].astype(int)
        final_df['player'] = final_df['name']
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'assists']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Bundesliga'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]

        top_assists_df = pd.concat([top_assists_df, final_df])

        ################################### 3. LA LIGA ##############################################
        league_id = "140"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
        assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        assists_stats_df_e1.columns = ['data']
        assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
        assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
        df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'assists']]
        final_df['assists'] = final_df['assists'].astype(int)
        final_df['player'] = final_df['name']
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'assists']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'La Liga'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
        top_assists_df = pd.concat([top_assists_df, final_df])

        ################################### 4. SERIE A ##############################################
        league_id = "135"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
        assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        assists_stats_df_e2 = assists_stats_df_e1.apply(pd.Series)
        assists_stats_df_e3 = assists_stats_df_e2.drop(assists_stats_df_e2.columns[1], axis=1)
        assists_stats_df_e4 = assists_stats_df_e3.apply(pd.Series)
        assists_stats_df_e4.columns = ['data']
        assists_stats_df_e5 = assists_stats_df_e4['data'].apply(pd.Series)
        assists_stats_df_e6 = assists_stats_df_e5['goals'].apply(pd.Series)
        df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e6], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'assists']]
        final_df['assists'] = final_df['assists'].astype(int)
        final_df['player'] = final_df['name']
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'assists']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Serie A'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
        top_assists_df = pd.concat([top_assists_df, final_df])

        ################################### 5. LIGUE 1 ##############################################
        league_id = "61"
        endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
        query_string = {"season": "2021", "league": league_id}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
        }
        response = requests.get(endpoint_url, headers=headers, params=query_string)
        e = response.json()['response']
        df_e = pd.DataFrame(e)
        player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
        assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
        assists_stats_df_e2 = assists_stats_df_e1.apply(pd.Series)
        assists_stats_df_e3 = assists_stats_df_e2.drop(assists_stats_df_e2.columns[1], axis=1)
        assists_stats_df_e4 = assists_stats_df_e3.apply(pd.Series)
        assists_stats_df_e4.columns = ['data']
        assists_stats_df_e5 = assists_stats_df_e4['data'].apply(pd.Series)
        assists_stats_df_e6 = assists_stats_df_e5['goals'].apply(pd.Series)
        df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e6], axis=1)
        final_df = df_concat[['name', 'age', 'nationality', 'assists']]
        final_df['assists'] = final_df['assists'].astype(int)
        final_df['player'] = final_df['name']
        final_df = final_df.drop(['name'], axis=1)
        final_df = final_df[['player', 'age', 'nationality', 'assists']]
        final_df.index = np.arange(1, len(final_df) + 1)
        final_df['position'] = final_df.index
        final_df['league'] = 'Ligue 1'

        final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
        top_assists_df = pd.concat([top_assists_df, final_df])

        df = top_assists_df

        if value == "Premier League":
            premier_league_assists = df.loc[df['league'] == "Premier League"]
            premier_league_data = premier_league_assists.to_dict('records')
            columns = [{"name": i, "id": i} for i in df.columns]
            return premier_league_data

        elif value == "Bundesliga":
            bundesliga_assists = df.loc[df['league'] == "Bundesliga"]
            bundesliga_data = bundesliga_assists.to_dict("records")
            return bundesliga_data

        elif value == "La Liga":
            la_liga_assists = df.loc[df['league'] == "La Liga"]
            la_liga_data = la_liga_assists.to_dict("records")
            return la_liga_data

        elif value == "Serie A":
            serie_a_assists = df.loc[df['league'] == "Serie A"]
            serie_a_data = serie_a_assists.to_dict("records")
            return serie_a_data

        elif value == "Ligue 1":
            ligue_1_assists = df.loc[df['league'] == "Ligue 1"]
            ligue_1_data = ligue_1_assists.to_dict("records")
            return ligue_1_data

        elif value == "All":
            all_data = df.to_dict("records")
            return all_data


## Callback 3B
@app.callback(
    Output("graph_for_df_3", "figure"),
    Input("dropdown_3", "value")
)
@cache.memoize(timeout=timeout)
def update_top_assists_graph(value):
    if value is not None:
        if value is None:
            return None
        if value is not None:
            ############################################# 1. PREMIER LEAGUE ##############################################
            league_id = "39"
            endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
            query_string = {"season": "2021", "league": league_id}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': API_KEY
            }
            response = requests.get(endpoint_url, headers=headers, params=query_string)
            e = response.json()['response']
            df_e = pd.DataFrame(e)
            player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
            assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
            assists_stats_df_e1.columns = ['data']
            assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
            assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
            df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
            final_df = df_concat[['name', 'age', 'nationality', 'assists']]
            final_df['assists'] = final_df['assists'].astype(int)
            final_df['player'] = final_df['name']
            final_df = final_df.drop(['name'], axis=1)
            final_df = final_df[['player', 'age', 'nationality', 'assists']]
            final_df.index = np.arange(1, len(final_df) + 1)
            final_df['position'] = final_df.index
            final_df['league'] = 'Premier League'
            final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]

            top_assists_df = final_df

            ######################################### 2. GERMAN BUNDESLIGA ##############################################
            league_id = "78"
            endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
            query_string = {"season": "2021", "league": league_id}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': API_KEY
            }
            response = requests.get(endpoint_url, headers=headers, params=query_string)
            e = response.json()['response']
            df_e = pd.DataFrame(e)
            player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
            assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
            assists_stats_df_e1.columns = ['data']
            assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
            assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
            df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
            final_df = df_concat[['name', 'age', 'nationality', 'assists']]
            final_df['assists'] = final_df['assists'].astype(int)
            final_df['player'] = final_df['name']
            final_df = final_df.drop(['name'], axis=1)
            final_df = final_df[['player', 'age', 'nationality', 'assists']]
            final_df.index = np.arange(1, len(final_df) + 1)
            final_df['position'] = final_df.index
            final_df['league'] = 'Bundesliga'

            final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]

            top_assists_df = pd.concat([top_assists_df, final_df])

            ################################### 3. LA LIGA ##############################################
            league_id = "140"
            endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
            query_string = {"season": "2021", "league": league_id}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': API_KEY
            }
            response = requests.get(endpoint_url, headers=headers, params=query_string)
            e = response.json()['response']
            df_e = pd.DataFrame(e)
            player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
            assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
            assists_stats_df_e1.columns = ['data']
            assists_stats_df_e2 = assists_stats_df_e1['data'].apply(pd.Series)
            assists_stats_df_e3 = assists_stats_df_e2['goals'].apply(pd.Series)
            df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e3], axis=1)
            final_df = df_concat[['name', 'age', 'nationality', 'assists']]
            final_df['assists'] = final_df['assists'].astype(int)
            final_df['player'] = final_df['name']
            final_df = final_df.drop(['name'], axis=1)
            final_df = final_df[['player', 'age', 'nationality', 'assists']]
            final_df.index = np.arange(1, len(final_df) + 1)
            final_df['position'] = final_df.index
            final_df['league'] = 'La Liga'

            final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
            top_assists_df = pd.concat([top_assists_df, final_df])

            ################################### 4. SERIE A ##############################################
            league_id = "135"
            endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
            query_string = {"season": "2021", "league": league_id}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': API_KEY
            }
            response = requests.get(endpoint_url, headers=headers, params=query_string)
            e = response.json()['response']
            df_e = pd.DataFrame(e)
            player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
            assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
            assists_stats_df_e2 = assists_stats_df_e1.apply(pd.Series)
            assists_stats_df_e3 = assists_stats_df_e2.drop(assists_stats_df_e2.columns[1], axis=1)
            assists_stats_df_e4 = assists_stats_df_e3.apply(pd.Series)
            assists_stats_df_e4.columns = ['data']
            assists_stats_df_e5 = assists_stats_df_e4['data'].apply(pd.Series)
            assists_stats_df_e6 = assists_stats_df_e5['goals'].apply(pd.Series)
            df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e6], axis=1)
            final_df = df_concat[['name', 'age', 'nationality', 'assists']]
            final_df['assists'] = final_df['assists'].astype(int)
            final_df['player'] = final_df['name']
            final_df = final_df.drop(['name'], axis=1)
            final_df = final_df[['player', 'age', 'nationality', 'assists']]
            final_df.index = np.arange(1, len(final_df) + 1)
            final_df['position'] = final_df.index
            final_df['league'] = 'Serie A'

            final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
            top_assists_df = pd.concat([top_assists_df, final_df])

            ################################### 5. LIGUE 1 ##############################################
            league_id = "61"
            endpoint_url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"
            query_string = {"season": "2021", "league": league_id}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': API_KEY
            }
            response = requests.get(endpoint_url, headers=headers, params=query_string)
            e = response.json()['response']
            df_e = pd.DataFrame(e)
            player_assists_stats_df_e1 = df_e['player'].apply(pd.Series)
            assists_stats_df_e1 = df_e['statistics'].apply(pd.Series)
            assists_stats_df_e2 = assists_stats_df_e1.apply(pd.Series)
            assists_stats_df_e3 = assists_stats_df_e2.drop(assists_stats_df_e2.columns[1], axis=1)
            assists_stats_df_e4 = assists_stats_df_e3.apply(pd.Series)
            assists_stats_df_e4.columns = ['data']
            assists_stats_df_e5 = assists_stats_df_e4['data'].apply(pd.Series)
            assists_stats_df_e6 = assists_stats_df_e5['goals'].apply(pd.Series)
            df_concat = pd.concat([player_assists_stats_df_e1, assists_stats_df_e6], axis=1)
            final_df = df_concat[['name', 'age', 'nationality', 'assists']]
            final_df['assists'] = final_df['assists'].astype(int)
            final_df['player'] = final_df['name']
            final_df = final_df.drop(['name'], axis=1)
            final_df = final_df[['player', 'age', 'nationality', 'assists']]
            final_df.index = np.arange(1, len(final_df) + 1)
            final_df['position'] = final_df.index
            final_df['league'] = 'Ligue 1'

            final_df = final_df[['position', 'player', 'age', 'nationality', 'assists', 'league']]
            top_assists_df = pd.concat([top_assists_df, final_df])

            df = top_assists_df

            if value == "Premier League":
                premier_league_assists = df.loc[df['league'] == "Premier League"]
                fig = px.bar(premier_league_assists, x='player', y='assists',
                             # hover_data=['lifeExp', 'gdpPercap'],
                             color='assists',
                             labels={'assists': 'total assists'}, height=550)
                return fig

            elif value == "Bundesliga":
                bundesliga_assists = df.loc[df['league'] == "Bundesliga"]
                fig = px.bar(bundesliga_assists, x='player', y='assists',
                             # hover_data=['lifeExp', 'gdpPercap'],
                             color='assists',
                             labels={'assists': 'total assists'}, height=550)
                return fig

            elif value == "La Liga":
                la_liga_assists = df.loc[df['league'] == "La Liga"]
                fig = px.bar(la_liga_assists, x='player', y='assists',
                             # hover_data=['lifeExp', 'gdpPercap'],
                             color='assists',
                             labels={'assists': 'total assists'}, height=550)
                return fig

            elif value == "Serie A":
                serie_a_assists = df.loc[df['league'] == "Serie A"]
                fig = px.bar(serie_a_assists, x='player', y='assists',
                             # hover_data=['lifeExp', 'gdpPercap'],
                             color='assists',
                             labels={'assists': 'total assists'}, height=550)
                return fig

            elif value == "Ligue 1":
                ligue_1_assists = df.loc[df['league'] == "Ligue 1"]
                fig = px.bar(ligue_1_assists, x='player', y='assists',
                             # hover_data=['lifeExp', 'gdpPercap'],
                             color='assists',
                             labels={'assists': 'total assists'}, height=550)
                return fig


# Host app in local environment
if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
