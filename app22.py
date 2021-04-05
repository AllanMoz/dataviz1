import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
from urllib.request import urlopen
############################################################################################################################################################

import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)



external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#94b3d1',
    'text': '#111111'
}
############################################################################################################################################################




'''LOADING DATA'''
st = pd.read_csv('weekly_deaths.csv' , sep = ',').fillna(0)
df = pd.read_csv('USA_DISEASES.csv').drop(columns = ['Unnamed: 0', 'MMWR Year','MMWR Week', 'Jurisdiction of Occurrence'])

##############################################################################
diseases1 = df.iloc[:, 1:-1].columns

diseases = st.iloc[:, 5:-1].columns


st['Week Ending Date'] = pd.to_datetime(st['Week Ending Date'])

############################################################################################################################################################
############################################################################################################################################################

dis_colorscale={
        'All Cause': [0, 350000],
        'Natural Cause': [0, 250000],
        'Septicemia':[0,4000],
        'Malignant neoplasms':[0,62000],
        'Diabetes mellitus':[0,12000],
        'Alzheimer disease':[0,20000],
        'Influenza and pneumonia':[0,7000],
        'Chronic lower respiratory diseases':[0,14000],
        'Other diseases of respiratory system':[0,4000],
        'Nephritis, nephrotic syndrome and nephrosis':[0,5000],
        'Symptoms, signs and abnormal clinical and laboratory findings':[0,5000],
        'Diseases of heart':[0,44000],
        'Cerebrovascular diseases':[0,19000],
        'Multiple Cause of Death + COVID-19':[0,5000],
        'COVID-19 as Underlying Cause of Death':[0,3000]
    }
############################################################################################################################################################


tab_style = {
    #'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold',
    'box-shadow': '2px' '2px' '2px' '#cf9696',
    'backgroundColor': '#dce6ef',
    'border-radius': '7px'
}

tab_selected_style = {
    'borderTop': '1px solid #cf9696',
    'borderBottom': '1px solid #cf9696',
    'backgroundColor': '#cf9696',
    'color': 'black',
    'padding': '6px',
    'border-radius': '7px'
}



app.layout = html.Div(style={'backgroundColor': '#94b3d1'}, children=[
    
    html.H1(
        children='Deaths by Diseases in the USA',
        className = 'h1'
    ),

    html.Div(children='Different Diseases Deaths from 2014 to 2021', style={
        'textAlign': 'center',
        'font-size': '15px',
        'color': colors['text']
    }),
    
    
    dcc.Tabs(className = 'tabss',
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Deaths by Disease', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Deaths by State', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Map', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Table', value='tab-5', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sources', value='tab-6', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Data Download', value='tab-7', style=tab_style, selected_style=tab_selected_style),
    ]),
    
     html.Div(style = {'width': '70%', 'height': '50%', 
                      'margin-right': '15%', 'margin-left': '15%'},
                         id='tabs-content'
    ),
    

])
############################################################################################################################################################


@app.callback(
    Output('tabs-content', 'children'),
     Input('tabs', 'value'),
     
     )
############################################################################################################################################################




def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Dropdown(
                id='line_option',
                options=[{'label': i, 'value': i} for i in diseases1],
                value=['All Cause'],
                style = {'backgroundColor': '#dce6ef',
                         'color': 'black',
                         },
                multi = True
                ),
            dcc.RadioItems(
                id = 'timely',
                options = [dict(label = 'Yearly', value = 1), 
                           dict(label = 'Monthly', value = 0)],
                value = 0,
                style = {
                         'margin-left': '2%'}
                ),
            dcc.RadioItems(
                id = 'aggregates',
                options = [dict(label = 'Mean', value = 0), 
                           dict(label = 'Sum', value = 1)],
                value = 0,
                style = {
                         'margin-left': '2%'}
                ),
            dcc.Graph(
                id='lineplot',
                )],
            className = 'box'
            )
       



    
    elif tab == 'tab-2':
        return html.Div([
            dcc.Dropdown(
                id='disease1',
                options=[{'label': i, 'value': i} for i in diseases],
                value='All Cause',
                #className = 'box'
                style = {'backgroundColor': '#dce6ef',
                         'color': 'black'},
                ),
            dcc.Graph(id = 'top10',
                      className = 'box'),
    
            dcc.RangeSlider(
                id = 'range',
                min = 2014,
                max = 2021,
                value = [2015, 2017],
                marks={str(i): '{}'.format(str(i)) for i in
                       [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]})
                ],
            #html.Br(),
            className = 'box',
    
                )
        
    elif tab == 'tab-4':
        return html.Div([
            dcc.Dropdown(
                id='disease',
                options=[{'label': i, 'value': i} for i in diseases],
                value='All Cause',
               # className = 'box'
               style = {'backgroundColor': '#dce6ef',
                         'color': 'black'},
                ),
            dcc.Graph(id = 'choropleth',
                      className = 'box'),
            
            dcc.Slider(
                id = 'year',
                min = 2014,
                max = 2021,
                value = 2017,
                marks={str(i): '{}'.format(str(i)) for i in
                       [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
                
                
                )
            ],
            className = 'box',)

    elif tab == 'tab-5':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in st.columns],
                data=st.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
        # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
    }
                )
        ])
    
    
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 7')         
        ])
    
    
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Tab content 7')
        ])
    

