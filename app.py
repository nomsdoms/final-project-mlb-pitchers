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

###### Import a dataframe #######
all = pd.read_csv(filename)
recent = all[all['yearID']>1999]
exp = recent[recent['GS']>20]

###### Make unique IDs for duplicate player names, years, and teams ######
exp['yearID_string'] = exp['yearID'].astype(str)
exp['playerID'] = exp.apply(lambda x: x['playerID'][:-2], axis = 1)
exp['name_year_team'] = exp[['playerID', 'yearID_string','teamID']].apply(lambda x: '-'.join(x), axis=1)
exp.drop_duplicates(['name_year_team'], keep='last', inplace=True)

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
    html.H3('Choose a continuous variable for the Top 10 pitchers of each statistic:'),
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
# Change ascending vs descending based on statistic
    # if continuous_var == "Losses":
    #     sort_this_way = True
    # elif continuous_var == "Hits" or "Earned Runs" or "Earned Runs Average" or "Opponent Batting Average":
    #     sort_this_way = True
    # elif continuous_var == "Wins" or "Strikeouts":
    #     sort_this_way = False
    # else:
    #     sort_this_way = False
     #Create a grouped bar chart
    mydata = go.Bar(
        x=list(pitchers.sort_values(continuous_var, ascending = False).head(10)['name_year_team']),
        y=list(pitchers.sort_values(continuous_var, ascending = False).head(10)[continuous_var]),
        marker=dict(color=color1)
    )
    mylayout = go.Layout(
    title='Highest 10 {} pitched in a season from 2000 to 2018'.format(str(continuous_var)),
    xaxis = dict(title = 'Pitcher-Year-Team'), # x-axis label
    yaxis = dict(title = str(continuous_var)), # y-axis label
    )

    fig = go.Figure(data=[mydata], layout=mylayout)
    return fig

############ Deploy / Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
