# step09_compute_grasp.py
# --------------------------------
# Load 3D model, apply 6D pose, compute simple grasp, visualize
# --------------------------------

import trimesh
import numpy as np
import cv2
import json
from pathlib import Path

# -------------------------------
# Config: Easily changeable paths
# -------------------------------
CATEGORY = "Frenchs_yellow_mayonnaise_bottle"

FEATURES_DIR = Path("data/features") / CATEGORY
POSE_FILE = FEATURES_DIR / "pose" / "pose_result.json"
IMAGE_DIR = Path("data/detections") / CATEGORY / "cropped"
OUTPUT_DIR = FEATURES_DIR / "grasp"
VISUAL_DIR = FEATURES_DIR / "visualization"

# Model file (replace with your .gltf/.obj if needed)
MODEL_FILE = Path("data/models/frenchs_mustard_bottle.gltf")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Load pose
# -------------------------------
with open(POSE_FILE, "r") as f:
    pose_data = json.load(f)

K = np.array(pose_data.get("camera_matrix", [[204.8, 0, 78.0],
                                             [0, 204.8, 128.0],
                                             [0, 0, 1]]))
R = np.array(pose_data["rotation"])
t = np.array(pose_data["translation"]).reshape(3, 1)

# -------------------------------
# Load 3D model
# -------------------------------
mesh = trimesh.load(MODEL_FILE, force='mesh')

# Transform mesh using pose
mesh.apply_transform(np.vstack([
    np.hstack([R, t]),
    [0, 0, 0, 1]
]))

# -------------------------------
# Compute simple grasp candidate
# -------------------------------
# Here: grasp at mid-height, centered along X-axis
bbox = mesh.bounds  # [[min_x,min_y,min_z], [max_x,max_y,max_z]]
center = (bbox[0] + bbox[1]) / 2
grasp_point = np.array([[center[0], center[1], center[2]]], dtype=np.float32)  # (1,3)

# Optional: grasp orientation = aligned with bottle axis (Z)
grasp_orientation = R  # same as pose rotation

# -------------------------------
# Project grasp point onto image
# -------------------------------
image_files = sorted(list(IMAGE_DIR.glob("*.jpg")))
img = cv2.imread(str(image_files[0]))
grasp_img_pts, _ = cv2.projectPoints(grasp_point, cv2.Rodrigues(R)[0], t, K, distCoeffs=None)
grasp_img_pts = grasp_img_pts.reshape(-1, 2).astype(int)
grasp_pixel = tuple(grasp_img_pts[0])

# -------------------------------
# Draw grasp point + axes
# -------------------------------
axis_length = 0.3
origin_3d = np.array([0,0,0])
axes_3d = np.float32([
    origin_3d,
    origin_3d + [axis_length, 0, 0],
    origin_3d + [0, axis_length, 0],
    origin_3d + [0, 0, axis_length]
])
projected_axes, _ = cv2.projectPoints(axes_3d, cv2.Rodrigues(R)[0], t, K, distCoeffs=None)
projected_axes = projected_axes.reshape(-1,2).astype(int)

origin = tuple(projected_axes[0])
x_axis = tuple(projected_axes[1])
y_axis = tuple(projected_axes[2])
z_axis = tuple(projected_axes[3])

# Draw axes
cv2.line(img, origin, x_axis, (0,0,255), 2)   # X-red
cv2.line(img, origin, y_axis, (0,255,0), 2)   # Y-green
cv2.line(img, origin, z_axis, (255,0,0), 2)   # Z-blue

# Draw grasp point (yellow circle)
cv2.circle(img, grasp_pixel, 6, (0,255,255), -1)

# -------------------------------
# Save visualization
# -------------------------------
output_img_file = VISUAL_DIR / "grasp_pose_visualization.jpg"
cv2.imwrite(str(output_img_file), img)
print("✅ Grasp + pose visualization saved to:", output_img_file)

# -------------------------------
# Save grasp configuration to JSON
# -------------------------------
grasp_config = {
    "grasp_point": grasp_point.flatten().tolist(),
    "grasp_orientation": grasp_orientation.tolist()
}

grasp_json_file = OUTPUT_DIR / "grasp_config.json"
with open(grasp_json_file, "w") as f:
    json.dump(grasp_config, f, indent=4)
print("✅ Grasp configuration saved to:", grasp_json_file)