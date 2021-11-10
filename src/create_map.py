import os
from posix import listdir
import folium

def generate_colors(list_value):
    print("Generating color palette ...")

    tab_value = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    tab_color = []
    for value_1 in tab_value:
        for value_2 in tab_value:
            for value_3 in tab_value:
                tab_color.append('#'+value_1+value_1+value_2+value_2+value_3+value_3)
    max_size = len(tab_color)
    sample_size = len(list_value)

    step = int(max_size/(sample_size*1.2))

    to_return = {list_value[index] : tab_color[index*step] for index in range(len(list_value))}

    return to_return

def create_maps(data_frames):
    if('map' not in listdir('src')):
        os.mkdir('src/map')
    for data_frame in data_frames:
        print(str(data_frame) + "'s Maps are building ...")
        actual_data = data_frames[data_frame]

        first_base = actual_data['price'].quantile(0.25)
        second_base = actual_data['price'].quantile(0.5)
        third_base = actual_data['price'].quantile(0.75)

        to_color = 'district' if (data_frame == 'New York') else 'neighbourhood'

        values_color = actual_data[to_color].unique().tolist()

        color_palette = generate_colors(values_color)

        mean_longitude = actual_data['longitude'].mean()
        mean_latitude = actual_data['latitude'].mean()

        mean_coord = [mean_latitude, mean_longitude]

        min_latitude = actual_data['latitude'].min()
        max_latitude = actual_data['latitude'].max()

        min_longitude = actual_data['longitude'].min()
        max_longitude = actual_data['longitude'].max()

        actual_map = folium.Map(
            mean_coord,
            min_zoom=10, 
            min_lat=min_latitude,
            max_lat=max_latitude,
            min_lon=min_longitude,
            max_lon=max_longitude
        )
        
        actual_heatmap = folium.Map(
            mean_coord,
            min_zoom=10, 
            min_lat=min_latitude,
            max_lat=max_latitude,
            min_lon=min_longitude,
            max_lon=max_longitude
        )

        print("Placing markers on the maps ...")
        for element in actual_data.iterrows():
            element = element[1]
            lat = element['latitude']
            long = element['longitude']
            coloration = element[to_color]

            marker = folium.Circle(location=[lat, long], radius=1, color=color_palette[coloration])
            marker.add_to(actual_map)

            price = element['price']

            if(price < first_base): 
                heat_color = "#FFBF00"
            elif(price < second_base):
                heat_color = "#FF8000"
            elif(price < third_base): 
                heat_color = "#FF4000"
            else: 
                heat_color = "#FF0000"

            heat_marker = folium.Circle(location=[lat, long], radius=1, color=heat_color)
            heat_marker.add_to(actual_heatmap)

        actual_map.save('src/map/' + data_frame +  '.html')
        actual_heatmap.save('src/map/' + data_frame +  '_heatmap.html')
        print(data_frame + ' maps saved')
        print()