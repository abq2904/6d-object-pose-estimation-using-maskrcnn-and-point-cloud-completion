from pathlib import Path
import cv2
import numpy as np


# -------------------------------
# Load images
# -------------------------------
def load_images(input_dir):
    images = list(Path(input_dir).glob("*.jpg"))

    if len(images) < 2:
        raise Exception("Not enough images for matching.")

    img1 = cv2.imread(str(images[0]))
    img2 = cv2.imread(str(images[1]))

    return img1, img2


# -------------------------------
# Detect and compute features
# -------------------------------
def detect_and_compute(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=1500)
    kp, des = orb.detectAndCompute(gray, None)
    return kp, des


# -------------------------------
# Match features
# -------------------------------
def get_good_matches(des1, des2, top_k=50):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x: x.distance)

    print(f"Total matches found: {len(matches)}")

    return matches[:top_k]


# -------------------------------
# Optional standalone execution
# -------------------------------
if __name__ == "__main__":

    INPUT_DIR = "data/detections/Frenchs_yellow_mayonnaise_bottle/cropped"

    img1, img2 = load_images(INPUT_DIR)
    kp1, des1, kp2, des2 = detect_and_compute(img1, img2)
    good_matches = get_good_matches(des1, des2)

    match_img = cv2.drawMatches(
        img1, kp1,
        img2, kp2,
        good_matches, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    OUTPUT_PATH = Path("data/features/matching_result.jpg")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(OUTPUT_PATH), match_img)

    print("✅ Matching visualization saved at:", OUTPUT_PATH)