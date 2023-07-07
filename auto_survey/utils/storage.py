# This script `storage.py` is used to handle the cloud storage.
#   `upload_file`:
#       Function to upload a local file to the specified S3 bucket.
#       If the target_name is not specified, it will use the file_name as the object key.
#   `list_all_files`:
#       Function to list all the files in the specified S3 bucket.
#   `download_file`:
#       Function to download a file from the specified S3 bucket to the local machine using the specified file_name.

import os
import boto3

BUCKET_NAME = "hf-storage"

def get_client():
    access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    return s3, bucket

def upload_file(file_name, target_name=None):
    s3, _ = get_client()

    if target_name is None:
        target_name = file_name
    s3.meta.client.upload_file(Filename=file_name, Bucket=BUCKET_NAME, Key=target_name)
    print(f"The file {file_name} has been uploaded!")


def list_all_files():
    _, bucket = get_client()
    return [obj.key for obj in bucket.objects.all()]


def download_file(file_name):
    ''' Download `file_name` from the bucket.
    Bucket (str) – The name of the bucket to download from.
    Key (str) – The name of the key to download from.
    Filename (str) – The path to the file to download to.
    '''
    s3, _ = get_client()
    s3.meta.client.download_file(Bucket=BUCKET_NAME, Key=file_name, Filename=file_name)
    print(f"The file {file_name} has been downloaded!")

if __name__ == "__main__":
    file = "sample-output.pdf"
    upload_file(file)
