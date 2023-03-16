import base64
import json
import os
from google.cloud import storage
import time
import psycopg2
from datetime import datetime
import requests

BUCKET_GCP_IMAGES = "images_detection_virus"
url2 = "https://ddd-object-detection-unyu5blyja-ew.a.run.app/predict/"


def get_image_inference_from_model(image_encoded):
    message_dict = {"image": image_encoded}
    # Convert the dictionary to a JSON string
    message_str = json.dumps(message_dict)
    # Send the message to the API
    print("sending image base64")
    response = requests.post(url2, json=message_dict)
    # {'Virus': 'Lassa', 'Proba = ': 0.95}
    result_dict = {}
    # json to dict
    result_dict = response.json()
    print(result_dict)
    virus = result_dict["virus"]
    count = result_dict["virus_count"]
    return virus, count


def write_data(virus, virus_count):
    conn = psycopg2.connect(f"dbname={os.environ['DB_NAME']} host={os.environ['DB_HOST']} user={os.environ['DB_USER']} password={os.environ['DB_PASSWORD']}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Execute a query
    query = f"""
    INSERT INTO {os.environ['DB_TABLE_DETECTION']}
    VALUES ('{virus}', '{virus_count}', '{timestamp}')
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
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    pubsub_message = json.loads(pubsub_message)

    image_encoded = pubsub_message["image"]
    # get the results of the inference
    virus, count = get_image_inference_from_model(image_encoded)
    write_data(virus,count)
