# step08_visualize_pose.py
# --------------------------------
# Visualize 6D pose by projecting 3D coordinate axes on object images
# --------------------------------

import cv2
import numpy as np
import json
from pathlib import Path

# -------------------------------
# Configuration / Paths (change these easily)
# -------------------------------
CATEGORY = "Frenchs_yellow_mayonnaise_bottle"

# Base directories
BASE_DIR = Path("data/features") / CATEGORY
POSE_DIR = BASE_DIR / "pose"
POSE_FILE = POSE_DIR / "pose_result.json"

IMAGE_DIR = Path("data/detections") / CATEGORY / "cropped"
OUTPUT_DIR = BASE_DIR / "visualization"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Axis length in object units
AXIS_LENGTH = 0.05  # adjust if too small/large

# -------------------------------
# Load pose from JSON
# -------------------------------
with open(POSE_FILE, "r") as f:
    pose_data = json.load(f)

# Camera intrinsics (use stored or approximated)
K = np.array(pose_data.get("camera_matrix", [[204.8, 0, 78.],
                                             [0, 204.8, 128.],
                                             [0, 0, 1.0]]), dtype=np.float32)
R = np.array(pose_data["rotation"], dtype=np.float32)
t = np.array(pose_data["translation"], dtype=np.float32).reshape(3, 1)

# Convert rotation to Rodrigues vector
rvec, _ = cv2.Rodrigues(R)

# -------------------------------
# Load first image to visualize
# -------------------------------
image_files = sorted(list(IMAGE_DIR.glob("*.jpg")))
if len(image_files) == 0:
    raise RuntimeError(f"No images found in {IMAGE_DIR}")

img = cv2.imread(str(image_files[0]))
h, w = img.shape[:2]

# -------------------------------
# Define 3D coordinate axes
# Origin at base of the bottle
# X: red, Y: green, Z: blue
# -------------------------------
origin_3d = np.array([0.0, 0.0, 0.0], dtype=np.float32)

axes_3d = np.array([
    origin_3d,
    origin_3d + np.array([AXIS_LENGTH, 0.0, 0.0], dtype=np.float32),  # X axis
    origin_3d + np.array([0.0, AXIS_LENGTH, 0.0], dtype=np.float32),  # Y axis
    origin_3d + np.array([0.0, 0.0, AXIS_LENGTH], dtype=np.float32)   # Z axis
], dtype=np.float32)

# -------------------------------
# Project 3D axes to image
# -------------------------------
projected_points, _ = cv2.projectPoints(
    axes_3d,
    rvec,
    t,
    K,
    distCoeffs=None
)

projected_points = projected_points.reshape(-1, 2).astype(int)
origin_pt = tuple(projected_points[0])
x_pt = tuple(projected_points[1])
y_pt = tuple(projected_points[2])
z_pt = tuple(projected_points[3])

# -------------------------------
# Draw axes
# -------------------------------
cv2.line(img, origin_pt, x_pt, (0, 0, 255), 3)   # X axis - Red
cv2.line(img, origin_pt, y_pt, (0, 255, 0), 3)   # Y axis - Green
cv2.line(img, origin_pt, z_pt, (255, 0, 0), 3)   # Z axis - Blue

# Draw origin point
cv2.circle(img, origin_pt, 5, (0, 255, 255), -1)  # yellow dot at origin

# -------------------------------
# Save visualization
# -------------------------------
output_file = OUTPUT_DIR / "pose_visualization.jpg"
cv2.imwrite(str(output_file), img)
print("✅ Pose visualization saved to:", output_file)