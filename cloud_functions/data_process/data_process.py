import base64
import json
import os
from google.cloud import storage
import time

BUCKET_GCP_IMAGES = "images_classification_virus"

def save_image_to_bucket_gcp(image, bucket):
    """Save image to bucket in GCP
    Args:
         image (bytes): Image to be saved
         bucket (str): Bucket name
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    name_photo = "class-1.jpg"
    # add timestamp to name
    name_photo = name_photo.split(".")[0] + "-" + str(time.time()) + ".jpg"
    blob = bucket.blob(os.path.basename(name_photo))
    # add metadata to image
    blob.metadata = {"time": str(time.time()), "class": "dog"}
    blob.upload_from_string(image, content_type="image/jpeg")
    print("Image saved to bucket")

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = json.loads(pubsub_message)
    image = pubsub_message["image"]
    # decode image from base64
    print(image)
    image_decoded = base64.b64decode(image)

    # save image to file
    save_image_to_bucket_gcp(image_decoded, BUCKET_GCP_IMAGES)
