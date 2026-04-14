import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    static_input_path = "static"
    content_input_path = "content"
    output_path = "docs"
    template_path = "template.html"

    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    elif len(sys.argv) == 1:
        basepath = "/"
    else:
        raise ValueError("Usage: python main.py [basepath=/]")

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    copy_files_recursive(static_input_path, output_path)
    generate_pages_recursive(basepath, content_input_path, template_path, output_path)


if __name__ == "__main__":
    main()
