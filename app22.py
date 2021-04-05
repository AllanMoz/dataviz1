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



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}
############################################################################################################################################################




'''LOADING DATA'''
st = pd.read_csv('weekly_deaths.csv' , sep = ',').fillna(0)
df = pd.read_csv('USA_diseases.csv').drop(columns = ['Unnamed: 0', 'MMWR Year','MMWR Week', 'Jurisdiction of Occurrence'])

st.loc[:,'All Cause'] = st.loc[:,'All Cause'].map(lambda x: x*1000 if x < 20 else x)
st.loc[:,'Natural Cause'] = st.loc[:,'Natural Cause'].map(lambda x: x*1000 if x < 20 else x)
st.loc[:,'Malignant neoplasms (C00-C97)'] = st.loc[:,'Malignant neoplasms (C00-C97)'].map(lambda x: x*1000 if x < 10 else x)
st.loc[:,'Diseases of heart (I00-I09,I11,I13,I20-I51)'] = st.loc[:,'Diseases of heart (I00-I09,I11,I13,I20-I51)'].map(lambda x: x*1000 if x < 10 else x)
st.loc[:,'COVID-19 (U071, Multiple Cause of Death)'] = st.loc[:,'COVID-19 (U071, Multiple Cause of Death)'].map(lambda x: x*1000 if x < 10 else x)
st.loc[:,'COVID-19 (U071, Underlying Cause of Death)'] = st.loc[:,'COVID-19 (U071, Underlying Cause of Death)'].map(lambda x: x*1000 if x < 10 else x)
##############################################################################

def top10(disease, date):
    
    dis = st.loc[:, [disease, "Week Ending Date",'State']]
    between  = dis[(dis['Week Ending Date']>=date[0]) & (dis['Week Ending Date']<=date[1])]
    sumofdeaths = between.groupby('State').sum().reset_index()
    top10withmoredeaths = sumofdeaths.sort_values(by=disease,ascending=False)[:10]
    top10withmoredeaths = top10withmoredeaths.reset_index().sort_index(ascending=False)
    
    fig= go.Figure(go.Bar(x=top10withmoredeaths[disease], y=top10withmoredeaths['State'], orientation='h'))
    
    return fig

st['Week Ending Date'] = pd.to_datetime(st['Week Ending Date'])

AL = st[st['State'] == 'Alabama']
AL = AL.sort_values(by='Week Ending Date')
AL = AL[AL['All Cause']!=0]

random_x = AL['Week Ending Date']
random_y0 = AL['All Cause']



############################################################################################################################################################


# Maybe you needed to display plot in jupyter notebook
import plotly.offline as pyo
pyo.init_notebook_mode()

# Load exmples data
df.sort_values(by = ['Week Ending Date'], inplace = True)

# Base plot
fig = go.Figure(
    layout=go.Layout(
        updatemenus=[dict(type="buttons", direction="right", x=0.3, y=1.4), ],
        xaxis=dict(range=["2014-04-01", "2021-03-13"],
                   autorange=False, tickwidth=2,
                   title_text="Time"),
        yaxis=dict(range=[0, 4000],
                   autorange=False,
                   title_text="Disease"),
        title="Diseases",
    ))

# Add traces
init = 1

fig.add_trace(
    go.Scatter(x=df['Week Ending Date'],
               y=np.log2(df['Diabetes mellitus'])[:init],
               name="Diabetes",
               visible=True,
               line=dict(color="#33CFA5"),
                  mode = 'lines'))

fig.add_trace(
    go.Scatter(x=df['Week Ending Date'][:init],
               y=np.log2(df['Influenza and pneumonia'])[:init],
               name="Influenza & Pnemonia",
               visible=True,
               line=dict(color="#bf00ff"),
              mode = 'lines'))


fig.add_trace(
    go.Scatter(x=df['Week Ending Date'][:init],
               y=np.log2(df['Symptoms, signs and abnormal clinical and laboratory findings'])[:init],
               name="Abnormal",
               visible=True,
               line=dict(color="#ff0000"),
              mode = 'lines'))


# Animation
fig.update(frames=[
    go.Frame(
        data=[
            go.Scatter(x=df['Week Ending Date'][:k], y=df['Diabetes mellitus'][:k]),
            go.Scatter(x=df['Week Ending Date'][:k], y=df['Influenza and pneumonia'][:k]),
            go.Scatter(x=df['Week Ending Date'][:k], y=df['Symptoms, signs and abnormal clinical and laboratory findings'][:k]),
        ])
    for k in range(init, len(df)+1)])

# Extra Formatting
fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=10)
fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
fig.update_layout(yaxis_tickformat='-')
fig.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")

