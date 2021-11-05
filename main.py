# Local import

from os import chdir
from src.read_data import read_data
from src.get_data import get_data

# Extern import

from dash.dependencies import Input, Output
from dash import html, dcc
import dash
import plotly_express as px

# Function 

def filter_data(city, values): 
    if(city == ''):
        data = airbnb_data
    else : 
        data = dataframes[city]

    data = data[data.price > values[0]]
    data = data[data.price < values[1]]

    return data

# Main

if __name__ == '__main__': 
    get_data()
    airbnb_data = read_data()

    cities = airbnb_data['city'].unique()   
    dataframes = {city:airbnb_data.query('city == @city') for city in cities}

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Div(
                id='nav_bar',
                children=[
                    html.H2(children='Graph choice'),
                    dcc.Dropdown(
                        id='graph_choice',
                        options=[
                            {'label': 'Airbnb Map', 'value':'map'},
                            {'label': 'Histogram', 'value':'hist'}
                        ],
                        value='map'
                    ),

                    html.Hr(),

                    html.H2(children='Graph settings'),

                    html.H3(children='City choice'),
                    dcc.Dropdown(id='city_choice'),

                    html.H3(children='Price range'),
                    dcc.RangeSlider(
                        id='price_range',
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),

                    html.Hr(),

                    html.Div(children='Clément MAURER & Jeremy DEMAY -- ESIEE PARIS')

                    
                ],
                style={'border-right':'1px gray solid','flex': 1,'padding': 10, 'height': '100%'}
            ),
            html.Div(
                id='fig',
                children=[
                    html.H1(id='graph_title'),

                    dcc.Graph(id='graph_figure')
                ],
                style={'flex': 3,'padding': 10}
            )
        ],
        style={'display': 'flex', 'flex-direction': 'row'}
    )

    @app.callback(
        [
            Output(component_id='city_choice', component_property='options'),
            Output(component_id='city_choice', component_property='value')
        ],
        Input(component_id='graph_choice', component_property='value')
    )
    def setup_city_choice(input_graph):
        choices = [{'label': city, 'value': city} for city in cities]
        if(input_graph == 'map'):
            return [choices,'Paris']
        elif(input_graph == 'hist'):            
            choices.append({'label': 'All', 'value': ''})
            return [choices,'Paris']
        else : 
            return ["",""]
    
    
    @app.callback(
        [
            Output(component_id='price_range', component_property='min'),
            Output(component_id='price_range', component_property='max'),
            Output(component_id='price_range', component_property='value'),
        ],
        Input(component_id='city_choice', component_property='value')
    )
    def setup_range(input_city):
        if(input_city == ''):
            df = airbnb_data
        else : 
            df = dataframes[input_city]

        min = df['price'].min()
        max = df['price'].max()

        return [min, max, [min, max]]

    @app.callback(
        [
            Output(component_id='graph_title', component_property='children'),
            Output(component_id='graph_figure', component_property='figure')
        ],
        [
            Input(component_id='graph_choice', component_property='value'),
            Input(component_id='city_choice', component_property='value'),
            Input(component_id='price_range', component_property='value'),
        ]
    )
    def graph_setup(graph_choice, city_choice, price_range):
        data = filter_data(city=city_choice, values=price_range)
        if(graph_choice == 'map'):
            title = 'Map of {}'.format(city_choice)
            fig= px.scatter(data, x='longitude', y='latitude', color='neighbourhood')
        elif(graph_choice == 'hist'):
            title = 'Histogram of the Airbnb value of ' + ('every cities' if city_choice == '' else city_choice)
            fig = px.histogram(data, x='price')
        else: title = ''

        return[title, fig]
     
    
    app.run_server(debug=True)

    

