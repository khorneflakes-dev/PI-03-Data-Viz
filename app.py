from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
  
# SQLAlchemy connectable
engine = create_engine('sqlite:///data_viz.db').connect()
  
# table named 'contacts' will be returned as a dataframe.
sqlite_connection = engine.connect()
df = pd.read_sql_table('accidentes', engine)
sqlite_connection.close()

df['fallecidos'] = df['cantidad_de_fallecidos'] + df['fallecidos_en_tierra']
df['decada'] = df['anio'].apply(lambda x: x - (x%10))
decada = df['decada'].drop_duplicates().tolist()
decada.sort(reverse=True)
fallecidos = df['anio'].drop_duplicates().tolist()
fallecidos.sort(reverse=True)

aux = df.groupby(['decada'], as_index=False).agg({'fecha':'count'})
aux2 = df.groupby(['decada'], as_index=False).agg({'total_a_bordo':'sum'})


all_options = {
    'Decades': decada,
    'Years': fallecidos
}

app = Dash(__name__)

app.title = 'ICAO Report'
server = app.server

app.layout = html.Div([
    
    html.Div([
        
        html.Div([
            
            html.Img(src='./assets/logo.png', className='logo1'),
            html.P('Air Accidents in the 20th Century', className='title')
                        
        ], className='left-side'),
        
        html.Div([
            
            html.Img(src='./assets/logo2.png', className='logo2')
            
        ], className = 'right-side')
        
    ], className = 'navbar'),
    
    html.Div([
        
        html.Div([
            dcc.RadioItems(id='aux', value='')
        ], className='aux'),
        
        html.Div([
            
            dcc.Graph(id='anios', figure={})
            
        ], className='anios-graph')
        
    ], className='row1'),
    
    html.Div([
    
    
        html.Div([

            html.P('You can filter by:', className = 'descriptor'),
            dcc.RadioItems(
                id='countries-dropdown',
                options=[{'label': html.Div([k], className='option'), 'value': k} for k in all_options.keys()],
                value='Decades', className='radio-items'
            ),
            dcc.Dropdown(id='value-dropdown', className='dropdown')

        ], className='row2-column1'),
        
        html.Div([
        ], className='row2-column2'),
        
        html.P(['Report of the Air Accidents that occurred in the 20th Century, we explore the amount of accidents and their consequences in human victims'
        ],className = 'row2-column3')
    
    ], className='row2'),
    
    html.Div([
        html.Div([
            html.P(id='anio', className='anio')
        ], className='row3-column1'),
        
        html.Div([
            html.P('Crashes', className='subtitle'),
            html.P(id='number-crashes', className='number-crashes')

        ], className='row3-column2'),
        
        html.Div([
            html.P('Total Deaths', className='subtitle'),
            html.P(id='number-deaths', className='number-deaths')
        ], className='row3-column3'),
        
        html.Div([
            html.P('Total on Board', className='subtitle'),
            html.P(id='total-on-board', className='total-on-board')
        ], className='row3-column4'),
        
        # html.Div([

        # ], className='row3-column5'),
    ], className='row3'),
    
        
    html.Div([
        html.Div([
            dcc.Graph(id='continents', figure={}, className='continentes')
        ], className='row5-column1'),

        html.Div([
            
            dcc.Graph(id='months', figure={}, className='pie')
        ], className='row5-column2'),

        dcc.Slider(10, 144, 1, value=30, marks=None, tooltip={"placement": "bottom", "always_visible": True},id='slider', className='slider'),
    ], className='row5'),
    
    html.P('Country Air Accidents', className='subtitle-country'),
    
    html.Div([
        dcc.Graph(id='map', figure={}, className='map')
    ], className='row4'),

    html.Div([

        html.P('About me', className='about-me-title'),

        html.Div([

            html.Div([

                html.A(
                    href="https://github.com/khorneflakes-dev/PI-03-Data-Viz",
                    target="_blank",
                    children=[
                        html.Img(
                            alt="source code",
                            src="assets/github-logo.png",
                        )
                    ], className='github-logo'
                ),

            ], className = 'about-icon-1'),
            
            html.Div([

                html.A(
                    href="https://www.linkedin.com/in/khorneflakes/",
                    target="_blank",
                    children=[
                        html.Img(
                            alt="linkedin",
                            src="assets/linkedin-logo.png",
                        )
                    ], className='linkedin-logo'
                ),
            ], className = 'about-icon-2')

        ], className='about-icons')

    ], className='about-me')
    
], className = 'main-container')


@app.callback(
    Output('anios', component_property='figure'),
    [Input('aux', component_property='value')]
)
def anios_graph(value):
    
    agrupado_decadas = df.groupby(['decada'], as_index=False).agg({'fallecidos': 'sum'})

    colors = ['#E5B028']*len(agrupado_decadas)
      
    data_graph = [go.Bar(
            x = agrupado_decadas['decada'],
            y = agrupado_decadas['fallecidos'],
            orientation='v',
            marker_color=colors,
            
            )]
    layout = go.Layout(
    margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=100, #top margin
        ))
    fig = go.Figure(data=data_graph, layout=layout)
    fig.update_layout({
        'plot_bgcolor': 'rgba(1, 1, 1, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis_title': '<b>Decades</b>',
        'yaxis_title': 'Number  of  deaths',
        'font_family': 'Lato',
        'font_color': 'white',
        'title_text': 'Deaths  per  Decade',
        'title_font_size': 30,
        'title_xanchor': 'center',
        'title_yanchor': 'top',
        'title_x': 0.5,
        'title_y': 0.9,
        })
    fig.update_xaxes(tickfont_size=20, title_font={'size': 20})
    fig.update_yaxes(tickfont_size=20, title_font={'size': 20})
    fig.update_traces(width=3)
    fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=1900,
                dtick=10
            )
        )

    return fig

