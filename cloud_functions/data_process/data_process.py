import base64
import json
import os
from google.cloud import storage
import time
import requests
import base64
import json
import psycopg2
from datetime import datetime


BUCKET_GCP_IMAGES = "images_classification_virus"
url2 = "https://ddd-model-unyu5blyja-ew.a.run.app/predict/"

def save_image_to_bucket_gcp(image, bucket, virus, proba):
    """Save image to bucket in GCP
    Args:
         image (bytes): Image to be saved
         bucket (str): Bucket name
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    name_photo = str(virus)+".jpg"
    # add timestamp to name
    name_photo = name_photo.split(".")[0] + "-" + str(time.time()) + ".jpg"
    blob = bucket.blob(os.path.basename(name_photo))
    # add metadata to image
    blob.metadata = {"time": str(time.time()), "class": virus, "proba": proba}
    blob.upload_from_string(image, content_type="image/jpeg")
    print("Image saved to bucket")


def get_image_inference_from_model(image_encoded):

    message_dict = {"image": image_encoded}
    # Convert the dictionary to a JSON string
    message_str = json.dumps(message_dict)
    # Send the message to the API
    print('sending image base64')
    response = requests.post(url2, json=message_dict)
    # {'Virus': 'Lassa', 'Proba = ': 0.95}
    result_dict = {}
    # json to dict
    result_dict = response.json()
    print(result_dict)
    virus = result_dict["Virus"]
    proba = result_dict["Proba"]
    return virus, proba


# code to get prediction from the model via the API:
def write_data_to_db(virus, proba):
    conn = psycopg2.connect(f"dbname={os.environ['DB_NAME']} host={os.environ['DB_HOST']} user={os.environ['DB_USER']} password={os.environ['DB_PASSWORD']}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Execute a query
    query = f"""
    INSERT INTO {os.environ['DB_TABLE_CLASSIFICATION']}
    VALUES ('{virus}', '{proba}', '{timestamp}')
    """

    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = json.loads(pubsub_message)

    image_encoded = pubsub_message["image"]
    # get the results of the inference
    virus, proba = get_image_inference_from_model(image_encoded)
    # decode image
    image_decoded = base64.b64decode(image_encoded)
    # save image to file with metadata
    save_image_to_bucket_gcp(image_decoded, BUCKET_GCP_IMAGES, virus, proba)
