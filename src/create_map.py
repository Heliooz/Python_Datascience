import os
from posix import listdir
import folium

def generate_colors(list_value):
    """ Generate a dict of color to display on the map

    Args:
        list_value : List of the key of the dict

    Returns:
        [type]: Dict key:color
    """
    print("Generating color palette ...")

    tab_value = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'] # Possible hexa value
    tab_color = []
    for value_1 in tab_value:
        for value_2 in tab_value:
            for value_3 in tab_value:
                # Append the newly created color
                tab_color.append('#'+value_1+value_1+value_2+value_2+value_3+value_3)
    max_size = len(tab_color)
    sample_size = len(list_value)   

    # Generate the step. We don't go all the way to white cause it's not visible on the map
    step = int(max_size/(sample_size*1.2))

    # Create the dict
    to_return = {list_value[index] : tab_color[index*step] for index in range(len(list_value))}

    return to_return

def create_maps(data_frames):
    """ Generate all the maps (neighbourhood colored and price heated) from the given data

    Args:
        data_frames ([type]): List of data_frame of each city
    """
    if('map' not in listdir('src')): # Create map dir if it doesn't exist
        os.mkdir('src/map')
    for data_frame in data_frames: # Foreach of the data_frames key
        print(str(data_frame) + "'s Maps are building ...")
        actual_data = data_frames[data_frame] # Get the data_frame

        # Get the special values for the heat map
        first_base = actual_data['price'].quantile(0.25) 
        second_base = actual_data['price'].quantile(0.5)
        third_base = actual_data['price'].quantile(0.75)

        # Special case of New York 
        to_color = 'district' if (data_frame == 'New York') else 'neighbourhood'

        # Get the neighbourhood list
        values_color = actual_data[to_color].unique().tolist()

        color_palette = generate_colors(values_color)

        # Get the mean coordinates to center the maps
        mean_longitude = actual_data['longitude'].mean()
        mean_latitude = actual_data['latitude'].mean()

        mean_coord = [mean_latitude, mean_longitude]

        # Create both maps
        actual_map = folium.Map(
            mean_coord,
            min_zoom=10
        )
        
        actual_heatmap = folium.Map(
            mean_coord,
            min_zoom=10
        )

        print("Placing markers on the maps ...")
        for element in actual_data.iterrows(): # For each airbnb
            element = element[1] # Get the row
            lat = element['latitude']
            long = element['longitude']
            coloration = element[to_color]

            # Create the neighbourhood colored marker and add it
            marker = folium.Circle(location=[lat, long], radius=1, color=color_palette[coloration])
            marker.add_to(actual_map)

            price = element['price']

            # Select the color depending on the price
            if(price < first_base): 
                heat_color = "#FFBF00"
            elif(price < second_base):
                heat_color = "#FF8000"
            elif(price < third_base): 
                heat_color = "#FF4000"
            else: 
                heat_color = "#FF0000"

            # Create the heated map marker and add it
            heat_marker = folium.Circle(location=[lat, long], radius=1, color=heat_color)
            heat_marker.add_to(actual_heatmap)
        
        # Save both maps under different names
        actual_map.save('src/map/' + data_frame +  '.html')
        actual_heatmap.save('src/map/' + data_frame +  '_heatmap.html')
        print(data_frame + ' maps saved')
        print()