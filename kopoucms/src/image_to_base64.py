import base64
import os

import yaml
from PIL import Image


# Function to resize an image to 128x128 pixels
def resize_image(image_path):
    image = Image.open(image_path)
    resized_image = image.resize((128, 128))
    return resized_image


# Function to convert an image to base64 representation
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_data = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_data


# Function to process the directory for PNG files
def process_directory(directory):
    image_files = [file for file in os.listdir(directory) if file.endswith(".png")]
    image_data = {}
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        resized_image = resize_image(image_path)
        resized_image.save(image_path + ".resized.png")
        base64_data = image_to_base64(image_path + ".resized.png")
        image_data[image_file] = base64_data
    return image_data


# Main function
def main():
    directory = (
        "templates/static/assets/images/icons"  # Replace with the actual directory path
    )
    image_data = process_directory(directory)
    output_file = "templates/static/assets/images/icons/icons.yml"  # Replace with the desired output file path
    with open(output_file, "w") as file:
        yaml.dump(image_data, file)


if __name__ == "__main__":
    main()
