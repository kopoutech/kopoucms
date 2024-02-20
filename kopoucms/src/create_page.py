import copy
import os
import posixpath as path
import shutil
from datetime import datetime
from typing import List

import yaml
from catilo import catilo
from jinja2 import Environment, FileSystemLoader

from src import create_sitemap, markdown_page, minify, static

TEMPLATE_DIR = "templates"
BUILD_DIR = "dist"

VARS = catilo.VariableDirectory()
VARS.add_file_source("default", 10, "values.yml")
meta = {
    "published_time": datetime.now().strftime("%Y-%m-%d T%H:%M:%S"),
}
VARS.add_source("meta", 6, meta)


def get_methods():
    return {"strip": lambda x: x.replace(" ", "-").replace("&", "").lower()}


def render_elements(template_dir, values={}):
    env = Environment(loader=FileSystemLoader(template_dir))
    template_files = os.listdir(template_dir)
    elements = {}
    for template_file in template_files:
        template = env.get_template(template_file)
        rendered_content = template.render(values)
        template_file = template_file.replace(".html", "")
        elements[template_file] = rendered_content

    return elements


def create_dist_directory():
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
    subdirs = get_templates_subdirs(TEMPLATE_DIR + "/content")
    # print("dist: ", subdirs)
    for subdir in subdirs:
        os.makedirs(os.path.join(BUILD_DIR, subdir))


def check_or_fail(path):
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")


# a method that clears all files and folders in a directory
def clear_dist_directory():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)


def render_files(template_dir):
    env = Environment(loader=FileSystemLoader(template_dir))
    template_files = os.listdir(template_dir)
    for template_file in template_files:
        template = env.get_template(template_file)
        rendered_content = template.render(VARS.variables)
        output_file = path.join("dist", template_file)
        with open(output_file, "w") as f:
            f.write(rendered_content)


def save_page(output_file, rendered_content):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_content)


def copy_file(source, destination):
    shutil.copy(source, destination)


def get_templates_content(content_dir) -> List[str]:
    template_files = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            ppath = (
                path.join(root, file).replace("\\", "/").replace(content_dir + "/", "")
            )
            template_files.append(ppath)

    # print(content_dir, template_files)
    return template_files


def get_templates_subdirs(content_dir) -> List[str]:
    subdirs = []
    for root, dirs, files in os.walk(content_dir):
        for dir in dirs:
            ppath = (
                path.join(root, dir).replace("\\", "/").replace(content_dir + "/", "")
            )
            subdirs.append(ppath)

    # print(content_dir, subdirs)
    return subdirs


def get_values_from_file(filename, content_dir, default=""):
    values = {}
    values_file = path.join(content_dir, filename + ".values.yml")
    if check_if_file_exists(values_file):
        with open(values_file, "r") as f:
            values = yaml.safe_load(f)
    return values.get("title", default)


def get_articles(content_dir) -> List[str]:
    articles = []
    articles_dir = path.join(content_dir, "articles")
    for root, dirs, files in os.walk(articles_dir):
        for file in files:
            if file.endswith(".md"):
                filename = file.replace(".md", "")
                filename = filename.replace(" ", "-")
                title = get_values_from_file(filename, articles_dir, filename)
                articles.append({"slug": filename + ".html", "title": title})
    print(content_dir, articles)
    return articles


def check_if_file_exists(file):
    if not os.path.exists(file):
        return False
    return True


def check_and_updated_values(values, file, template_dir, ext):
    """
    Check if a values file exists for the given file and update the values dictionary.

    Args:
        values (dict): The dictionary of values to be updated.
        file (str): The file name.
        template_dir (str): The directory where the template files are located.
        ext (str): The file extension.

    Returns:
        dict: The updated values dictionary.
    """
    file = path.join(template_dir, file.replace(ext, ".values.yml"))

    print("Content file: ", file, ext)
    if check_if_file_exists(file):
        # print("Updating values from file: ", file)
        v = catilo.VariableDirectory(store_flat=False)
        v.add_file_source("default", 10, file)
        # print("Values: ", v.variables)
        values.update(v.variables)
        # print("Updated values: ", values)
    return values


