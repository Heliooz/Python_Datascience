import pandas as pd
import plotly_express as px

def print_data(data):
        print(data['name'])

def draw_map(data, city_name):
        new_dataset = data.query("city=='"+ city_name +"'")
        print(new_dataset.describe())
        fig = px.scatter(new_dataset, x='longitude', y='latitude', color='neighbourhood')

        fig.show()       
