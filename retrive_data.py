# importing modules
import os
from pathlib import Path
import requests, zipfile, io
import pandas as pd
import json

class DataDownloader:
    def __init__(self, HUC8_code, name):
        self.HUC8_code = HUC8_code
        self.name = name
        self.gdb_link = "https://ebfedata.s3.amazonaws.com/"+self.HUC8_code+"_"+self.name+"/"+self.HUC8_code+"_SpatialData.zip"
        self.hec_link = "https://ebfedata.s3.amazonaws.com/"+self.HUC8_code+"_"+self.name+"/"+self.HUC8_code+"_Models.zip"

    def downLoad(self):
        """
        A function to retrive USGS cross section data
        """
        # Directories
        geodatabase_download_directory = "GDP_DL"
        hec_ras_download_directory = "HEC_RAS_DL"
        Parent_download_directory = "DATA_DL"
        path = Path.cwd()

        # Check for existing paths or creat new ones
        if os.path.exists(os.path.join(path, Parent_download_directory)):
            print("parent path exists")
        else:
            os.mkdir(os.path.join(path, Parent_download_directory))
            print("parent path created")

        save_GDP_path = os.path.join(path, Parent_download_directory, geodatabase_download_directory)
        if os.path.exists(save_GDP_path):
            print("save path exists")
        else:
            os.mkdir(save_GDP_path)
            print("save path created")

        save_HEC_RAS_path = os.path.join(path, Parent_download_directory, hec_ras_download_directory)
        if os.path.exists(save_HEC_RAS_path):
            print("save path exists")
        else:
            os.mkdir(save_HEC_RAS_path)
            print("save path created")

        save_GDP_path = os.path.join(save_GDP_path, self.HUC8_code+"_"+self.name)
        save_HEC_RAS_path = os.path.join(save_HEC_RAS_path, self.HUC8_code+"_"+self.name)

        # build the url, download and extract the data
        try:   
            # Geo-database file
            read_url = requests.get(self.gdb_link)
            zip_file = zipfile.ZipFile(io.BytesIO(read_url.content))
            zip_file.extractall(save_GDP_path)

            # Hec_Ras model file
            read_url = requests.get(self.hec_link)
            zip_file = zipfile.ZipFile(io.BytesIO(read_url.content))
            zip_file.extractall(save_HEC_RAS_path)
        except:
            print("invalid url >> cehck servers")

        print('Download Complete')

# A driver class
class RunDL:
    @staticmethod
    def main(args):
        # Get HUC8 as input
        HUC8_code = str(input("Enter HUC8 code: ")) #"11130210"
        
        # Search for HUC8 watershed names
        with open('HUC8_names.json') as json_data:
            h_data = json.load(json_data)
        HUC8_names = pd.DataFrame(h_data['data'],columns=['huc', 'basin'])
        HUC8_names["huc"]=HUC8_names["huc"].values.astype(str)
        HUC8_names["basin"]=HUC8_names["basin"].values.astype(str)
        h_series = HUC8_names['basin'].loc[HUC8_names['huc'] == HUC8_code]
        h_name = str(h_series.iloc[0]).replace(" ", "")
        # name = str(input("Enter watershed name code: ")) #"LakeTexoma"
        
        # Bulid an instance of DataDownloader object
        data_obg = DataDownloader(HUC8_code, h_name) 

        # Download 
        data_obg.downLoad()

if __name__ == "__main__":
    RunDL.main([])



