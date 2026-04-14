import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page

static_path = "./static"
public_path = "./public"
input_path = "content/index.md"
template_path = "template.html"
output_path = "public/index.html"


def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    copy_files_recursive(static_path, public_path)
    generate_page(input_path, template_path, output_path)


if __name__ == "__main__":
    main()
