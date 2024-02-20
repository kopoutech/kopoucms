import os

from PIL import Image


def convert_png_to_jpg(input_path, output_path):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Get a list of all files in the input directory
    files = os.listdir(input_path)

    for file in files:
        # Check if the file is a PNG
        if file.lower().endswith(".png"):
            # Open the PNG image
            png_image = Image.open(os.path.join(input_path, file))

            # Create a new white background image with the same size as the PNG image
            white_background = Image.new("RGBA", png_image.size, (255, 255, 255))

            # Convert the PNG image to RGB mode
            png_image = png_image.convert("RGB")

            # Paste the PNG image onto the white background
            white_background.paste(png_image, (0, 0), png_image)

            # Convert the image to JPG and save it
            jpg_image = white_background.convert("RGB")
            jpg_image.save(os.path.join(output_path, file.replace(".png", ".jpg")))

            # Close the images
            png_image.close()
            jpg_image.close()

    print("Conversion complete!")


# Example usage
input_path = "templates/static/client_logos"
output_path = "templates/static/client_logos"
convert_png_to_jpg(input_path, output_path)
