import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

static_path = "static"
public_path = "public"
content_path = "content"
template_path = "template.html"


def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    copy_files_recursive(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)


if __name__ == "__main__":
    main()
