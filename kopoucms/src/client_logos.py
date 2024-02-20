import os
from posixpath import join as urljoin

import yaml
from PIL import Image, ImageOps

output_list = []

logos_yaml_raw = """
- name: 'Syracuse University'
  path: /static/client_logos_o/0.webp
- name: 'Wellesley'
  path: /static/client_logos_o/1.webp
- name: 'University of Bath'
  path: /static/client_logos_o/10.webp
- name: 'Arizona State University'
  path: /static/client_logos_o/11.webp
- name: 'University of California, Davis'
  path: /static/client_logos_o/12.webp
- name: 'The pennsylvania state university'
  path: /static/client_logos_o/13.webp
- name: 'Georgetown University'
  path: /static/client_logos_o/14.webp
- name: 'Skema Business School'
  path: /static/client_logos_o/15.webp
- name: 'Paris School of Business'
  path: /static/client_logos_o/16.webp
- name: 'Rennes School of Business'
  path: /static/client_logos_o/17.webp
- name: 'University of Surrey'
  path: /static/client_logos_o/18.webp
- name: 'Anglia Ruskin University'
  path: /static/client_logos_o/19.webp
- name: 'NYU'
  path: /static/client_logos_o/2.webp
- name: 'University college Birmingham'
  path: /static/client_logos_o/20.webp
- name: 'Brunel University London'
  path: /static/client_logos_o/21.webp
- name: 'American University of Sharjah'
  path: /static/client_logos_o/22.webp
- name: 'Amity University'
  path: /static/client_logos_o/23.webp
- name: 'Bryn Mawr College'
  path: /static/client_logos_o/24.webp
- name: 'Mount Holyoke College'
  path: /static/client_logos_o/25.webp
- name: 'Oxy Occidental College'
  path: /static/client_logos_o/26.webp
- name: 'Marquette University'
  path: /static/client_logos_o/27.webp
- name: 'Berlin International College'
  path: /static/client_logos_o/28.webp
- name: 'Rangsit University'
  path: /static/client_logos_o/29.webp
- name: 'Vassar College'
  path: /static/client_logos_o/3.webp
- name: 'Nuova Accademia di Belle Arti'
  path: /static/client_logos_o/30.webp
- name: 'Linstitut Superieur Des Arts Appliques'
  path: /static/client_logos_o/31.webp
- name: 'University of Rochester'
  path: /static/client_logos_o/32.webp
- name: 'One Brooklyn Health'
  path: /static/client_logos_o/33.webp
- name: 'Agnes Scott College'
  path: /static/client_logos_o/34.webp
- name: 'Wheaton College Massachusetts'
  path: /static/client_logos_o/35.webp
- name: 'Ursinus College'
  path: /static/client_logos_o/36.webp
- name: 'Krea University'
  path: /static/client_logos_o/37.webp
- name: 'Scripps College'
  path: /static/client_logos_o/38.webp
- name: 'ie University'
  path: /static/client_logos_o/39.webp
- name: 'University of Oregon'
  path: /static/client_logos_o/4.webp
- name: 'University of South Florida'
  path: /static/client_logos_o/40.webp
- name: 'University of Colorado Boulder'
  path: /static/client_logos_o/5.webp
- name: 'Harvard University'
  path: /static/client_logos_o/6.webp
- name: 'University of Cambridge'
  path: /static/client_logos_o/7.webp
- name: 'Imperial College London'
  path: /static/client_logos_o/8.webp
- name: 'The University of Manchester'
  path: /static/client_logos_o/9.webp
"""

logos_yaml = yaml.load(logos_yaml_raw, Loader=yaml.FullLoader)

names = {item["path"].split("/")[-1]: item["name"] for item in logos_yaml}

print(names)


def process_image(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            filename = filename.replace(" ", "_").lower()
            output_path = urljoin(output_dir, filename)
            try:
                trim_and_resize_image(input_path, output_path)
            except:
                print(f"Error processing {input_path}")


def trim_and_resize_image(input_path, output_path):
    """
    Trim whitespace from the input image, resize it to a height of 100 pixels,
    save the resulting image as a webp file, and add the image size to the output list.

    Args:
      input_path (str): The path to the input image file.
      output_path (str): The path to save the output image file.

    Returns:
      None
    """

    image = Image.open(input_path)
    image = trim_whitespace(image)
    image = resize_image(image, height=250)
    output_path = (
        os.path.splitext(output_path)[0] + ".webp"
    )  # Change the output filename extension to .webp
    image.save(output_path, "WEBP")  # Save the image as webp

    filename = output_path.split("/")[-1]
    output_list.append(
        {
            "path": output_path,
            "name": names.get(filename),
            "width": image.width,
            "height": image.height,
        }
    )


def trim_whitespace(image):
    """
    Trims the whitespace around an image.

    Args:
      image (PIL.Image.Image): The input image.

    Returns:
      PIL.Image.Image: The cropped image without whitespace.
    """
    if image.mode == "P":
        image_s = image.convert("RGBA")
        # background = Image.new("RGBA", image.size, (255, 255, 255))
        # image_s = Image.alpha_composite(background, image).convert("RGBA")
    else:
        image_s = image
    invert_im = ImageOps.invert(image_s)
    bbox = invert_im.getbbox()
    return image.crop(bbox)


def resize_image(image, height):
    width, original_height = image.size
    aspect_ratio = height / original_height
    new_width = int(width * aspect_ratio)
    return image.resize((new_width, height))


def resize_image_width(image, width):
    original_width, height = image.size
    aspect_ratio = width / original_width
    new_height = int(height * aspect_ratio)
    return image.resize((width, new_height))


# Example usage
input_directory = "templates/static/client_logos"
output_directory = "templates/static/client_logos_o"
process_image(input_directory, output_directory)


def display_output_list_as_yaml():
    yaml_output = yaml.dump(output_list)
    print(yaml_output)


display_output_list_as_yaml()
