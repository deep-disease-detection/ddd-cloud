# Set project ID and region
# get project ID from env var
PROJECT_ID=$PROJECT_ID
# get region from env var
REGION=$REGION

# build the streamlit Docker image
docker build -t gcr.io/${PROJECT_ID}/streamlit-dashboard . --platform linux/amd64

# Push the Docker image to Container Registry
docker push gcr.io/${PROJECT_ID}/streamlit-dashboard:latest

# Deploy the Docker image to Cloud Run

gcloud run deploy streamlit-dashboard \
  --image gcr.io/${PROJECT_ID}/streamlit-dashboard:latest \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8501 \
  --memory '4Gi'
