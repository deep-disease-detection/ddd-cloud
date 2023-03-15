import streamlit as st
import base64
import requests


st.header(" Use our model to find the type of 🦠🦠🦠🦠")

# User uploads image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "tif","tiff"])


def get_image_inference_from_model(image):
    """ Returns the type of virus and the probabilty (tuple) of the image
        uploaded by user
    """
    url = "https://ddd-model-unyu5blyja-ew.a.run.app/predict/"

    # Convert image to bytes
    bytes_data = image.getvalue()
    image_encoded = base64.b64encode(bytes_data).decode("utf-8")
    message_dict = {"image": image_encoded}

    # Convert Dict to a JSON string
    response = requests.post(url, json=message_dict)
    result_dict = {}
    # Convert Json to a Dict
    result_dict = response.json()
    print(result_dict)
    virus = result_dict["Virus"]
    proba = result_dict["Proba"]

    return virus, proba



if uploaded_file:
    virus, proba = get_image_inference_from_model(uploaded_file)
    st.write(f"CONGRATS ! Your virus is {virus} with a probability of {proba}")
    st.image(uploaded_file)
