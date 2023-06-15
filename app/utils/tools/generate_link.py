from google.cloud import storage

import datetime


from google.auth.transport import requests
from google.auth import default, compute_engine
    
credentials, _ = default()

# then within your abstraction
auth_request = requests.Request()
credentials.refresh(auth_request)

signing_credentials = compute_engine.IDTokenCredentials(
    auth_request,
    "",
    service_account_email=credentials.service_account_email
)

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
        credentials=signing_credentials,
        method="GET"
    )

    return signed_url
