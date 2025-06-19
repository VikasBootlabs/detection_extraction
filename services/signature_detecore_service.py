import cv2
import numpy as np
from ultralytics import YOLO
from huggingface_hub import hf_hub_download,login
from dotenv import load_dotenv
import supervision as sv
import os
load_dotenv()
os.environ['HUGGINGFACE_API_TOKEN'] = os.getenv("HUGGINGFACE_API_TOKEN")
login(os.getenv("HUGGINGFACE_API_TOKEN"))

class SignatureDetectorService:
    def __init__(self):
        model_path = hf_hub_download(
            repo_id="tech4humans/yolov8s-signature-detector",
            filename="yolov8s.pt"
        )
        self.model = YOLO(model_path)
        self.box_annotator = sv.BoxAnnotator()

    def detect_signature(self, image_bytes: bytes) -> tuple[np.ndarray, list[dict]]:
        # Convert bytes to OpenCV image
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Run detection
        results = self.model(image)
        detections = sv.Detections.from_ultralytics(results[0])

        # Annotate image
        annotated_image = self.box_annotator.annotate(scene=image.copy(), detections=detections)

        # Collect detection results
        detected_boxes = []
        for xyxy, conf, cls_id in zip(detections.xyxy, detections.confidence, detections.class_id):
            detected_boxes.append({
                "box": xyxy.tolist(),
                "confidence": float(conf),
                "class_id": int(cls_id)
            })

        return annotated_image, detected_boxes