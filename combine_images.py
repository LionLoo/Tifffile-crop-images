import os
import re
import numpy as np
import tifffile as tiff


# Input Paths
nisnet_output = r"C:\Users\kvs62\OneDrive\Desktop\epoch\testing_result_zebrafish_embryo3" #place the location of your NisNET output
original_split_file = r"C:\Users\kvs62\Downloads\epoch" #place the location of your original crop
combined_path = r"\Users\kvs62\Downloads\TifResult" #output location
image_name = "epoch" #name your image output

def number_items_in_file(path):
    try:
        items = os.listdir(path)
        return len(items)
    except FileNotFoundError:
        print("No path found in items_in_file")
        return None

def get_directories(path):
    try:
        items = os.listdir(path)
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        return directories
    except FileNotFoundError:
        print("No path found in get_directories")

def sort_nisnet_directories(path):
    try:
        return int(path.split('_')[0])
    except ValueError:
        print("Value Error in sort_nisnet_directories")
        return -1

def load_images(image_paths):
    images = [tiff.imread(path) for path in image_paths]
    for i, image in enumerate(images):
        images[i] = image.transpose(1, 2, 0, 3)
    return images

def extract_coordinates(filename):
    match = re.findall(r'\d+', filename)
    if match:
        # Assuming the order is (x, y, z)
        coordinates = tuple(map(int, match[-3:]))
        return coordinates
    else:
        return None

# Create output directory if not exists
if not os.path.exists(combined_path):
    os.makedirs(combined_path)

# Get number of items in the original split file
num_images = number_items_in_file(original_split_file)

# Get directories in nisnet output
nisnet_directories = get_directories(nisnet_output)

# Get sorted nisnet directories based on sorting function
sorted_nisnet = sorted(nisnet_directories, key=sort_nisnet_directories)

# Get paths of segmented CC2 files
sorted_seg_CC2 = [os.path.join(nisnet_output, path, "seg_CC2.tif") for path in sorted_nisnet]

# Load images
tiff_nisnet = load_images(sorted_seg_CC2)

# Print the size of each image
for idx, image in enumerate(tiff_nisnet):
    print(f"Image {idx + 1} size: {image.shape}")

# Extract coordinates from split files
coordinates_list = [extract_coordinates(filename) for filename in os.listdir(original_split_file)]


# Function to calculate output shape
def calculate_output_shape(images, coordinates):
    max_dims = [0, 0, 0, 0]
    for image, (x, y, z) in zip(images, coordinates):
        dx, dy, dz, t = image.shape
        max_dims = np.maximum(max_dims, [x + dx, y + dy, z + dz, t])
    return tuple(max_dims)

# Function to combine images
def combine_images(images, coordinates):
    output_shape = calculate_output_shape(images, coordinates)
    output_volume = np.zeros(output_shape, dtype=np.uint8)

    for image, (x, y, z) in zip(images, coordinates):
        dx, dy, dz, t = image.shape
        output_volume[x:x + dx, y:y + dy, z:z + dz, :] = image

    return output_volume

# Combine images
combined_volume = combine_images(tiff_nisnet, coordinates_list)

# Save the combined volume as tiff file
tiff.imwrite(os.path.join(combined_path, f"{image_name}.tif"), combined_volume)

print("Images combined and saved successfully.")