def render_website(template_dir, build_dir):
    prepare_dist(template_dir)
    content_dir = path.join(template_dir, "content")
    template_files = get_templates_content(content_dir)

    articles = get_articles(content_dir)
    values = copy.deepcopy(VARS.variables)
    values["nav_articles"] = articles
    elements = render_elements(template_dir + "/elements", values)

    env = Environment(loader=FileSystemLoader(template_dir))

    static_files = static.copy_static_files(
        template_dir + "/static", build_dir + "/static"
    )

    for content_file in template_files:
        output_file = os.path.join(build_dir, content_file)
        base = "base.html"
        values = copy.deepcopy(VARS.variables)
        values["elements"] = elements
        values["static"] = static_files
        values["methods"] = get_methods()
        if content_file.endswith(".md"):
            values = check_and_updated_values(values, content_file, content_dir, ".md")
            rendered_content, output_file = handle_markdown_file(
                build_dir, content_dir, content_file
            )
            values["body"] = rendered_content
            base = "markdown.html"
            rendered_content = render_base(env, values, base)

        elif content_file.endswith(".html"):
            values = check_and_updated_values(
                values, content_file, content_dir, ".html"
            )
            rendered_html = generate_from_jinja(env, content_file, values)
            values["body"] = rendered_html

            rendered_content = render_base(env, values, base)

        elif content_file.endswith("amp.yml") or content_file.endswith("amp.yaml"):
            # Generate AMP format
            amp, output_file = generate_from_amp(content_file, build_dir)
            canonical_url = output_file.replace(".amp.html", ".html")
            base = "base.amp.html"
            values["amp"] = amp
            values["canonical_url"] = canonical_url
            values["amp_url"] = output_file
            rendered_content = []
            rendered_content.append((render_base(env, values, base), output_file))

            # Generate in HTML format
            base = "base.canonical.html"
            output_file = output_file.replace(".amp.html", ".html")
            rendered_content.append((render_base(env, values, base), output_file))

        else:
            continue
        url = path.join(
            "http://",
            values["site_url"],
            output_file.replace("dist\\", "").replace("dist/", ""),
        )
        create_sitemap.add_url_to_sitemap(url, values["priority"])
        if isinstance(rendered_content, list):
            for content in rendered_content:
                save_page(content[1], content[0])
        else:
            save_page(output_file, rendered_content)

    minify.combine_css_files(
        template_dir + "/styles", build_dir + "/" + VARS.get("css")
    )
    minify.combine_js_files(template_dir + "/js", build_dir + "/" + VARS.get("js"))
    copy_file(template_dir + "/robots.txt", BUILD_DIR)
    create_sitemap.save_sitemap(build_dir)


def handle_markdown_file(build_dir, content_dir, content_file):
    content_file_ab = path.join(content_dir, content_file)
    print("Generating HTML page from markdown ", content_dir, content_file_ab)
    rendered_content = markdown_page.get_html_from_markdown_file(content_file_ab)
    content_file = content_file.replace(" ", "-")
    content_file = content_file.replace(".md", ".html")
    content_file = content_file.lower()
    output_file = os.path.join(build_dir, content_file)
    return rendered_content, output_file


def load_amp(content_file_ab):
    with open(content_file_ab, "r") as f:
        values = yaml.safe_load(f)
    return values


def generate_from_amp(content_file, build_dir):
    content_file_ab = "templates/content/" + content_file
    print("Generating AMP page from", content_file, content_file_ab)
    page = load_amp(content_file_ab)
    output_file = content_file.replace(".yaml", ".html")
    output_file = output_file.replace(".yml", ".html")
    output_file = output_file.replace(" ", "-")
    output_file = path.join(build_dir, output_file)
    return page, output_file


def render_base(env, values, base_file="base.html"):
    base = env.get_template(base_file)
    rendered_base = base.render(values)
    return rendered_base


def generate_from_jinja(env, content_file, values):
    content_file_ab = "content/" + content_file
    # values = VARS.variables
    page = env.get_template(content_file_ab)
    # print(f"Values {content_file}: ", values.keys())
    rendered_content = page.render(values)
    # print(rendered_content)

    return rendered_content


def prepare_dist(template_dir):
    check_or_fail(os.path.join(template_dir, "base.html"))
    check_or_fail(os.path.join(template_dir, "content"))
    clear_dist_directory()
    create_dist_directory()
