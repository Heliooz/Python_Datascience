from read_data import read_data
import display_data 
from get_data import get_data

## get_data()
data = read_data('Airbnb Data/Listings.csv')
display_data.draw_map(data, "Cape Town")