# Local import

from math import pi
from os import WIFCONTINUED
from src.read_data import read_data
from src.get_data import get_data_kaggle as get_data
from src.create_map import create_maps

# Extern import

from dash.dependencies import Input, Output
from dash import html, dcc
import dash
import plotly_express as px

# Function 

def filter_data(city, values, checklist): 
    """ Select the Data needed for the figure wanted

    Args:
        city (str): City selected in city_choice dropdown
        values ([int,int]): Values selected in price_range range slider
        checklist ([str...]): Values selected in city_checklist multi drop down

    Returns:
        [dataframe]: Data frame needed to create the figure
    """
    if(city == 'default'): # Value used when multi choice dropdown is selected
        data = airbnb_data
        if(checklist == []): return dataframes['Paris'] # Special case when nothing is selected
        query = ''
        if(len(checklist) > 4): # Limatation to avoid unreadable graph
            checklist = checklist[:4]
        for city in checklist: # Creation of the query that filters the city
            query = query + "city == '" + city + "' or "
        query= query[:-4] # Cut the last 4 char ("' or")
        data = data.query(query)
        return data
    if(city == ''): # Case when All is selected (price histogram)
        data = airbnb_data
    else : # Case when a particular city is selected
        data = dataframes[city]

    # Remove values outside of the price range
    data = data[data.price > values[0]]
    data = data[data.price < values[1]]

    return data

def clean_data(data):
    """ Remove all the unnecessary columns 

    Args:
        data (dataframe): Data frame 

    Returns:
        [type]: Cleaned dataframe
    """
    print("Cleaning data...")
    to_delete = data.columns.tolist() # Get all the columns of the dataframe
    to_delete.remove('price')  # Remove from the list all the columns needed for the dashboard
    to_delete.remove('review_scores_value')
    to_delete.remove('accommodates')
    to_delete.remove('longitude')
    to_delete.remove('latitude')
    to_delete.remove('city')
    to_delete.remove('neighbourhood')
    to_delete.remove('district')

    data.drop(to_delete, inplace=True, axis=1) # Drop all but the needed columns
    data = data.drop(data[data.price == 0].index) # Drop rows with absurd values

    print("Data cleaned")

    return data


# Main

