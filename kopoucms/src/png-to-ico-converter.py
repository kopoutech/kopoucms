
from PIL import Image

def png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path,format='ICO')

if __name__ == '__main__' : 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('png_path', help='PNG file path')
    parser.add_argument('ico_path', help='ICO file path' , default='favicon.ico')
    args = parser.parse_args()
    png_to_ico(args.png_path, args.ico_path)