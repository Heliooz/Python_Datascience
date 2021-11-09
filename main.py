# Local import

from src.read_data import read_data
from src.get_data import get_data

# Extern import

from dash.dependencies import Input, Output
from dash import html, dcc
import dash
import plotly_express as px

# Function 

def filter_data(city, values, checklist): 
    if(city == 'default'):
        data = airbnb_data
        if(checklist == []): return data
        query = ''
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

                    dcc.Graph(id='graph_figure')
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
        ],
        Input(component_id='graph_choice', component_property='value')
    )
    def setup_city_choice(input_graph):
        choices = [{'label': city, 'value': city} for city in cities]
        if(input_graph == 'map'):
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'}]
        elif(input_graph == 'hist'):            
            choices.append({'label': 'All', 'value': ''})
            return [choices,'Paris',{'display':'block'},choices,['Paris'],{'display':'none'}]
        else : 
            return [choices,'default',{'display':'none'},choices,['Paris'],{'display':'block'}]
    
    
    @app.callback(
        [
            Output(component_id='price_range', component_property='min'),
            Output(component_id='price_range', component_property='max'),
            Output(component_id='price_range', component_property='value'),
            Output(component_id='price_range_div', component_property='style')
        ],
        Input(component_id='city_choice', component_property='value')
    )
    def setup_range(input_city):
        if(input_city == 'default'):
            return [0, 0, [0, 0], {'display':'none'}]
        if(input_city == ''):
            df = airbnb_data
        else : 
            df = dataframes[input_city]

        min = df['price'].min()
        max = df['price'].mean()*10

        return [min, max, [min, max], {'display':'block'}]

    @app.callback(
        [
            Output(component_id='graph_title', component_property='children'),
            Output(component_id='graph_figure', component_property='figure')
        ],
        [
            Input(component_id='graph_choice', component_property='value'),
            Input(component_id='city_choice', component_property='value'),
            Input(component_id='price_range', component_property='value'),
            Input(component_id='city_checklist', component_property='value'),
        ]
    )
    def graph_setup(graph_choice, city_choice, price_range, city_checklist):
        data = filter_data(city=city_choice, values=price_range, checklist=city_checklist)
        if(graph_choice == 'map'):
            title = 'Map of {}'.format(city_choice)
            fig= px.scatter(data, x='longitude', y='latitude', color='neighbourhood')
        elif(graph_choice == 'hist'):
            title = 'Histogram of the Airbnb value of ' + ('every cities' if city_choice == '' else city_choice)
            fig = px.histogram(data, x='price')
        elif(graph_choice == 'price'):
            title = 'Price of an Airbnb depending on the accomodate number'
            fig = px.scatter(data, x='price', y='accommodates', color='neighbourhood', facet_col='city')
        elif(graph_choice == 'grade'):
            title = 'Percentage of the grades of listed Airbnb'
            fig = px.histogram(data, x='review_scores_value', color='city')
        else: 
            title = 'Error'
            fig = px.box(data)

        return[title, fig]
     
    
    app.run_server(debug=True)