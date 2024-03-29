import streamlit as st
from google.cloud import storage
import datetime
import json

# Set up GCP storage client
client = storage.Client()
bucket_name = "images_classification_virus"
bucket = client.get_bucket(bucket_name)

# Set pages' names
pages = st.source_util.get_pages('Home.py')
new_page_names = {
  'Page_2': '🦠 Upload your Virus',
  'page_3': '📈 Analytics',
}
for key, page in pages.items():
  if page['page_name'] in new_page_names:
    page['page_name'] = new_page_names[page['page_name']]


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
        "proba" : metadata['metadata']['proba'],
        "class": metadata["metadata"]["class"],
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
  [data-testid="stMetricValue"] {
    font-size: 1.75rem;
  }
"""

st.write(f"<style>{CSS}</style>", unsafe_allow_html=True)

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

## Create two columns
col1, col2 = st.columns([4, 1])

## VIRUS INFORMATION
metadata = get_metadata(most_recent_image_upload)
with col1:
    st.header("Microscope Feed")
    img = get_image(most_recent_image_upload)
    st.image(img, width=300, output_format="PNG")


with col2:
    st.header("Classification")
    st.metric("Virus type", metadata["class"])
    st.metric("Proability", metadata['proba'] )
    st.metric("Date", metadata["date"])
    st.metric("Time", metadata["time"])


st.header("Virus information")
st.write(f"**{metadata['class']}** {wikipedia_data[metadata['class']]}")


## Refresh the page every 5 seconds
# from streamlit_autorefresh import st_autorefresh
# count = st_autorefresh(interval=50000, limit=100, key="ddd")


with st.sidebar:
    if st.button("Refresh"):
        st.experimental_rerun()

st.write("--")

## Cite the source
st.write(" (1) Source: _Wikipedia_")

with st.sidebar:
    st.image("QRcode.png")
