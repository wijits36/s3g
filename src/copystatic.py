import os
import shutil


def copy_files_recursive(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isdir(source_path):
            copy_files_recursive(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)
