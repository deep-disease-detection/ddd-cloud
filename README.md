# ddd-cloud
This repository contains cloud infrastructure and code for DDD project

## ⚙️ Code and repositories
- **cloud_functions**: Code deployed on GCP Cloud Functions to process the images coming from Pub/Sub, make the predictions and store the results on buckets and a PostgreSQL database.
- **dashboard**: Code for streamlit dashboard used for classification
- **dashboard-detection**: Code for streamlit dashboard used for object detection
- **infra**: Various shell code scripts (eg. dockerise dashboards and deploy on GCP)
