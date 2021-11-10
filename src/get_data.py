import os

def get_data():
    """ Get the data from the web using command line (Linux only) \n
        Kaggle module and key setup needed
    """
    if("airbnb-listings-reviews.zip" not in os.listdir()):
        command_get_kaggle_data = "kaggle datasets download -d mysarahmadbhat/airbnb-listings-reviews"
        os.system(command_get_kaggle_data)
    else : print("Archive deja telechargee")

    command_unzip_data = "unzip -o airbnb-listings-reviews.zip"
    os.system(command_unzip_data)


import kaggle
import shutil

def get_data_kaggle():
    """ Get the data from the web using command line (Linux only) \n
        Kaggle module and key setup needed
    """

    print("Authentification ...")
    kaggle.api.authenticate()
    print("Authentification successful")

    if("airbnb-listings-reviews.zip" not in os.listdir()):
        print("Downloading files from kaggle ...")
        kaggle.api.dataset_download_files("mysarahmadbhat/airbnb-listings-reviews")
        print("Download complete")
    else : print("Archive deja telechargee")

    shutil.unpack_archive("airbnb-listings-reviews.zip", ".")

