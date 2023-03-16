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
        f"It is a picture of a {virus} with {count} particle{'s' if (count>1 or count ==0) else ''}"
    )
    st.image(uploaded_file)


# # Define a function to make a prediction with the machine learning model
# def predict(image):
#     # Prepare the image data
#     img = Image.open(image)
#     # img = img.resize((256, 256))
#     # img = img.convert('RGB')
#     img_bytes = BytesIO()
#     img.save(img_bytes, format='PNG')
#     img_bytes = f'{img_bytes.getvalue()}'

#     img_json = {
#         "image": img_bytes}

#     # Make the API request
#     response = requests.post('https://ddd-model-unyu5blyja-ew.a.run.app/predict', json=img_json)
#     response.raise_for_status()
#     result = response.json()
#     print(result)

#     return result['Virus']


# # Use the uploaded file to make a prediction and display the result
# if uploaded_file is not None:
#     result = predict(uploaded_file)
#     st.write('Prediction:', result)
#     st.image(uploaded_file, caption='Uploaded Image')
