from src.create_page import render_website

TEMPLATE_DIR = "templates"
BUILD_DIR = "dist"

if __name__ == "__main__":
    render_website(TEMPLATE_DIR, BUILD_DIR)
