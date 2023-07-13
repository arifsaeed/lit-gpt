import os
from pathlib import Path
import boto3
import csv

class CloudManager:



    def __init__(self,credentials_path):
        aws_access_key_id,aws_secret_access_key,bucket=self.get_credentials(credentials_path)
        self.s3 = boto3.client('s3',
                  endpoint_url='https://s3.eu-west-1.wasabisys.com',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
        
        self.bucket_name = bucket

    def get_credentials(self,folder_path):
        login_dict={}
        with open(folder_path) as file:
            reader = csv.reader(file)
            for row in reader:
                for column in row:
                    keyvalue = column.split("=")
                    login_dict[keyvalue[0]]=keyvalue[1]
        return (login_dict['aws_access_key_id'],login_dict['aws_secret_access_key'],login_dict['bucket'])

    def uplod_all_files_in_folder(self,path,folder,prefix=None):
        folder_path = os.path.join(path, folder)
        #data_dir = Path(path + data_path)
        files = os.listdir(folder_path)
        if prefix!=None:
            prefix=prefix + "_"
        for file in files:
            self.upload_file_to_cloud(folder_path,file,prefix)

    def upload_file_to_cloud(self,folder_path,file,prefix):
        if prefix!=None:
            key_name = prefix + file
        else:
            key_name=file
        file_path = os.path.join(folder_path,file)
        for tries in range(3):
            try:
                self.s3.upload_file(file_path, Bucket=self.bucket_name, Key=key_name)
            except Exception as e:
                if tries<2:
                    print(e)
                    print(f"attempts {tries+1} of 3")
                else:
                    raise e 

                    
        
    def download_all_files(self,files,save_path,new_names=None):
        for idx,file in enumerate(files):
            file_path =  os.path.join(save_path,file) 
            if new_names!=None:
                file_path =  os.path.join(save_path,new_names[idx]) 
            self.s3.download_file(Bucket=self.bucket_name,Key=file,Filename=file_path)


def init_cloud_uploader_from_args(args):
    key = args.aws_access_key_id
    secret= args.aws_secret_access_key
    bucket=args.aws_bucket
    return CloudManager(key,secret,bucket)


def init_cloud_uploader_from_params(key,secret,bucket):
    return CloudManager(key,secret,bucket)