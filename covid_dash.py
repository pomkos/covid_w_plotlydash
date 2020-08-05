######################
## Import Libraries ##
######################
# to import custom functions
import pandas as pd
import dash
import dash_html_components as html # add html components

import dash_core_components as dcc # add graphs
import plotly.express as px

from dash.dependencies import Input, Output # add callbacks
import plotly.graph_objects as go # for callback function to create graph. More args available than plotly.express

import datetime as dt
####################
## Initialize App ##
####################

app = dash.Dash(__name__)
server = app.server # the Flask app

###############
## Load data ##
###############
import sqlalchemy as sq
cnx = sq.create_engine('sqlite:///covid.db')
df_state = pd.read_sql_table('covid_states',cnx, parse_dates='date')
df_state = df_state.set_index('date')

df_world = pd.read_sql_table('covid_world',cnx)
df_world['date'] = pd.to_datetime(df_world['date'])
df_world = df_world.set_index('date')

def get_options(list_states):
    '''
    Returns a dictionary of label:value, required by dropdown menu
    Label: displayed in app
    Value: exposed for other functions to use
    '''
    dict_list = []
    for i in list_states:
        dict_list.append({'label': i, 'value': i})
    return dict_list

################
## Define App ##
################
app.layout = html.Div(
    children=[
        html.Div(className='row', # row element contains all content
                 children=[
                     ### LEFT COLUMN ###
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('Historic Covid19 Cases in the United States'), # headline
                                 html.P('Pick one or more states from the dropdown below.'), # paragraph
                                 html.Div(className = 'div-for-dropdown',
                                          children=[
                                              ## Dropdown Menu for State ##
                                              dcc.Dropdown(id='stateselector', # id for callback-input
                                                           options=get_options(df_state['state'].unique()), # 'state' for callback-input
                                                           multi=True,
                                                           value=['OH','MA','NH','TX'], # choose a default state
                                                           style={'backgroundColor': '#1E1E1E'},
                                                           className='stateselector'
                                                          )
                                          ]),
                                 html.P('Dotted line represents WHO recommended target'),
                                 dcc.Markdown('''
                                 __________________
                                 '''),
                                 html.H2('Historic Covid19 Cases in the World'), # headline
                                 html.P('Pick one or more countries from the dropdown below.'), # paragraph
                                 html.Div(className = 'div-for-dropdown',
                                          children=[
                                              ## Dropdown Menu for Country ##
                                              dcc.Dropdown(id='ctryselector', # id for callback-input
                                                           options=get_options(df_world['location'].unique()),
                                                           multi=True,
                                                           value=['United States','Hungary'], # choose a default state
                                                           style={'backgroundColor': '#1E1E1E'},
                                                           className='ctryselector'
                                                          )
                                          ]),
                                 dcc.Markdown('''
                                 ## Instructions
                                 * Click and drag to zoom
                                 * Double click the graph to reset axes
                                 * Click in the legend to enable/disable that view
                                 ''')
                                ]),
                     ### RIGHT COLUMN ###
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 ## Graph 1 ##
                                 dcc.Graph(id='pos_per_case', # id for callback-output
                                           config={'displayModeBar': False}, # 'figure' for callback-output is assumed
                                           animate=True),
                                 ## Graph 2 ##
                                 dcc.Graph(id='total_pos_case',config={'displayModeBar':False},animate=True),
                                 ## Graph 0 ##
                                 dcc.Graph(id='pos_world',config={'displayModeBar':False},animate=True)
                                      ]),
                 ])
        ])

#########################
## Make it Interactive ##
#########################
# callback for pos_world graph
@app.callback(Output('pos_world','figure'),
              [Input('ctryselector','value')])
def update_ctry_pos_case(ctry_value):
    trace = []
    df_copy = df_world.copy()
    
    for c in ctry_value:
        temp_df = df_copy[df_copy['location']==c]
        trace.append(go.Scatter(
            x = temp_df.index,
            y = temp_df['new_cases_per_million'],
            mode='lines',
            opacity=0.7,
            name=c,
            textposition='bottom center'))
    traces = [trace]
    flat_trace = [val for sl in traces for val in sl]
    
    figure = {
        'data':flat_trace,
        'layout':go.Layout(
            colorway=["#EA62E3", '#FFB28F', '#B6C4E7', '#32DC62', '#FFF400', '#FFA8C5'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'b': 15},
            hovermode='x',
            autosize=True,
            title={'text': 'World Daily Cases per Million', 'font': {'color': 'white'}, 'x': 0.5},
            xaxis={
                'range': [dt.date(2020,2,1), df_copy.index.max()],
                'showgrid':False
            },
            yaxis={
                'showgrid':False
            }
        )
    }
    return figure

# callback for pos_per_case graph
@app.callback(Output('pos_per_case','figure'),
              [Input('stateselector','value')])
def update_pos_per_case(state_value):
    trace = []
    df_copy = df_state.copy()
    
    for s in state_value:
        temp_df = df_copy[df_copy['state']==s]
        trace.append(go.Scatter(
            x = temp_df.index,
            y = temp_df['pos_per_tests'],
            mode = 'lines',
            opacity = 0.7,
            name = s,
            textposition = 'bottom center'))
    traces = [trace]
    flat_trace = [val for sl in traces for val in sl]
    
    figure = {
        'data':flat_trace,
        'layout':go.Layout(
            colorway=["#EA62E3", '#FFB28F', '#B6C4E7', '#32DC62', '#FFF400', '#FFA8C5'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'b': 15},
            hovermode='x',
            autosize=True,
            title={'text': 'Daily Positive:Tests Ratio', 'font': {'color': 'white'}, 'x': 0.5},
            annotations=[
                {
                    'text':'WHO Goal',
                    'x':dt.date(2020,2,10),
                    'y':0.1
                }
            ],
            xaxis={
                'range': [dt.date(2020,2,1), df_copy.index.max()],
                'showgrid':False
            },
            yaxis={
                'range': [0,1],
                'showgrid':False
            },
            shapes=[{'type':'line',
                     'yref':'paper', 'y0':0.1, 'y1':0.1,
                     'xref':'x', 'x0':dt.date(2020,2,1), 'x1':dt.date(2020,8,5),
                     'line':{
                         'color':'#33DBD3',
                         'dash':'dot',
                         'width':0.5
                     }
                   }]
        )
    }
    return figure

# callback for total_pos_case graph
@app.callback(Output('total_pos_case','figure'),
              [Input('stateselector','value')])
def update_total_pos_case(state_value):
    trace = []
    df_copy = df_state.copy()
    for s in state_value:
        temp_df = df_copy[df_copy['state']==s]
        trace.append(go.Scatter(
            x = temp_df.index,
            y = temp_df['positive'],
            mode = 'lines',
            opacity = 0.7,
            name = s,
            textposition = 'bottom center'))
    traces = [trace]
    flat_trace = [val for sl in traces for val in sl]
    
    figure = {
        'data':flat_trace,
        'layout':go.Layout(
            colorway=["#EA62E3", '#FFB28F', '#B6C4E7', '#32DC62', '#FFF400', '#FFA8C5'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'b': 15},
            hovermode='x',
            autosize=True,
            title={'text': 'Reported Positive Cases', 'font': {'color': 'white'}, 'x': 0.5},
            xaxis={
                'range': [dt.date(2020,2,1), df_copy.index.max()],
                'showgrid':False
            },
            yaxis={
                'showgrid':False
            },
        )
    }
    return figure

#################
## Run the app ##
#################

if __name__ == '__main__':
    app.run_server(debug=False,host="0.0.0.0",port=8051)