@app.callback(
    Output('value-dropdown', 'value'),
    [Input('value-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('value-dropdown', 'options'),
    [Input('countries-dropdown', 'value')]
)
def set_cities_options(selected):
    return [{'label': i, 'value': i} for i in all_options[selected]]

@app.callback(
    Output('anio', component_property='children'),
    [Input('value-dropdown', component_property='value')]
)
def anio(value):
    return value

@app.callback(
    Output('number-deaths', 'children'),
    [Input('value-dropdown', 'value')],
    [Input('countries-dropdown', 'value')]
)
def number_deaths(value, value2):
    
    if value2 == 'Decades':
        muertos = df['cantidad_de_fallecidos'][df['decada']==value].sum() + df['fallecidos_en_tierra'][df['decada']==value].sum()
        return "{:,}".format(muertos)
    else:
        muertos = df['cantidad_de_fallecidos'][df['anio']==value].sum() + df['fallecidos_en_tierra'][df['anio']==value].sum()
        return "{:,}".format(muertos)

@app.callback(
    Output('number-crashes', 'children'),
    [Input('value-dropdown', 'value')],
    [Input('countries-dropdown', 'value')]
)
def number_crashes(value, value2):
    if value2 == 'Decades':
        accidentes = aux['fecha'][aux['decada']==value].sum()
        return "{:,}".format(accidentes)
    else:
        accidentes = df['fecha'][df['anio']==value].count()
        return "{:,}".format(accidentes)

@app.callback(
    Output('total-on-board', 'children'),
    [Input('value-dropdown', 'value')],
    [Input('countries-dropdown', 'value')]
)
def total_onboard(value, value2):
    if value2 == 'Decades':
        abordo = aux2['total_a_bordo'][aux2['decada']==value].sum()
        return "{:,}".format(abordo)

    else:
        abordo = df['total_a_bordo'][df['anio']==value].sum()
        return "{:,}".format(abordo)
    
@app.callback(
    Output('map', 'figure'),
    [Input('aux', component_property='value')]
)
def plot_map(value):
    colorscale=[
                [0,     "#FEFFB1"],
                # [0.5,   "#FCD975"],
                # [0.10,  "#FDB24B"],
                [0.25,  "#FA4E27"],
                [0.65,  "#E11A1C"],
                [1,     "#9B0D0D"],
    ]
    df2 = df.groupby(['pais', 'code'], as_index=False).agg({'fecha':'count'}).sort_values('fecha', ascending=False)
    df2.columns = ['Country', 'Code', 'Crashes']

    fig = px.choropleth(df2, locations="Code",
                        color="Crashes", 
                        hover_name="Country",
                        # color_continuous_scale=px.colors.diverging.RdGy_r,
                        color_continuous_scale=colorscale
                        )
    fig.update_layout({
        'plot_bgcolor': 'rgba(1, 1, 1, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_family': 'Lato',
        'font_color': 'white',
        })
    fig.update_layout(geo=dict(bgcolor= '#252525'))

    return fig

@app.callback(
    Output('continents', 'figure'),
    [Input('aux', 'value')]
)
def continents(value):
    aux3 = df[df['continent']!='no continent']
    continentes = aux3.groupby(['continent'], as_index=False).agg({'fecha':'count'}).sort_values('fecha', ascending=True)
    continentes.columns = ['Continent','Crashes']
    continentes['Continent'] = continentes['Continent'] + '  '

    data_graph = [go.Bar(
        y = continentes['Continent'],
        x = continentes['Crashes'],
        orientation='h',
        marker_color=['#E5B028']*len(continentes),
        text=continentes['Crashes'],
        texttemplate='%{text:,.0f}',
        textfont_size=50,
        textfont_color='#202020',
        hoverinfo='none', 
        )]
    layout = go.Layout(
        margin=go.layout.Margin(
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=100, #top margin
        ))
    fig = go.Figure(data=data_graph, layout=layout)
    fig.update_layout({
        'plot_bgcolor': 'rgba(1, 1, 1, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_family': 'Lato',
        'font_color': 'white',
        'title_text': 'Crashes per Continent',
        'title_font_size': 30,
        'title_xanchor': 'center',
        'title_yanchor': 'top',
        'title_x': 0.5,
        'title_y': 0.9,
    })
    fig.update_xaxes(tickfont_size=20, title_font={'size': 20})
    fig.update_traces(width=0.6)
    return fig

@app.callback(
    Output('months', 'figure'),
    [Input('aux', 'value')],
    [Input('slider', 'value')]
)
def months_graph(value, slider):
    
    asientos = df.groupby(['total_a_bordo', 'fecha'], as_index=False).agg({'fecha':'count'})
    asientos['categoria'] = asientos['total_a_bordo'].apply(lambda x: f'<= {slider}' if x <= slider else f'> {slider}')
    asientos2 = asientos.groupby(['categoria'], as_index=False).agg({'fecha': 'sum'})
    
    layout = go.Layout(
    margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=50, #top margin
    ))

    fig = go.Figure(data=[go.Pie(labels=asientos2['categoria'], values=asientos2['fecha'],
                                hole=.5, scalegroup='one', marker_colors=['#E5B028','#A98425','#7E631B','#574411',])],
                    layout=layout)
    fig.update_layout({
        'plot_bgcolor': 'rgba(1, 1, 1, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_family': 'Lato',
        'font_color': 'white',
    })
    fig.update_layout(showlegend=False)
    fig.update_layout(annotations=[dict(text='People<br>per plane', x=0.5, y=0.5, font_size=30, showarrow=False)])
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20)
    

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)