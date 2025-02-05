import os
import shutil
from pathlib import Path
from PIL import Image  # Import PIL for dynamic image size detection

# Define paths to the FGVC Aircraft dataset files
base_path = "/Users/gordysun/Downloads/fgvc-aircraft-2013b/"
images_dir = os.path.join(base_path, "data/images")
box_annotations_file = os.path.join(base_path, "data/images_box.txt")
train_split_file = os.path.join(base_path, "data/images_variant_train.txt")
val_split_file = os.path.join(base_path, "data/images_variant_val.txt")

# Define output directories
output_base = "yolo_dataset"
train_images_output = os.path.join(output_base, "images/train")
val_images_output = os.path.join(output_base, "images/val")
train_labels_output = os.path.join(output_base, "labels/train")
val_labels_output = os.path.join(output_base, "labels/val")

# Create required directories
os.makedirs(train_images_output, exist_ok=True)
os.makedirs(val_images_output, exist_ok=True)
os.makedirs(train_labels_output, exist_ok=True)
os.makedirs(val_labels_output, exist_ok=True)

# Parse bounding box annotations
def load_annotations(annotation_file):
    annotations = {}
    with open(annotation_file, "r") as file:
        for line in file:
            parts = line.strip().split()
            image_name = parts[0].split("/")[-1]  # Only use the filename
            xmin, ymin, xmax, ymax = map(int, parts[1:])
            annotations[image_name] = (xmin, ymin, xmax, ymax)
    return annotations

bbox_data = load_annotations(box_annotations_file)

# Function to clip bounding boxes to valid ranges
def clip_bounding_box(x_center, y_center, width, height):
    width = min(width, 1.0)
    height = min(height, 1.0)
    x_center = min(max(x_center, width / 2), 1 - width / 2)
    y_center = min(max(y_center, height / 2), 1 - height / 2)
    return x_center, y_center, width, height

# Function to process a split (train or validation)
def process_split(split_file, images_output, labels_output):
    with open(split_file, "r") as file:
        for line in file:
            image_name = line.strip().split()[0]
            if image_name not in bbox_data:
                continue

            # Get bounding box details
            xmin, ymin, xmax, ymax = bbox_data[image_name]

            # Get image dimensions dynamically
            src_image_path = os.path.join(images_dir, f"{image_name}.jpg")
            if not os.path.exists(src_image_path):
                continue

            image = Image.open(src_image_path)
            img_width, img_height = image.size

            # Convert bounding box to YOLO format
            x_center = ((xmin + xmax) / 2) / img_width
            y_center = ((ymin + ymax) / 2) / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            # Clip bounding box to valid ranges
            x_center, y_center, width, height = clip_bounding_box(x_center, y_center, width, height)

            # Skip invalid bounding boxes
            if width <= 0 or height <= 0:
                print(f"Skipping invalid bounding box for {image_name}")
                continue

            # Create YOLO annotation file
            label_file = os.path.splitext(image_name)[0] + ".txt"
            label_path = os.path.join(labels_output, label_file)
            with open(label_path, "w") as label:
                label.write(f"0 {x_center} {y_center} {width} {height}\n")  # Class ID is 0

            # Copy the image to the output directory
            dst_image_path = os.path.join(images_output, f"{image_name}.jpg")
            shutil.copy(src_image_path, dst_image_path)

# Process training and validation splits
process_split(train_split_file, train_images_output, train_labels_output)
process_split(val_split_file, val_images_output, val_labels_output)

# Create YOLO dataset configuration file
dataset_yaml_path = os.path.join(output_base, "dataset.yaml")
with open(dataset_yaml_path, "w") as yaml_file:
    yaml_file.write(f"""
train: {train_images_output}
val: {val_images_output}
nc: 1
names: ['airplane']
""")

print("Dataset preparation completed!")