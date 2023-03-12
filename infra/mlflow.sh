# Set project ID and region
# get project ID from env var
PROJECT_ID=$PROJECT_ID
# get region from env var
REGION=$REGION

# Pull the mlflow Docker image
docker pull ghcr.io/mlflow/mlflow:latest --platform linux/amd64

# Tag the Docker image with the Cloud Run URL
docker tag ghcr.io/mlflow/mlflow:latest gcr.io/${PROJECT_ID}/mlflow-server

# Push the Docker image to Container Registry
docker push gcr.io/${PROJECT_ID}/mlflow-server

# Deploy the Docker image to Cloud Run

gcloud run deploy mlflow-server \
  --image burakince/mlflow \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 5000 \
  --memory '4Gi'

RAW_DATA_PATH='data/TEM virus dataset/context_virus_RAW'
PROCESS_DATA_PATH='data/process/TEM virus dataset/context_virus_1nm_256x256'
SAMPLE_PATH=data/process/TEM virus dataset/context_virus_1nm_256x256/sample_train/
AUGTRAIN_PATH='data/dataset-processed/TEM virus dataset/context_virus_1nm_256x256/augmented_train'
