# Local import

from math import pi
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
    if(city == 'default'):
        data = airbnb_data
        if(checklist == []): return dataframes['Paris']
        query = ''
        if(len(checklist) > 4):
            checklist = checklist[:4]
        for city in checklist:
            query = query + "city == '" + city + "' or "
        query= query[:-4]
        data = data.query(query)
        return data
    if(city == ''):
        data = airbnb_data
    else : 
        data = dataframes[city]

    data = data[data.price > values[0]]
    data = data[data.price < values[1]]

    return data

def clean_data(data): 
    to_delete = data.columns.tolist()
    to_delete.remove('price')
    to_delete.remove('review_scores_value')
    to_delete.remove('accommodates')
    to_delete.remove('longitude')
    to_delete.remove('latitude')
    to_delete.remove('city')
    to_delete.remove('neighbourhood')

    data.drop(to_delete, inplace=True, axis=1)

    return data


# Main

if __name__ == '__main__': 
    get_data()
    airbnb_data = clean_data(read_data())

    print(airbnb_data)

    cities = airbnb_data['city'].unique()   
    dataframes = {city:airbnb_data.query('city == @city') for city in cities}

    create_maps(dataframes)

    app = dash.Dash(__name__)

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

                    html.Iframe(
                        id='map', 
                        style={'display': 'none'}
                    )
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
        if(input_graph == 'map'):
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'},{'display':'none'}]
        elif(input_graph == 'hist'):            
            choices.append({'label': 'All', 'value': ''})
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'},{'display':'block'}]
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
        if(input_city == 'default'):
            return [0, 0, [0, 0]]
        if(input_city == ''):
            df = airbnb_data
        else : 
            df = dataframes[input_city]

        min = df['price'].min()
        max = df['price'].mean()*10

        return [min, max, [min, max]]

    @app.callback(
        [
            Output(component_id='graph_title', component_property='children'),
            Output(component_id='graph_figure', component_property='figure'),
            Output(component_id='figure_display', component_property='hidden'),
            Output(component_id='map', component_property='display')
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
        data = filter_data(city=city_choice, values=price_range, checklist=city_checklist)
        if(graph_choice == 'map'):
            title = 'Map of {}'.format(city_choice)
            fig= px.scatter(data, x='longitude', y='latitude',
                color='neighbourhood', labels={'longitude':'Longitude', 'latitude':'Latitude'})
        elif(graph_choice == 'hist'):
            title = 'Histogram of the Airbnb value of ' + ('every cities' if city_choice == '' else city_choice)
            fig = px.histogram(data, x='price', labels={'price':'Price'}, histnorm='percent')
        elif(graph_choice == 'price'):
            title = 'Price of an Airbnb depending on the accomodate number'
            fig = px.scatter(data, x='price', y='accommodates',
                color='city', labels={'price':'Price', 'accommodates':'Accommodate number'})
        elif(graph_choice == 'grade'):
            title = 'Grades of listed Airbnb'
            fig = px.histogram(data, x='review_scores_value',
                color='city', labels={'review_scores_value':'Score'})
        else: 
            title = 'Error'
            fig = px.box(data)
        
        print(graph_choice)

        display_fig = (graph_choice == 'map')
        display_map = {'display':'block'} if (graph_choice == 'map') else {'display':'none'}

        return[title, fig, display_fig, display_map]
     
    
    app.run_server()