# 01_download_images.py
from bing_image_downloader import downloader
import os
import shutil

# ----------- CONFIG -----------
KEYWORD = "French's yellow mayonnaise bottle" # or "water bottle"
LIMIT = 50                     # number of images to download
OUTPUT_DIR = "data/raw_images"
REPLACE_SPACES = True          # replace spaces with underscores
# -------------------------------

# Download images
downloader.download(
    KEYWORD,
    limit=LIMIT,
    output_dir=OUTPUT_DIR,
    adult_filter_off=True,
    force_replace=False,
    timeout=60
)

# ---- Post-processing: rename folder if contains spaces ----
original_folder = os.path.join(OUTPUT_DIR, KEYWORD)
if REPLACE_SPACES:
    new_folder = os.path.join(OUTPUT_DIR, KEYWORD.replace(" ", "_"))
    if os.path.exists(original_folder):
        if os.path.exists(new_folder):
            # Merge contents if target folder already exists
            for f in os.listdir(original_folder):
                shutil.move(os.path.join(original_folder, f), new_folder)
            os.rmdir(original_folder)
        else:
            os.rename(original_folder, new_folder)
    folder_name = new_folder
else:
    folder_name = original_folder

print(f"✅ Download complete! All images are in: {folder_name}")