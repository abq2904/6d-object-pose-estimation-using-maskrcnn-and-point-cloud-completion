from pathlib import Path
from PIL import Image

# -------------------------------
# Input / Output Paths (easily changeable)
# -------------------------------
RAW_IMAGES_DIR = Path("data/raw_images/French's_yellow_mayonnaise_bottle")  # Root folder with downloaded images
# Automatically create a safe folder name: replace spaces and apostrophes
safe_folder_name = RAW_IMAGES_DIR.name.replace(" ", "_").replace("'", "")
PROCESSED_IMAGES_DIR = Path("data/processed_images") / safe_folder_name

TARGET_WIDTH = 256
TARGET_HEIGHT = 256
TARGET_MODE = "RGB"  # Ensure all images are in RGB

# Create output folder if it doesn't exist
PROCESSED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Preprocessing loop
# -------------------------------
# Collect all image paths in the input folder (only jpg/png)
image_paths = list(RAW_IMAGES_DIR.glob("*.jpg")) + list(RAW_IMAGES_DIR.glob("*.png"))

print(f"Found {len(image_paths)} images to process in '{RAW_IMAGES_DIR}'...")

for img_path in image_paths:
    with Image.open(img_path) as img:
        # Convert mode if necessary
        if img.mode != TARGET_MODE:
            img = img.convert(TARGET_MODE)
        
        # Resize while keeping aspect ratio, add black bars if needed
        img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        new_img = Image.new(TARGET_MODE, (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0))
        paste_x = (TARGET_WIDTH - img.width) // 2
        paste_y = (TARGET_HEIGHT - img.height) // 2
        new_img.paste(img, (paste_x, paste_y))
        
        # Save to output folder
        out_path = PROCESSED_IMAGES_DIR / img_path.name
        new_img.save(out_path)

print(f"✅ Preprocessing complete! Processed {len(image_paths)} images.")
print(f"All images are saved in: {PROCESSED_IMAGES_DIR}")