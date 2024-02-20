import os
from posixpath import join as urljoin

heading = "Why Study Abroad"

path = "templates/content/articles/"

filename = heading.lower().replace(" ", "-")

markdown_file = urljoin(path, filename + ".md")
values_file = urljoin(path, filename + ".values.yml")


def create_article(heading, markdown_file, values_file):
    if not os.path.exists(markdown_file):
        with open(markdown_file, "w") as f:
            f.write(
                f"""
![{heading}](image_url)
# {heading}
  """
            )
    else:
        print("Markdown File already exists")

    if not os.path.exists(values_file):
        with open(values_file, "w") as f:
            f.write(
                f"""
title: "{heading}"
description: ""
social_image: ""
  """
            )
    else:
        print("Values File already exists")


create_article(heading, markdown_file, values_file)
