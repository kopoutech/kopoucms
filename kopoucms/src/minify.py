import os

import rcssmin
import rjsmin


def combine_css_files(directory, output_file):
    css_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".css"):
                css_files[file] = os.path.join(root, file)

    with open(output_file, "w") as output:
        for filename, css_file in css_files.items():
            with open(css_file, "r") as file:
                data = rcssmin.cssmin(file.read())
                output.write(f"/* {filename} */ ")
                output.write(data)


def combine_js_files(directory, output_file):
    js_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                js_files[file] = os.path.join(root, file)

    with open(output_file, "w") as output:
        for filename, js_file in js_files.items():
            with open(js_file, "r") as file:
                data = rjsmin.jsmin(file.read())
                output.write(f"/* {filename} */\n")
                output.write(data + "\n")
