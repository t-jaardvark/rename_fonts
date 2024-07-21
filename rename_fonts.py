import os
import sys
import shutil
from fontTools.ttLib import TTFont

def get_font_info(font_path):
    font = TTFont(font_path)
    name_record = font['name'].names
    family_name = style_name = version = None

    for record in name_record:
        if record.nameID == 1 and not family_name:
            family_name = record.string.decode(record.getEncoding())
        if record.nameID == 2 and not style_name:
            style_name = record.string.decode(record.getEncoding())
        if record.nameID == 5 and not version:
            version_str = record.string.decode(record.getEncoding())
            version = version_str.split(' ')[1] if ' ' in version_str else version_str

    if family_name and style_name and version:
        family_name = ''.join(family_name.title().split())
        style_name = ''.join(style_name.title().split())
        return f"{family_name}_{style_name}_{version}"
    return None

def rename_font_files(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.ttf', '.otf')):
            file_path = os.path.join(directory, filename)
            new_name = get_font_info(file_path)
            if new_name:
                new_file_path_temp = os.path.join(directory, f"{new_name}_tmp{os.path.splitext(filename)[1].lower()}")
                new_file_path_final = os.path.join(directory, f"{new_name}{os.path.splitext(filename)[1].lower()}")

                # Rename to temporary name to ensure case change
                os.rename(file_path, new_file_path_temp)
                # Rename to final name
                os.rename(new_file_path_temp, new_file_path_final)

                print(f"Renamed {filename} to {new_file_path_final}")

def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
        print(f"Copied directory {src} to {dest}")
    except Exception as e:
        print(f"Error copying directory: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        original_directory = sys.argv[1]
    else:
        original_directory = input("Please enter the directory containing the font files: ")

    if os.path.isdir(original_directory):
        base_name = os.path.basename(original_directory.rstrip('/'))
        new_directory = os.path.join(os.path.dirname(original_directory), f"{base_name}_rename")

        copy_directory(original_directory, new_directory)
        rename_font_files(new_directory)
    else:
        print("The provided directory does not exist.")