# Buttons
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Play",
                        method="animate",
                    args=[None, {"frame": {"duration": 1}}]),
                dict(label="Diabetes",
                    method="update",
                    args=[{"visible": [False, True, False]},
                          {"showlegend": True}]),
                dict(label="Influenza & pnemonia",
                    method="update",
                    args=[{"visible": [True, False, False]},
                          {"showlegend": True}]),
                dict(label="Abnormal",
                    method="update",
                    args=[{"visible": [False, False, True]},
                          {"showlegend": True}]),
                dict(label="All",
                    method="update",
                    args=[{"visible": [True, True, True, True]},
                          {"showlegend": True}]),

            ]))])



############################################################################################################################################################

def make_choropleth(year,disease):
    dis_dict={
       'Septicemia (A40-A41)' : 'Septicemia', 
       'Malignant neoplasms (C00-C97)' : 'Malignant neoplasms',
       'Diabetes mellitus (E10-E14)' : 'Diabetes mellitus', 
       'Alzheimer disease (G30)' : 'Alzheimer',
       'Influenza and pneumonia (J09-J18)' : 'Influenza and pneumonia',
       'Chronic lower respiratory diseases (J40-J47)' : 'Chronic lower respiratory',
       'Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98)' : 'Other diseases of respiratory system',
       'Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27)' : 'Nephritis, nephrotic syndrome and nephrosis',
       'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)' : 'Symptoms, signs and abnormal clinical and laboratory findings',
       'Diseases of heart (I00-I09,I11,I13,I20-I51)' : 'Diseases of heart',
       'Cerebrovascular diseases (I60-I69)' : 'Cerebrovascular diseases',
       'COVID-19 (U071, Multiple Cause of Death)' : 'COVID-19 Multiple',
       'COVID-19 (U071, Underlying Cause of Death)' : 'COVID-19 Underlying'
    }
    
    dis_colorscale={
        'Septicemia (A40-A41)':[0,4000],
        'Malignant neoplasms (C00-C97)':[0,5000],
        'Diabetes mellitus (E10-E14)':[0,12000],
        'Alzheimer disease (G30)':[0,20000],
        'Influenza and pneumonia (J09-J18)':[0,7000],
        'Chronic lower respiratory diseases (J40-J47)':[0,14000],
        'Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98)':[0,4000],
        'Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27)':[0,5000],
        'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)':[0,5000],
        'Diseases of heart (I00-I09,I11,I13,I20-I51)':[0,44000],
        'Cerebrovascular diseases (I60-I69)':[0,19000],
        'COVID-19 (U071, Multiple Cause of Death)':[0,18000],
        'COVID-19 (U071, Underlying Cause of Death)':[0,19000]
    }
    
    choropleth_dataset = st[(st['MMWR Year']==year)]
    choropleth_dataset=choropleth_dataset.groupby('state_abv').sum().reset_index()
    
    fig = px.choropleth(choropleth_dataset, 
                        locationmode='USA-states', 
                        locations='state_abv', 
                        color='Septicemia (A40-A41)',
                        color_continuous_scale="Viridis",
                        range_color=(dis_colorscale[disease][0], dis_colorscale[disease][1]),
                        scope="usa")#.show()
   
    
    #fig_layout = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

############################################################################################################################################################
slider_year = dcc.Slider(
        id='year_slider',
        min=st['Week Ending Date'].min(),
        max=st['Week Ending Date'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
        value=st['Week Ending Date'].min(),
        step=1
    )

fig1 = top10('All Cause', ['2015-04-30', '2018-04-30'])
fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=random_x, y=random_y0,
                    mode='lines+markers',
                    name='lines+markers'))
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

year=2020
disease='Septicemia (A40-A41)'


slider_year = dcc.Slider(
        id='year_slider',
        min=st['Week Ending Date'].min(),
        max=st['Week Ending Date'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
        value=st['Week Ending Date'].min(),
        step=1
    )
#fig5 = make_choropleth(2020,'Septicemia (A40-A41)')
############################################################################################################################################################




app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Deaths by Diseases in the USA',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Different Diseases Deaths from 2014 to 2021.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    
    dcc.Tabs(
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Deaths by Disease', value='tab-1'),
        dcc.Tab(label='Deaths by State', value='tab-2'),
        dcc.Tab(label='Map', value='tab-4'),
        dcc.Tab(label='Table', value='tab-5'),
        dcc.Tab(label='Sources', value='tab-6'),
        dcc.Tab(label='Data Download', value='tab-7'),
    ]),
    
     html.Div(id='tabs-content'
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
            dcc.RadioItems(
                id='lin_log',
                options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                value=0,
                labelStyle={'display': 'inline-block'}
                ),          
            dcc.Graph(
                id='example-graph-1',
                figure = fig
                ),
            
        ])

    
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                id='example-graph-2',
                figure = fig1
                
                )
        ])
    
    elif tab == 'tab-4':
        return html.Div([
            dcc.Graph(
                id='example-graph-3',
                figure = make_choropleth(2020,'Diabetes mellitus (E10-E14)')
                ),            
        ])
    
    
    elif tab == 'tab-5':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in st.columns],
                data=st.to_dict('records'),
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
############################################################################################################################################################




if __name__ == '__main__':
    app.run_server(debug=True)