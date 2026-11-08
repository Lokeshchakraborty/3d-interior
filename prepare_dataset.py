import os
import zipfile
from PIL import Image
from datasets import load_dataset

# =====================================================================
# CONFIGURATION
# =====================================================================
TRIGGER_WORD = "modern_interior"  # Trigger word to activate your custom style in prompts
DATASET_NAME = "MohamedAli77/interior-rooms"
NUM_IMAGES = 50
TARGET_SIZE = (1024, 1024)
OUTPUT_DIR = "interior_lora_dataset"
ZIP_FILENAME = "interior_lora_dataset.zip"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print(f"Preparing {NUM_IMAGES} high-res interior design training pairs...")
print(f"Trigger word: '{TRIGGER_WORD}'")
print(f"Target size: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")
print("=" * 60)

# =====================================================================
# 1. STREAM & DOWNLOAD 50 HIGH-QUALITY ROOMS
# =====================================================================
print("\n[1/3] Streaming from MohamedAli77/interior-rooms...")
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)

count = 0
for idx, item in enumerate(dataset):
    if count >= NUM_IMAGES:
        break

    try:
        # 'full_room' contains the fully furnished, designed room
        img = item["full_room"].convert("RGB")
        raw_caption = item.get("caption", "Modern luxurious interior room design")

        # Smart center-crop to square
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        img_cropped = img.crop((left, top, right, bottom)).resize(TARGET_SIZE, Image.Resampling.LANCZOS)

        # File paths
        base_name = f"interior_{count + 1:03d}"
        img_path = os.path.join(OUTPUT_DIR, f"{base_name}.jpg")
        txt_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")

        # Save 1024x1024 JPEG
        img_cropped.save(img_path, "JPEG", quality=95)

        # Prepend trigger word to caption
        final_caption = f"{TRIGGER_WORD}, {raw_caption.strip()}"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(final_caption)

        count += 1
        print(f" -> [{count:02d}/{NUM_IMAGES}] Saved: {base_name}.jpg | '{final_caption[:60]}...'")

    except Exception as e:
        print(f"Skipping image {idx} due to error: {e}")
        continue

print(f"\n[2/3] Successfully saved {count} pairs into '{OUTPUT_DIR}'!")

# =====================================================================
# 2. ZIP THE DATASET FOR 1-CLICK UPLOAD TO KAGGLE / AUTOTRAIN
# =====================================================================
print(f"\n[3/3] Compressing into '{ZIP_FILENAME}'...")
with zipfile.ZipFile(ZIP_FILENAME, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=file)

print("\n" + "=" * 60)
print("DATASET PREPARATION COMPLETE!")
print(f"Dataset location: {os.path.abspath(OUTPUT_DIR)}")
print(f"Ready-to-upload Zip: {os.path.abspath(ZIP_FILENAME)}")
print("=" * 60)
