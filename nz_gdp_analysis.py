import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

df = pd.read_csv('gdp_nz.csv')
dates = {
    2000: 0,
    2001: 1,
    2002: 2,
    2003: 3,
    2004: 4,
    2005: 5,
    2006: 6,
    2007: 7,
    2008: 8,
    2009: 9,
    2010: 10,
    2011: 11,
    2012: 12,
    2013: 13,
    2014: 14,
    2015: 15,
    2016: 16,
    2017: 17,
    2018: 18

}
df['Number'] = df['YEARS'].map(dates)

df['YEARS'] = pd.to_datetime(df['YEARS'], format='%Y')
df = df.groupby(['Industries', 'YEARS', 'State', 'Number'], as_index=False)['SCORE'].sum()
df = df.set_index('YEARS')

df = df.groupby([pd.Grouper(freq='Y'), 'Industries', 'State', 'Number'])['SCORE'].sum().reset_index()

app.layout = html.Div([

    html.Div([

        html.Img(src="https://i.ya-webdesign.com/images/new-zealand-map-png-8.png", className="three columns",
                 style={"height": '9%',
                        'width': '9%',
                        'float': 'right',
                        'position': 'relative',
                        'margin-top': 6}),
        html.H2("Dash - New Zealand GDP Analysis 2000 to 2018", style={'font-weight': 'bold', "text-align": "center"}),

        html.Div([
            dcc.Graph(id='line_chart')
        ], className='eight columns'),

        html.Div([
            html.Br(),
            html.Label(['Choose an Industry and three Areas to Compare: '],
                       style={'font-weight': 'bold', "text-align": "center"}),

            dcc.Dropdown(id='industries',
                         options=[{'label': x, 'value': x} for x in
                                  df.sort_values('Industries')['Industries'].unique()],
                         value='Agriculture',
                         multi=False,
                         disabled=False,
                         clearable=True,
                         searchable=True,
                         placeholder='Choose an industry...',
                         className='form-dropdown',
                         style={'width': '90%'},
                         persistence='string',
                         persistence_type='memory'),

            dcc.Dropdown(id='area_one',
                         options=[{'label': x, 'value': x} for x in df.sort_values('State')['State'].unique()],
                         value='Auckland',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='session'),

            dcc.Dropdown(id='area_two',
                         options=[{'label': x, 'value': x} for x in df.sort_values('State')['State'].unique()],
                         value='Wellington',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='session'),

            dcc.Dropdown(id='area_three',
                         options=[{'label': x, 'value': x} for x in df.sort_values('State')['State'].unique()],
                         value='Northland',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='local'),

        ], className='three columns')
    ]),

    html.Div([
        html.H2("Pie chart - NZ GDP by industries", style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Graph(id='pie_chart'),
        html.Div([
            dcc.Slider(id='pie_slider', min=0, max=18, value=2,
                       marks={
                           0: 2000,
                           1: 2001,
                           2: 2002,
                           3: 2003,
                           4: 2004,
                           5: 2005,
                           6: 2006,
                           7: 2007,
                           8: 2008,
                           9: 2009,
                           10: 2010,
                           11: 2011,
                           12: 2012,
                           13: 2013,
                           14: 2014,
                           15: 2015,
                           16: 2016,
                           17: 2017,
                           18: 2018
                       })
        ], style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "85%", "margin-left": "auto",
                  "margin-right": "auto"})
    ], className="nine columns")

])


@app.callback(
    Output('line_chart', 'figure'),
    [Input('industries', 'value'),
     Input('area_one', 'value'),
     Input('area_two', 'value'),
     Input('area_three', 'value')]

)
def build_line(industry, first_state, second_state, thrid_state):
    filter_boro_df = df[df['Industries'] == industry]

    dff = filter_boro_df[(filter_boro_df['State'] == first_state) |
                         (filter_boro_df['State'] == second_state) |
                         (filter_boro_df['State'] == thrid_state)]

    fig = px.line(dff, x="YEARS", y="SCORE", color='State', height=600)
    fig.update_layout(yaxis={'title': 'GDP by areas (NZD millions)'},
                      title={'text': 'GDP in different areas in selected industry',
                             'font': {'size': 20}, 'x': 0.5, 'xanchor': 'center'})

    return fig


@app.callback(
    Output('pie_chart', 'figure'),
    [Input('pie_slider', 'value')]
)
def update_pie(selected):
    return {
        "data": [
            go.Pie(labels=df['Industries'].unique().tolist(), values=df[df['Number'] == selected]['SCORE'].tolist(),
                   marker={'colors': [df['Industries']]}, textinfo='label')],
        "layout": go.Layout(title=f"Pie Chart - GDP by industries (NZD millions)", margin={"l": 200, "r": 200},
                            legend={"x": 1, "y": 0.7})
    }


if __name__ == '__main__':
    app.run_server(debug=False)