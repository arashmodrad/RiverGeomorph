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
        self.link = "https://ebfedata.s3.amazonaws.com/"+self.HUC8_code+"_"+self.name+"/"+self.HUC8_code+"_SpatialData.zip"

    def downLoad(self):
        # Directories
        geodatabase_download_directory = "GDP_DL"
        Parent_download_directory = "DATA_DL"
        path = Path.cwd()

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

        save_GDP_path = os.path.join(save_GDP_path, self.HUC8_code+"_"+self.name)

        try:   
            read_url = requests.get(self.link)
        except:
            print("invalid url >> cehck servers")

        zip_file = zipfile.ZipFile(io.BytesIO(read_url.content))
        
        zip_file.extractall(save_GDP_path)

        print('Done!')

class RunDL:
    @staticmethod
    def main(args):
        HUC8_code = str(input("Enter HUC8 code: ")) #"11130210"
        with open('HUC8_names.json') as json_data:
            h_data = json.load(json_data)
        HUC8_names = pd.DataFrame(h_data['data'],columns=['huc', 'basin'])
        HUC8_names["huc"]=HUC8_names["huc"].values.astype(str)
        HUC8_names["basin"]=HUC8_names["basin"].values.astype(str)
        h_series = HUC8_names['basin'].loc[HUC8_names['huc'] == HUC8_code]
        h_name = str(h_series.iloc[0]).replace(" ", "")
        # name = str(input("Enter watershed name code: ")) #"LakeTexoma"
        data_obg = DataDownloader(HUC8_code, h_name) 
        data_obg.downLoad()

if __name__ == "__main__":
    RunDL.main([])

# from pandas.io.json import json_normalize


