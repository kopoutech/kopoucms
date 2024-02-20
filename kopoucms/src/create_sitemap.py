import xmltodict


def generate_sitemap(data):
    xml = xmltodict.unparse(data, pretty=True)
    return xml


# Example dictionary
sitemap_data = {
    "urlset": {"@xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9", "url": []}
}

links_parsed = {}


def add_url_to_sitemap(url, priority):
    global sitemap_data, links_parsed
    if url in links_parsed:
        return
    links_parsed[url] = True
    sitemap_data["urlset"]["url"].append({"loc": url, "priority": priority})


def save_sitemap(build_dir):
    global sitemap_data
    sitemap_xml = generate_sitemap(sitemap_data)
    with open(build_dir + "/sitemap.xml", "w") as f:
        f.write(sitemap_xml)


# sitemap_xml = generate_sitemap(sitemap_data)
# print(sitemap_xml)
