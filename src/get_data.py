# Require : 

# - kaggle 
# - kaggle key 

import os

def get_data():
    if("airbnb-listings-reviews.zip" not in os.listdir()):
        command_get_kaggle_data = "kaggle datasets download -d mysarahmadbhat/airbnb-listings-reviews"
        os.system(command_get_kaggle_data)
    else : print("Archive deja telechargee")

    command_unzip_data = "unzip -o airbnb-listings-reviews.zip"
    os.system(command_unzip_data)


import kaggle
import shutil

def get_data_kaggle():
    kaggle.api.authenticate()

    if("airbnb-listings-reviews.zip" not in os.listdir()):
        kaggle.api.dataset_download_files("mysarahmadbhat/airbnb-listings-reviews")
    else : print("Archive deja telechargee")

    shutil.unpack_archive("airbnb-listings-reviews.zip", ".")

