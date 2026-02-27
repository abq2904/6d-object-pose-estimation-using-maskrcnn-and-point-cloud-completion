from pathlib import Path
import cv2
import json
from ultralytics import YOLO

# -------------------------------
# Paths
# -------------------------------
INPUT_DIR = Path("data/processed_images/Frenchs_yellow_mayonnaise_bottle")
OUTPUT_DIR = Path("data/detections/Frenchs_yellow_mayonnaise_bottle")
CROPPED_DIR = OUTPUT_DIR / "cropped"
BBOX_JSON = OUTPUT_DIR / "bboxes.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CROPPED_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Load pretrained YOLOv8 model
# -------------------------------
model = YOLO("yolov8n.pt")  # lightweight & fast

print("🚀 Running detection...")

results = model(str(INPUT_DIR))

all_detections = {}

for result in results:
    image_path = Path(result.path)
    image = cv2.imread(str(image_path))

    boxes = result.boxes
    if boxes is None:
        continue

    bottle_boxes = []

    for box in boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name == "bottle":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            area = (x2 - x1) * (y2 - y1)
            bottle_boxes.append((area, x1, y1, x2, y2))

    if not bottle_boxes:
        continue

    # Select largest bottle
    _, x1, y1, x2, y2 = max(bottle_boxes, key=lambda x: x[0])

    # Add padding (15%)
    h, w = image.shape[:2]
    pad_x = int((x2 - x1) * 0.15)
    pad_y = int((y2 - y1) * 0.15)

    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(w, x2 + pad_x)
    y2 = min(h, y2 + pad_y)

    cropped = image[y1:y2, x1:x2]
    crop_path = CROPPED_DIR / image_path.name
    cv2.imwrite(str(crop_path), cropped)

    all_detections[image_path.name] = {
        "class": "bottle",
        "bbox_xyxy": [x1, y1, x2, y2]
    }

# Save bounding boxes
with open(BBOX_JSON, "w") as f:
    json.dump(all_detections, f, indent=4)

print("✅ Detection complete!")
print(f"Cropped images saved in: {CROPPED_DIR}")
print(f"Bounding boxes saved in: {BBOX_JSON}")