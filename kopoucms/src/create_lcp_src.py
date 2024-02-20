import os

from PIL import Image


def resize_image(image_path, output_path, device_sizes):
    """
    Resize the image to the specified device sizes while maintaining the aspect ratio,
    and save the resized images.

    Args:
      image_path (str): The path to the input image file.
      output_path (str): The path to the output directory where the resized images will be saved.
      device_sizes (dict): A dictionary containing the device names as keys and the desired sizes as values.

    Returns:
      None
    """
    with Image.open(image_path) as img:
        original_width, original_height = img.size
        for device, size in device_sizes.items():
            device_width, device_height = get_resized_dimensions(
                original_width, original_height, size
            )
            img_resized = img.resize((device_width, device_height))
            image_path = os.path.splitext(image_path)[0].replace(" ", "-")
            output_filename = (
                f"{os.path.splitext(os.path.basename(image_path))[0]}_{device}.webp"
            )
            output_filepath = os.path.join(output_path, output_filename)
            img_resized.save(output_filepath, "WEBP")


def get_resized_dimensions(original_width, original_height, device_size):
    """
    Calculate the resized dimensions while maintaining the aspect ratio.

    Args:
      original_width (int): The original width of the image.
      original_height (int): The original height of the image.
      device_size (tuple): The desired size of the device (width, height).

    Returns:
      tuple: The resized dimensions (width, height).
    """
    device_width, device_height = device_size
    aspect_ratio = original_width / original_height
    if device_width / device_height > aspect_ratio:
        device_width = int(device_height * aspect_ratio)
    else:
        device_height = int(device_width / aspect_ratio)
    return device_width, device_height


def generate_html_code(images_dir, output_dir, device_sizes):
    """
    Generate HTML code for displaying images with responsive srcset attribute.

    Args:
      images_dir (str): The directory path where the images are located.
      output_dir (str): The directory path where the resized images will be saved.
      device_sizes (dict): A dictionary containing device names as keys and
         corresponding image sizes as values.

    Returns:
      str: The generated HTML code.

    """
    html_code = ""
    for filename in os.listdir(images_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(images_dir, filename)
            resize_image(image_path, output_dir, device_sizes)
            filename = os.path.splitext(filename)[0].replace(" ", "-")
            alt_text = filename
            srcset = ""
            for device, size in device_sizes.items():
                device_width, device_height = size
                output_filename = f"{os.path.splitext(filename)[0]}_{device}.webp"
                output_filepath = os.path.join(output_dir, output_filename)
                srcset += f"{output_filepath} {device_width}w, "
            srcset = srcset.rstrip(", ")
            html_code += (
                f'<img src="{output_filepath}" alt="{alt_text}" srcset="{srcset}">\n'
            )

            print(output_dir + filename)
    return html_code


# Example usage
input_dir = "templates/static/assets/images/landing/img/"
output_dir = "templates/static/assets/images/webp/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
device_sizes = {"large": (1200, 800), "medium": (800, 600), "small": (400, 300)}
html_code = generate_html_code(input_dir, output_dir, device_sizes)
print(html_code)
