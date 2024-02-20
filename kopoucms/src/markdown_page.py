import markdown
from bs4 import BeautifulSoup

ENABLED_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.codehilite",
    "markdown.extensions.meta",
]


def get_html_from_markdown_file(markdown_file):
    md = markdown.Markdown(extensions=ENABLED_EXTENSIONS)

    with open(markdown_file, "r") as f:
        content = f.read()
        html = md.convert(content)
        html = process_html(html)
        return html


def process_html(raw_html):
    # Take the raw html, parse it through bs4, add custom classes
    # and then return the html

    soup = BeautifulSoup(raw_html, "lxml")
    soup = add_class(
        soup,
        "h1",
        "pt-4 pb-8 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-4xl lg:text-5xl xl:text-6xl w-full text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-blue-500 to-purple-500 lg:inline  ",
    )
    soup = add_class(soup, "h2", "py-6 text-4xl font-bold text-gray-900")
    soup = add_class(soup, "h3", "pt-4 text-2xl text-gray-900 pb-6")
    soup = add_class(soup, "p", "pt-4 text-xl text-gray-900")
    soup = add_class(soup, "ul", "list-disc list-outside mt-4")
    soup = add_class(soup, "ol", "list-decimal mt-4")
    soup = add_class(soup, "li", "ml-4 text-xl pb-2 text-gray-900")
    soup = add_class(soup, "img", "md:max-w-2xl max-w-full justify-center object-cover")
    soup = add_class(
        soup, "a", "underline decoration-blue-500 text-blue-500 font-medium"
    )
    return soup.prettify()


def add_class(soup, tag, class_name):
    tags = soup.find_all(tag)
    for t in tags:
        if t is not None:
            # if "class" in t:
            print(t.get("class"), class_name)
            if t.get("class") is not None:
                class_name = class_name + " " + " ".join(t.get("class"))
            t["class"] = class_name
    return soup
