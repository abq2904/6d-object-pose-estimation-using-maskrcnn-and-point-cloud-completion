# step07_pose_from_homography.py
# --------------------------------
# Automatic pose estimation from homography (category-aware)
# --------------------------------

import cv2
import numpy as np
from pathlib import Path
import json

# -------------------------------
# Configuration
# -------------------------------
CATEGORY = "Frenchs_yellow_mayonnaise_bottle"

FEATURES_DIR = Path("data/features") / CATEGORY
HOMOGRAPHY_DIR = FEATURES_DIR / "homography"
POSE_DIR = FEATURES_DIR / "pose"
POSE_DIR.mkdir(parents=True, exist_ok=True)

H_file = HOMOGRAPHY_DIR / "homography.npy"

if not H_file.exists():
    raise FileNotFoundError(f"Homography file not found: {H_file}")

# -------------------------------
# Load homography
# -------------------------------
H = np.load(H_file)

# -------------------------------
# Automatically build approximate camera matrix
# (since we don't have real calibration)
# -------------------------------

# Load one image just to get size
IMAGE_DIR = Path("data/detections") / CATEGORY / "cropped"
image_files = sorted(list(IMAGE_DIR.glob("*.jpg")))
if len(image_files) == 0:
    raise RuntimeError("No images found for estimating camera intrinsics.")

sample_img = cv2.imread(str(image_files[0]))
h, w = sample_img.shape[:2]

# Approximate intrinsics
focal_length = 0.8 * max(w, h)

K = np.array([
    [focal_length, 0, w / 2],
    [0, focal_length, h / 2],
    [0, 0, 1]
])

print("📷 Approximated Camera Matrix K:")
print(K)

# -------------------------------
# Decompose homography
# -------------------------------
num_solutions, Rs, Ts, normals = cv2.decomposeHomographyMat(H, K)

# -------------------------------
# Automatic pose selection
# -------------------------------
def choose_correct_pose(Rs, Ts):
    best_index = None
    max_positive_depth = -1

    # Assume planar square object
    pts_3d = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ], dtype=np.float32)

    for i, (R, t) in enumerate(zip(Rs, Ts)):
        X_cam = (R @ pts_3d.T + t).T
        positive_depth = np.sum(X_cam[:, 2] > 0)

        if positive_depth > max_positive_depth:
            max_positive_depth = positive_depth
            best_index = i

    return Rs[best_index], Ts[best_index]

R_correct, t_correct = choose_correct_pose(Rs, Ts)

print("\n✅ Automatic pose selection complete!")
print("Rotation:\n", R_correct)
print("Translation:\n", t_correct)

# -------------------------------
# Save Pose
# -------------------------------
pose_dict = {
    "camera_matrix": K.tolist(),
    "rotation": R_correct.tolist(),
    "translation": t_correct.flatten().tolist()
}

pose_file = POSE_DIR / "pose_result.json"

with open(pose_file, "w") as f:
    json.dump(pose_dict, f, indent=4)

print(f"\n✅ Pose saved to: {pose_file}")