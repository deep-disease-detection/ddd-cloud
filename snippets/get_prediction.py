# code to get prediction from the model via the API:

import requests
import base64
import json
from fastapi import FastAPI, UploadFile, UploadFile

url = "http://localhost:8000/predict"
url2 = "https://test-esn3iombla-ew.a.run.app/predict"

# Read the image into memory
with open("dog.jpg", "rb") as f:
    image = f.read()
    # transform the image into a JSON string
    image_str = base64.b64encode(image).decode("utf-8")
    # Create a dictionary representing your JSON message
    message_dict = {"image": image_str}
    # Convert the dictionary to a JSON string
    message_str = json.dumps(message_dict)
    # Send the message to the API
    print('sending image base64')

    response = requests.post(url, data=message_str)

    print(response.text)
