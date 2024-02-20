import os

from PIL import Image


def convert_to_webp(input_dir, output_dir, size=None):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            # Open the image
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            # Resize the image if size is provided
            if size:
                image = image.resize(size)

            # Convert the image to WebP format
            output_filename = os.path.splitext(filename)[0].replace(" ", "-") + ".webp"
            output_path = os.path.join(output_dir, output_filename)
            image.save(output_path, "webp")

            # Close the image
            image.close()


INPUT_DIR = "templates/static/assets/images/landing"
OUTPUT_DIR = "templates/static/assets/images/webp/"
convert_to_webp(INPUT_DIR, OUTPUT_DIR)
