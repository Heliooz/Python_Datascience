from pandas import read_csv

def read_data():
    """ Read the CSV file and return the dataframe created

    Returns:
        [pandas.DataFrame]: Dataframe created by the file Listings.csv
    """
    data = read_csv("Airbnb Data/Listings.csv", encoding='CP850')
    return data
