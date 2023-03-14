import streamlit as st
from google.cloud import storage
import datetime
from PIL import Image
import numpy as np
import pandas as pd
from statistics import mean
from streamlit_autorefresh import st_autorefresh
import json
import pyautogui

# Set up GCP storage client
client = storage.Client()
bucket_name = "images_classification_virus"
bucket = client.get_bucket(bucket_name)


def get_metadata(blob):
    metadata = {}
    metadata['name'] = blob.name
    metadata['metadata'] = blob.metadata

    return metadata


# Define function to display image and metadata
def display_image_and_metadata(blob):
    metadata = get_metadata(blob)
    st.image(blob.download_as_bytes(), caption=blob.name, use_column_width=True)
    # get time epoch and convert to date
    time_image_epoch = metadata['metadata']['time']
    date_image = datetime.datetime.fromtimestamp(float(time_image_epoch)).strftime('%Y-%m-%d')
    time_image = datetime.datetime.fromtimestamp(float(time_image_epoch)).strftime('%H:%M:%S')
    # convert the date to string
    get_class = metadata['metadata']['class']
    st.metric(label="Class", value=get_class)
    get_proba = metadata['metadata']['proba']
    st.metric(label="Accuracy", value=get_proba)
    st.metric(label="Date", value=date_image)
    st.metric(label="Time", value=time_image)



# Get the class name
def get_class(blob):
    metadata = get_metadata(blob)
    return metadata['metadata']['class']

##Get the description of viruses from json file
with open('description.json') as json_file:
    data = json.load(json_file)


# Logo pour faire styler
logo = Image.open('../dashboard/logo.png')
with st.sidebar:

    #st.markdown("![Github](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)(https://github.com/deep-disease-detection)")
    #st.write("**About Us** [👉](https://github.com/deep-disease-detection)")
    link ='[**About Us**](https://github.com/deep-disease-detection)'
    st.markdown(link, unsafe_allow_html=True)

    st.image(logo, use_column_width=True)




st.title("Deep Disease Detector")
bucket = client.get_bucket(bucket_name)
# Get list of blobs in bucket
blobs = list(bucket.list_blobs())

# get the most recent image uploaded by date and time
most_recent_image_upload = max(blobs, key=lambda x: x.time_created)

## Create three columns
#col1, col2, col3 = st.columns(3)

## Description of virus
# with col1:
st.header("Classification")
st.write(f'**{get_class(most_recent_image_upload)}** {data[get_class(most_recent_image_upload)]}')

## Picture of virus, Date/Time/Class/Accuracy
# with col2:
st.header("Virus")
display_image_and_metadata(most_recent_image_upload)

## Tendencies of the day with barchart, average accuracy and most detected virus
# with col3:
st.header("Tendencies of the day")
chart_data = pd.DataFrame(
np.random.randn(20, 3),
columns=["a", "b", "c"])

st.bar_chart(chart_data)
st.write(f"**Average Probability**: {mean([0.90, 0.95])}")
st.write(f'**Most detected virus**: {max(set(["Ebola", "Ebola", "CCHP"]))}')


## Refresh the page every 5 seconds
# from streamlit_autorefresh import st_autorefresh
# count = st_autorefresh(interval=50000, limit=100, key="ddd")



# ### Reset button
with st.sidebar:
    if st.button("Refresh"):
        pyautogui.hotkey("ctrl","F5")