@app.callback(
     Output('lineplot', 'figure'),
    [Input('line_option', 'value'),
     Input('timely', 'value'),
     Input('aggregates', 'value')])
    
      
def lineplot(disease, time, agg):
    gg = pd.read_csv('USA_DISEASES.csv').drop(columns = ['Unnamed: 0','MMWR Week','MMWR Year','Jurisdiction of Occurrence'])
    gg['Week Ending Date'] = pd.to_datetime(gg['Week Ending Date'])
    gg = gg.set_index('Week Ending Date')
    df1 = gg.groupby(pd.Grouper(freq="M")).mean().reset_index()
    data_line = []
    colory = ['rgb(0, 147, 146)','rgb(69, 176, 175)','rgb(114, 170, 161)','rgb(130, 181, 135)',
                  'rgb(177, 199, 179)','rgb(207, 250, 211)', 'rgb(241, 234, 200)','rgb(250, 235, 162)',
                      'rgb(255, 226, 87)','rgb(229, 185, 173)','rgb(250, 167, 145)','rgb(217, 137, 148)',
                          'rgb(208, 88, 126)']

    for i in range(len(disease)):
        if time == 0:
            if agg == 0:
                df1 = gg.groupby(pd.Grouper(freq="M")).mean().reset_index()
            elif agg == 1:
                df1 = gg.groupby(pd.Grouper(freq="M")).sum().reset_index()
        elif time == 1:
            if agg == 0:
                df1 = gg.groupby(pd.Grouper(freq="Y")).mean().reset_index()
            elif agg == 1:
                df1 = gg.groupby(pd.Grouper(freq="Y")).sum().reset_index()
        data_line.append(dict(type='scatter',x=df1['Week Ending Date'], y=df1[disease[i]], 
                              mode='lines',line=dict(color = colory[i]), name = disease[i],
                              ))
        figr = go.Figure(data=data_line)
        figr.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           autosize=False,
                            width=1300,
                            height=650,
                            margin=dict(
                                l=50,
                                r=50,
                                b=100,
                                t=100,
                                pad=4))
    
    return figr
 
@app.callback(
     Output('top10', 'figure'),
    [Input('disease1', 'value'),
     Input('range', 'value')])

   
def top10(disease, date):
    
    dis = st.loc[:, [disease, "MMWR Year",'State']]
    between  = dis[(dis['MMWR Year']>=date[0]) & (dis['MMWR Year']<=date[1])]
    sumofdeaths = between.groupby('State').sum().reset_index()
    top10withmoredeaths = sumofdeaths.sort_values(by=disease,ascending=False)[:10]
    top10withmoredeaths = top10withmoredeaths.reset_index().sort_index(ascending=False)
    
    fig= px.bar(top10withmoredeaths, x=disease, y = 'State', 
                          orientation='h', color = disease, 
                          color_continuous_scale= 'Tealrose',
                          range_color = (dis_colorscale[disease][0], dis_colorscale[disease][1]))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           autosize=False,
                            width=1200,
                            height=650,
                            margin=dict(
                                l=50,
                                r=50,
                                b=100,
                                t=100,
                                pad=4))
    
    return fig

@app.callback(
    Output('choropleth', 'figure'),
    [Input('disease', 'value'),
     Input('year', 'value')])

def display_choropleth(disease, year):
    
    

    choropleth_dataset = st[(st['MMWR Year']==year)]
    choropleth_dataset=choropleth_dataset.groupby('state_abv').sum().reset_index()
    fig = px.choropleth(
        choropleth_dataset,
        color = disease,
        locationmode="USA-states",
        locations = 'state_abv',
        range_color = (dis_colorscale[disease][0], dis_colorscale[disease][1]),
        color_continuous_scale="Tealrose",
        scope = 'usa')
    
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                    margin=dict(l=0, r=0, t=0, b=0),
                            autosize=False,
                            width=1200,
                            height=650,
        
                           )
    
    return fig
############################################################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)
    
