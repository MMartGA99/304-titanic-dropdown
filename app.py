##USE THIS FOR THE PROJECT SUBMISSION 

######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

###### Define your variables #####
tabtitle = 'NBA Stats!'
color1="rgb(165,0,38)"
color2="rgb(49,54,149)"
color3="rgb(253,174,97)"
sourceurl = 'https://www.nba.com/stats/players'
githublink = 'https://github.com/austinlasseter/titanic-example-app'


###### Import a dataframe #######
#df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
#df['Female']=df['Sex'].map({'male':0, 'female':1})
#df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
#variables_list=['Survived', 'Female', 'Fare', 'Age']

df = pd.read_excel("assets/21-22_NBA_Stats.xlsx", sheet_name="NBA_Players")
#Drop duplicate players that play multiple positions
df.drop_duplicates(subset=['PLAYER','TEAM'], inplace=True)

#Rename columns
df.rename(columns={"MIN":"Minutes", "PTS":"Points","FGM":"Field_Goals_Made", 
                   "FGA":"Field_Goals_Attempted", "3PM":"Three_Point_Field_Goals_Made",
                   "3PA":"Three_Point_Field_Goals_Attempted", "AST":"Assists"},inplace=True)
variables_list=['Minutes', 'Points', 'Field_Goals_Made', 'Field_Goals_Attempted','Three_Point_Field_Goals_Made',
                'Three_Point_Field_Goals_Attempted','Assists']



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div(children=[
    html.Div(className= 'five columns',
             style={'width':'40%','display': 'inline-block'},
             children=[
        html.Label("Select a Bar Plot Variable:"),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in variables_list],
            value=variables_list[0]
            
    )]),    
    html.Div(className= 'five columns', 
             style={'width':'40%','display': 'inline-block'},
             children =[
        html.Label("Select a Scatter Plot Variable:"),
        dcc.Dropdown(
            id='dropdown2',
            options=[{'label': i, 'value': i} for i in variables_list],
            value=variables_list[1]
            
    )]),
       
    html.Br(),
    
    html.Div([
        html.Br(),
        dcc.Graph(id="display-value", style={'display': 'inline-block'}),
        dcc.Graph(id="graph2", style={'display': 'inline-block'})
        ]),        
        html.A('Code on Github', href=githublink),
        html.Br(),
        html.A("Data Source", href=sourceurl),
             ])



######### Interactive callbacks go here #########
##Decorator and function for for left dropdown and figure
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(continuous_var):
    
    results = df.groupby(["Conference","Position"])[continuous_var].mean().reset_index()
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results['Conference'].unique(),
        y=results[results['Position']=='Guard'][continuous_var],
        name='Guard',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results['Conference'].unique(),
        y=results[results['Position']=='Center'][continuous_var],
        name='Center',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results['Conference'].unique(),
        y=results[results['Position']=='Forward'][continuous_var],
        name='Forward',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='NBA Position Per Game Stats (21-22 Season: As of 03/17/22)',
        xaxis = dict(title = 'Conference'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig

##Decorator and function for for right dropdown and figure
@app.callback(dash.dependencies.Output('graph2', 'figure'),
              [dash.dependencies.Input('dropdown2', 'value')])
def scatter_Y_axis(dropdown2_value):
          
    trace1 = (go.Scatter(
                x=df[df['Position']=="Guard"]["Minutes"],
                y=df[df['Position']== "Guard"][dropdown2_value],
                mode='markers',
                marker={'size':13, 'color':'orange', 'opacity':0.4, 'line': {'width': 0.5, 'color': 'white'}},
                #opacity = 0.5,
                text=df['PLAYER'],
                name = "Guard"
    
    ))
    
    trace2 = (go.Scatter(
                x=df[df['Position']=="Center"]["Minutes"],
                y=df[df['Position']== "Center"][dropdown2_value],
                mode='markers',
                marker={'size':13, 'opacity':0.4, 'line': {'width': 0.5, 'color': 'white'}},
                #opacity = 0.5,
                text=df['PLAYER'],
                name = "Center"
    
    ))
    
    trace3 = (go.Scatter(
                x=df[df['Position']=="Forward"]["Minutes"],
                y=df[df['Position']== "Forward"][dropdown2_value],
                mode='markers',
                marker={'size':13, 'opacity':0.4, 'line': {'width': 0.5, 'color': 'white'}},
                #opacity = 0.5,
                text=df['PLAYER'],
                name = "Forward"
    ))
    
    
    mylayout = go.Layout(
        title='Minutes Against Variable Comparison',
        xaxis = dict(title = 'Minutes'), # x-axis label
        yaxis = dict(title = str(dropdown2_value)), # y-axis label

    )
    fig = go.Figure(data=[trace1, trace2, trace3], layout=mylayout)
    
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)