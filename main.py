# Local import

from src.read_data import read_data
from src.get_data import get_data

# Extern import

from dash.dependencies import Input, Output
import dash
from dash import html, dcc
import plotly_express as px

# Main

if __name__ == '__main__': 
    get_data()
    airbnb_data = read_data()

    current_city = "Paris"

    cities = airbnb_data['city'].unique()   

    graphs = {city:airbnb_data.query("city == @city") for city in cities}

    app = dash.Dash(__name__)

    fig = px.scatter(graphs[current_city], x='longitude', y='latitude', color='neighbourhood')

    app.layout = html.Div(children=[
                            html.H1(
                                id='title',
                                children=f"Map of {current_city}'s Airbnb",
                                style={'textAlign': 'center', 'color': '#7FDBFF'}
                            ), 

                            html.Label('City'),
                            
                            dcc.Dropdown(
                                id='city_dropdown',
                                options=[{'label': city, 'value':city} for city in cities],
                                value="Paris"
                            ),

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ),

                            html.Label('Max price'),
                            dcc.Slider(
                                id='max_price',
                                min=0,
                                max=500,
                                step=5,
                                value=250,
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),

                            html.Div(
                                id='description',
                                children=f'''
                                The map shows the location of all Airbnb for the city of {current_city}. 
                            '''
                            ),
    ]
    )

    @app.callback(
        [
            Output(component_id='title', component_property='children'),
            Output(component_id='graph1', component_property='figure'),
            Output(component_id='description', component_property='children')
        ],
        [
            Input(component_id='city_dropdown', component_property='value'),
            Input(component_id='max_price', component_property='value')
        ]
    )

    def update_figure(input_city, input_price): 
        city_data = graphs[input_city]
        city_data = city_data[city_data.price < input_price]
        return [
            "Map of {}'s Airbnb".format(input_city),
            px.scatter(city_data, x='longitude', y='latitude', color='neighbourhood'),
            "The map shows the location of all Airbnb for the city of {}.".format(input_city)
        ]
    
    app.run_server(debug=True)

