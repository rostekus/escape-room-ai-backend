from google.cloud import storage

import datetime



def generate_download_signed_url_v4(bucket_name, blob_name):
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Get the blob (file) from the bucket
    blob = bucket.blob(blob_name)

    # Generate a signed URL for the blob
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=3600,
        method="GET"
    )

    return signed_url
