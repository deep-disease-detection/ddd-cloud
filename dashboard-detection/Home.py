import streamlit as st
from google.cloud import storage
import datetime
from PIL import Image
import numpy as np
import pandas as pd
from statistics import mean
import json
import pyautogui

# Set up GCP storage client
client = storage.Client()
bucket_name = "images_detection_virus"
bucket = client.get_bucket(bucket_name)


def get_metadata(blob):
    metadata = {}
    metadata["name"] = blob.name
    metadata["metadata"] = blob.metadata

    time_image_epoch = metadata["metadata"]["time"]
    date_image = datetime.datetime.fromtimestamp(float(time_image_epoch)).strftime(
        "%Y-%m-%d"
    )
    time_image = datetime.datetime.fromtimestamp(float(time_image_epoch)).strftime(
        "%H:%M:%S"
    )

    return {
        "class": metadata["metadata"]["class"],
        "count": metadata["metadata"]["virus_count"],
        "date": date_image,
        "time": time_image,
    }


# Define function to display image and metadata
def get_image(blob):
    return blob.download_as_bytes()


##Get the description of viruses from json file
with open("description.json") as json_file:
    wikipedia_data = json.load(json_file)

### CUSTOM CSS
CSS = """
  .stApp {
    background-color: #111119;
  }
  h1, h2 {
    color: springgreen;
  }
  [data-testid="stMetricValue"] {
    font-size: 1.75rem;
  }
"""

st.write(f"<style>{CSS}</style>", unsafe_allow_html=True)

# Logo pour faire styler
logo = Image.open("../dashboard/logo.png")
with st.sidebar:
    # st.markdown("![Github](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)(https://github.com/deep-disease-detection)")
    # st.write("**About Us** [👉](https://github.com/deep-disease-detection)")
    link = "[**About Us**](https://github.com/deep-disease-detection)"
    st.markdown(link, unsafe_allow_html=True)

    # st.image(logo, use_column_width=True)


st.title("Deep Disease Detector")
bucket = client.get_bucket(bucket_name)
# Get list of blobs in bucket
blobs = list(bucket.list_blobs())

# get the most recent image uploaded by date and time
most_recent_image_upload = max(blobs, key=lambda x: x.time_created)

## Create three columns
col1, col2 = st.columns([3, 1])

## VIRUS INFORMATION
metadata = get_metadata(most_recent_image_upload)
with col1:
    st.header("Microscope Feed")
    img = get_image(most_recent_image_upload)
    st.image(img, use_column_width=True, output_format="PNG")


with col2:
    st.header("Classification")
    st.metric("Virus type", metadata["class"])
    st.metric("Virus count", metadata["count"])
    st.metric("Date", metadata["date"])
    st.metric("Date", metadata["time"])


st.header("Virus information")
st.write(f"**{metadata['class']}** {wikipedia_data[metadata['class']]}")


## Refresh the page every 5 seconds
# from streamlit_autorefresh import st_autorefresh
# count = st_autorefresh(interval=50000, limit=100, key="ddd")


# ### Reset button
with st.sidebar:
    if st.button("Refresh"):
        pyautogui.hotkey("ctrl", "F5")
