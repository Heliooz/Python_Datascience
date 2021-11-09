import folium

def create_maps(data_frames):
    for data_frame in data_frames:
        actual_data = data_frames[data_frame]

        mean_longitude = actual_data['longitude'].mean()
        mean_latitude = actual_data['latitude'].mean()

        print(mean_longitude)
        print(mean_latitude)
        print("------")