import streamlit as st
from google.cloud import storage
import time
import datetime
import io

# Set up GCP storage client
client = storage.Client()
bucket_name = "images_classification_virus"
bucket = client.get_bucket(bucket_name)

# Define function to read metadata of image file
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
    st.metric(label="Date", value=date_image)
    st.metric(label="Time", value=time_image)
    get_class = metadata['metadata']['class']
    st.metric(label="Class", value=get_class)


# Main loop
while True:
    # add title to the app
    st.title("Image Viewer")

    # Get list of blobs in bucket
    blobs = list(bucket.list_blobs())

    # Filter list to only include image files
    image_blobs = [blob for blob in blobs]
    print(image_blobs[0])
    # get the recent image in the bucket

    # Check if there are any image files in the bucket
    if image_blobs:
        # Display the first image file and its metadata
        # display only one image
        display_image_and_metadata(image_blobs[0])
        print("Image found in bucket")
    else:
        st.write("No image files found in bucket.")

    # Wait 10 seconds before checking the bucket again
    time.sleep(10)
