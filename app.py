######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

########### Define a few variables ######

tabtitle = 'MLB Pitchers'
sourceurl = 'https://github.com/chadwickbureau/baseballdatabank/'
githublink = 'https://github.com/nomsdoms/final-project-mlb-pitchers'
filename = 'Pitching.csv'
color1 = '#000089'
color2 = '#cd0001'

###### Import a dataframe #######
all = pd.read_csv(filename)

###### Make unique IDs for duplicate player names, years, and teams ######
all['yearID_string'] = all['yearID'].astype(str)
all['playerID'] = all.apply(lambda x: x['playerID'][:-2], axis = 1)
all['name_year_team'] = all[['playerID', 'yearID_string','teamID']].apply(lambda x: '-'.join(x), axis=1)
all.drop_duplicates(['name_year_team'], keep='last', inplace=True)

###### Recent Players since 2000 and started over 20 games ######
recent = all[all['yearID']>1999]
exp = recent[recent['GS']>20]

###### Shorten amount of statistics to be considered ######
pitchers = exp[['playerID', 'yearID', 'teamID', 'name_year_team', 'W', 'L', 'H', 'ER', 'SO', 'BAOpp', 'ERA']]
pitchers = pitchers.rename(columns=({'W':       'Wins',
                                     'L':       'Losses',
                                     'H':       'Hits',
                                     'ER':      'Earned Runs',
                                     'ERA':     'Earned Runs Average',
                                     'SO':      'Strikeouts',
                                     'BAOpp':   'Opponent Batting Average'
                                     }))
variables_list=['Wins','Losses', 'Hits', 'Earned Runs', 'Earned Runs Average', 'Strikeouts', 'Opponent Batting Average']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Final Project - MLB Pitchers Seasonal Stats'),
    html.H2('Assumptions -- Year: 2000-2018, Games Started > 20'),
    html.H3('Choose a statistic:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(continuous_var):
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=list(pitchers.sort_values(continuous_var, ascending = False).head(10)['name_year_team']),
        y=list(pitchers.sort_values(continuous_var, ascending = False).head(10)[continuous_var]),
        marker=dict(color=color1),
        name='Highest',
    )

    mydata2 = go.Bar(
        x=list(pitchers.sort_values(continuous_var, ascending = True).head(10)['name_year_team']),
        y=list(pitchers.sort_values(continuous_var, ascending = True).head(10)[continuous_var]),
        marker=dict(color=color2),
        name='Lowest',
    )

    mylayout = go.Layout(
    title='Highest and lowest 10 seasonal {} by a pitcher from 2000 to 2018'.format(str.lower(continuous_var)),
    xaxis = dict(title = 'Pitcher-Year-Team'), # x-axis label
    yaxis = dict(title = str(continuous_var)), # y-axis label
    )

    fig = go.Figure(data=[mydata1, mydata2], layout=mylayout)
    return fig

############ Deploy / Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
