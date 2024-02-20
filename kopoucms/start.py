import copy
import http.server
import os
import shutil
import socketserver
import threading

from catilo import catilo
from jinja2 import Environment, FileSystemLoader, Template

from src.create_page import render_website
from src.watch_and_render import watch_and_render

TEMPLATE_DIR = "templates"
BUILD_DIR = "dist"


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_DIR, **kwargs)


def create_http_server():
    port = 8000
    with socketserver.TCPServer(("", port), ServerHandler) as httpd:
        print(f"Server started at http://localhost:{port}")
        httpd.serve_forever()


def run_server_in_thread():
    server_thread = threading.Thread(target=create_http_server)
    server_thread.daemon = True
    server_thread.start()


if __name__ == "__main__":
    # create_dist_directory()
    # render_files(TEMPLATE_DIR)
    run_server_in_thread()
    watch_and_render(TEMPLATE_DIR, render_website, [TEMPLATE_DIR, BUILD_DIR])
