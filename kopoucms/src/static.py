import os
import posixpath as path
import shutil
from typing import List


def get_templates_content(content_dir) -> List[str]:
    template_files = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            ppath = (
                path.join(root, file).replace("\\", "/").replace(content_dir + "/", "")
            )
            template_files.append(ppath)

    print(content_dir, template_files)
    return template_files


def copy_static_files(source_dir, destination_dir):
    """
    Copy static files from source directory to destination directory.
    """
    static_files = {}
    print("Copying static files...", source_dir, destination_dir)
    try:
        # Create destination directory if it doesn't exist
        # if not os.path.exists(destination_dir):
        #     os.makedirs(destination_dir)

        # Copy files from source directory to destination directory
        shutil.copytree(source_dir, destination_dir)
        print("Static files copied successfully!")
    except Exception as e:
        print(f"An error occurred while copying static files: {str(e)}")

    return static_files
