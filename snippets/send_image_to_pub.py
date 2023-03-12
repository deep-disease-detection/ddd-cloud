from google.cloud import pubsub_v1
import json
import base64
import random
import os
import time

# Create a publisher client
publisher = pubsub_v1.PublisherClient()

# The `topic_path` method creates a fully qualified identifier
topic_path = "projects/gcp-ddd-project/topics/images"

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string
while True:
    # scrap the folder and select a random image to send
    path = "../test/Adenovirus"
    random_image = random.choice(os.listdir(path))
    random_image_path = os.path.join(path, random_image)

    #read image from file and convert to base64
    image = get_image_base64(random_image_path)

    # Create a dictionary representing your JSON message
    message_dict_image = {
        "image": image.decode("utf-8")
    }

    print(message_dict_image)
    # Convert the dictionary to a JSON string
    message_str = json.dumps(message_dict_image)

    # Publish the message to the topic
    future = publisher.publish(topic_path, data=message_str.encode("utf-8"))
    print(f"Published message {future.result()} to {topic_path}")
    time.sleep(5)
