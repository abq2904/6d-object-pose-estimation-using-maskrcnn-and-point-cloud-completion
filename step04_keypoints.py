from pathlib import Path
import cv2
import json

# -------------------------------
# Paths
# -------------------------------
INPUT_DIR = Path("data/detections/Frenchs_yellow_mayonnaise_bottle/cropped")
OUTPUT_DIR = Path("data/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURES_JSON = OUTPUT_DIR / "orb_features.json"

# -------------------------------
# ORB Detector
# -------------------------------
orb = cv2.ORB_create(nfeatures=1000)

all_features = {}

print("🔍 Extracting ORB features...")

for image_path in INPUT_DIR.glob("*.jpg"):
    image = cv2.imread(str(image_path))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    keypoints, descriptors = orb.detectAndCompute(gray, None)

    if descriptors is None:
        continue

    # Save keypoints locations
    kp_data = []
    for kp in keypoints:
        kp_data.append({
            "pt": kp.pt,
            "angle": kp.angle,
            "size": kp.size
        })

    all_features[image_path.name] = {
        "num_keypoints": len(keypoints),
        "keypoints": kp_data
    }

    # Draw visualization
    vis = cv2.drawKeypoints(image, keypoints, None, color=(0,255,0))
    cv2.imwrite(str(OUTPUT_DIR / f"kp_{image_path.name}"), vis)

with open(FEATURES_JSON, "w") as f:
    json.dump(all_features, f, indent=4)

print("✅ ORB feature extraction complete!")
print(f"Saved in: {OUTPUT_DIR}")