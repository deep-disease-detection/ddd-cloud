import streamlit as st
import base64
import requests


st.header(" Use our model to find the type of 🦠🦠🦠🦠")


uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


def get_image_inference_from_model(image):
    url = "https://ddd-object-detection-unyu5blyja-ew.a.run.app/predict/"
    bytes_data = image.getvalue()
    image_encoded = base64.b64encode(bytes_data).decode("utf-8")
    message_dict = {"image": image_encoded}

    # Convert the dictionary to a JSON string
    response = requests.post(url, json=message_dict)

    # json to dict
    result = response.json()
    print(result)
    virus = result["virus"]
    count = result["virus_count"]

    return virus, count


if uploaded_file:
    virus, count = get_image_inference_from_model(uploaded_file)
    st.write(
        "Your 🦠 picture was successfully processed !"
    )