if __name__ == '__main__': 
    get_data() 
    airbnb_data = clean_data(read_data())

    cities = airbnb_data['city'].unique()  # Get all the cities values
    # Create a dict of dataset 
    dataframes = {city:airbnb_data.query('city == @city') for city in cities} 

    create_maps(dataframes)

    app = dash.Dash(__name__)

    # Create the dashboard layout with all the needed components
    app.layout = html.Div(
        children=[
            html.Div(
                id='nav_bar',
                children=[
                    html.H2(children='Graph choice'),
                    dcc.Dropdown(
                        id='graph_choice',
                        clearable=False,
                        options=[
                            {'label': 'Airbnb Map', 'value':'map'},
                            {'label': 'Airbnb Heatmap', 'value':'heatmap'},
                            {'label': 'Histogram', 'value':'hist'},
                            {'label': 'Price range', 'value': 'price'},
                            {'label': 'Grades', 'value': 'grade'}
                        ],
                        value='map'
                    ),

                    html.Hr(),


                    html.H2(children='Graph settings'),

                    html.Div(
                        id='city_choice_div',
                        children = [
                            html.H3(children='City choice'),
                            dcc.Dropdown(
                                id='city_choice',
                                clearable=False
                            ),
                        ]
                    ),                    

                    html.Div(
                        id='price_range_div',
                        children=[
                            html.H3(children='Price range'),
                            dcc.RangeSlider(
                                id='price_range',
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ]
                    ),

                    html.Div(
                        id='city_checklist_div',
                        children=[
                            html.H3(children='City choice(s)'),
                            dcc.Dropdown(
                                id='city_checklist',
                                clearable=False,
                                multi=True
                            ) 
                        ]
                    ),

                    html.Hr(),

                    html.Div(children='Clément MAURER & Jeremy DEMAY -- ESIEE PARIS')                    
                ],
                style={'flex': 1,'padding': 10}
            ),
            html.Div(
                id='fig',
                children=[
                    html.H1(id='graph_title'),

                    html.Div(
                        id='figure_display',
                        children = dcc.Graph(id='graph_figure'),
                        hidden=True
                    ),

                    html.Div(
                        id='map_display',
                        children = html.Iframe
                        (
                            id='map', 
                            style={'display': 'block'},
                            height='400px',
                            width='100%'
                        ),
                        hidden=False
                    ),
                    
                ],
                style={'border-left':'1px gray solid','flex': 3,'padding': 10}
            )
        ],
        style={'display': 'flex', 'flex-direction': 'row'}
    )

    # Callback

    @app.callback(
        [
            Output(component_id='city_choice', component_property='options'),
            Output(component_id='city_choice', component_property='value'),
            Output(component_id='city_choice_div', component_property='style'),
            Output(component_id='city_checklist', component_property='options'),
            Output(component_id='city_checklist', component_property='value'),
            Output(component_id='city_checklist_div', component_property='style'),
            Output(component_id='price_range_div', component_property='style')
        ],
        Input(component_id='graph_choice', component_property='value')
    )
    def setup_city_choice(input_graph):
        """ Create the appropriate city selector layout depending on the graph selected

        Args:
            input_graph (str): Graph selected in the graph_choice dropdown 

        Returns:
            [object]: List of the different components needed to create the expected layout
        """
        choices = [{'label': city, 'value': city} for city in cities]
        # If map or heatmap only the city_choice in needed
        if(input_graph == 'map' or input_graph == 'heatmap'):
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'},{'display':'none'}]
        # If hist city_choice (with All value) and price range are needed 
        elif(input_graph == 'hist'):            
            choices.append({'label': 'All', 'value': ''})
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'},{'display':'block'}]
        # Else, only the multi choice dropdown is needed
        else : 
            return [choices,'default',{'display':'none'},choices,['Paris'],{'display':'block'},{'display':'none'}]
    
    
    @app.callback(
        [
            Output(component_id='price_range', component_property='min'),
            Output(component_id='price_range', component_property='max'),
            Output(component_id='price_range', component_property='value'),
            
        ],
        Input(component_id='city_choice', component_property='value')
    )
    def setup_range(input_city):
        """ Create the appropriate price range selector and display it if needed

        Args:
            input_city (str): City selected in city_choice, 
            'default' is the value when the slider isn't needed

        Returns:
            [object]: List of the different components needed to create the expected layout
        """
        if(input_city == 'default'): # Default case price range isn't displayed nor used
            return [0, 0, [0, 0]]
        if(input_city == ''): # All case
            df = airbnb_data
        else : # City is specified
            df = dataframes[input_city]

        min = df['price'].min() 
        max = df['price'].mean()*10 # We don't use max cause the value gap is too big

        return [min, max, [min, max]]

    @app.callback(
        [
            Output(component_id='graph_title', component_property='children'),
            Output(component_id='graph_figure', component_property='figure'),
            Output(component_id='figure_display', component_property='hidden'),
            Output(component_id='map_display', component_property='hidden'),
            Output(component_id='map', component_property='srcDoc'),
        ],
        [
            Input(component_id='graph_choice', component_property='value'),
            Input(component_id='city_choice', component_property='value'),
            Input(component_id='price_range', component_property='value'),
            Input(component_id='city_checklist', component_property='value'),
        ]
    )
    def graph_setup(graph_choice, city_choice, price_range, city_checklist):
        """ Create the graph and graph title depending on the parameters

        Args:
            graph_choice (str): Graph selected in the graph_choice dropdown 
            city_choice (str): City selected in city_choice dropdown
            price_range ([int,int]): Values selected in price_range range slider
            city_checklist ([str...]): Values selected in city_checklist multi drop down
        
        Returns : 
            [] : Title and figure to display
        """

        fig = px.box(airbnb_data, x='price', y='city') # Default graph
        map = open('src/map/Paris.html', 'r').read() # Default map

        if(graph_choice == 'map'): # Map case, map readed
            title = 'Map of {}'.format(city_choice)
            map = open('src/map/{}.html'.format(city_choice), 'r').read()
        elif(graph_choice == 'heatmap'): # Heatmap case, heatmap readed
            title = 'Heatmap of {}'.format(city_choice)
            map = open('src/map/{}_heatmap.html'.format(city_choice), 'r').read()
        else: # Everything with px (no map)
            # Get the needed data
            data = filter_data(city=city_choice, values=price_range, checklist=city_checklist) 
            if(graph_choice == 'hist'): # Price histogram
                title = 'Histogram of the Airbnb value of ' + ('every cities' if city_choice == '' else city_choice)
                fig = px.histogram(data, x='price', labels={'price':'Price'}, histnorm='percent')
            elif(graph_choice == 'price'): # Scatter price 
                title = 'Price of an Airbnb depending on the accomodate number'
                fig = px.scatter(data, x='price', y='accommodates',
                    color='city', labels={'price':'Price', 'accommodates':'Accommodate number'})
            elif(graph_choice == 'grade'): # Grade histogram
                title = 'Grades of listed Airbnb'
                fig = px.histogram(data, x='review_scores_value',
                    color='city', labels={'review_scores_value':'Score'})
            else: 
                title = 'Error'
        
        print(graph_choice)

        # If the map is displayed the graph isn't and same otherwhise
        display_fig = (graph_choice == 'map' or graph_choice == 'heatmap')
        display_map = not display_fig


        print(display_fig)
        print(display_map)

        return[title, fig, display_fig, display_map, map]
     
    
    app.run_server()