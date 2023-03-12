import json
import base64

# The `topic_path` method creates a fully qualified identifier
topic_path = "projects/gcp-ddd-project/subscriptions/images-sub"
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# TODO(developer)
project_id = "gcp-ddd-project"
subscription_id = "images-sub"
# Number of seconds the subscriber should listen for messages
timeout = 60

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)
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



def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    # transform message to json
    message_json = json.loads(message.data)
    # get image from json
    image = message_json["image"]
    # decode image from base64
    image_decoded = base64.b64decode(image)

    # save image to file
    save_image_to_bucket_gcp(image_decoded, BUCKET_GCP_IMAGES)

    with open("dog_from_pub_sub.jpg", "wb") as image_file:
        image_file.write(image_decoded)

    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
