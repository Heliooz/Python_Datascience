from pandas import read_csv

def read_data(fileName):

    data = read_csv('Airbnb Data/Listings.csv', encoding='ISO-8859-1')
    return data

