# step06_estimate_homography.py
# --------------------------------
# Estimate homography between first two images of a category
# --------------------------------

from pathlib import Path
import cv2
import numpy as np
from step05_feature_matching import get_good_matches, load_images, detect_and_compute

# -------------------------------
# Input / Output Paths (easy to change)
# -------------------------------
CATEGORY = "Frenchs_yellow_mayonnaise_bottle"

# Where the cropped detections are stored
INPUT_DIR = Path("data/detections") / CATEGORY / "cropped"

# Features folder for homography and visualizations
FEATURES_DIR = Path("data/features") / CATEGORY
HOMOGRAPHY_DIR = FEATURES_DIR / "homography"
HOMOGRAPHY_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Load images (from directory)
# -------------------------------
img1, img2 = load_images(INPUT_DIR)

# -------------------------------
# Detect ORB keypoints & descriptors (per image)
# -------------------------------
kp1, des1 = detect_and_compute(img1)
kp2, des2 = detect_and_compute(img2)

# -------------------------------
# Match features
# -------------------------------
matches = get_good_matches(des1, des2)

if len(matches) < 4:
    raise RuntimeError("Not enough good matches to compute homography")

# -------------------------------
# Extract matched keypoints
# -------------------------------
pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])

# -------------------------------
# Compute Homography (RANSAC)
# -------------------------------
H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

if H is None:
    raise RuntimeError("Homography computation failed")

# -------------------------------
# Save homography matrix
# -------------------------------
H_file = HOMOGRAPHY_DIR / "homography.npy"
np.save(H_file, H)
print(f"✅ Homography matrix saved at: {H_file}")

# -------------------------------
# Save inlier matched keypoints
# -------------------------------
inlier_pts = np.array([kp2[m.trainIdx].pt for i, m in enumerate(matches) if mask[i]])
inlier_path = HOMOGRAPHY_DIR / "inlier_points.npy"
np.save(inlier_path, inlier_pts)
print("✅ Inlier points saved to:", inlier_path)

# -------------------------------
# Draw inlier matches only
# -------------------------------
matches_mask = mask.ravel().tolist()
draw_params = dict(
    matchColor=(0, 255, 0),
    singlePointColor=None,
    matchesMask=matches_mask,
    flags=2
)

matched_img = cv2.drawMatches(
    img1, kp1,
    img2, kp2,
    matches, None,
    **draw_params
)

# Save visualization
vis_file = HOMOGRAPHY_DIR / "homography_result.jpg"
cv2.imwrite(str(vis_file), matched_img)
print(f"✅ Homography visualization saved at: {vis_file}")