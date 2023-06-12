from google.cloud import storage

import datetime



def generate_download_signed_url_v4(bucket_name, blob_name):
    return f"https://storage.cloud.google.com/{bucket_name}/{blob_name}?authuser=0"   
