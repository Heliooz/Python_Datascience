from pandas import read_csv

def read_data():
    data = read_csv("Airbnb Data/Listings.csv", encoding='CP850')
    return data
