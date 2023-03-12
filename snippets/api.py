from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
from PIL import Image
import random
import json
from fastapi import FastAPI
from pydantic import BaseModel
import base64

app = FastAPI()

class MyData(BaseModel):
    image: str

class DetectionRequest(BaseModel):
    image: UploadFile

class DetectionResponse(BaseModel):
    object_class: str
    confidence: float

@app.post("/detect", response_model=list[DetectionResponse])
async def detect(request: DetectionRequest):
    # Read the uploaded image into memory
    contents = await request.image.read()
    image = Image.open(io.BytesIO(contents))

    # Simulate a detection by generating a random object class and confidence score
    detections = []
    for _ in range(random.randint(1, 5)):
        object_class = random.choice(["car", "person", "dog"])
        confidence = random.uniform(0.5, 0.9)
        detections.append(DetectionResponse(object_class=object_class, confidence=confidence))

    return detections

@app.post("/predict")
def predict(request):
    # Read the uploaded image into memory
    contents = request.image
    image = base64.b64decode(contents.encode("utf-8"))

    # Simulate a detection by generating a random object class and confidence score
    detections = []
    for _ in range(random.randint(1, 5)):
        object_class = random.choice(["car", "person", "dog"])
        confidence = random.uniform(0.5, 0.9)
        detections.append(DetectionResponse(object_class=object_class, confidence=confidence))

    return detections


@app.get("/")
def root():
    return {"message": "Hello World"}
