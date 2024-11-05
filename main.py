import os
import time
from PIL import Image
import sys
import threading
import argparse

def create_folders(input_dir, output_dir):
    folders = [input_dir, output_dir]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        else:
            print(f"Folder already exists: {folder}")

def display_directory_tree(directory, indent=""):
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        print(f"{indent}├── [Permission Denied]")
        return
    
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last_item = i == len(items) - 1
        connector = "└──" if is_last_item else "├──"

        if os.path.isdir(path):
            print(f"{indent}{connector} {item}/")
            display_directory_tree(path, indent + ("    " if is_last_item else "│   "))
        else:
            ext = os.path.splitext(item)[1]
            print(f"{indent}{connector} {item} ({ext})")

def convert_image_to_webp(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, "WEBP")

def create_output_structure(input_dir, output_dir):
    for root, dirs, _ in os.walk(input_dir):
        for dir_name in dirs:
            os.makedirs(os.path.join(output_dir, os.path.relpath(os.path.join(root, dir_name), input_dir)), exist_ok=True)

def start_conversion(input_dir, output_dir):
    create_output_structure(input_dir, output_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            input_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(input_file_path, input_dir)
            output_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + ".webp")
            
            print(f"Converting {file} to .webp...", end="")
            loader = threading.Thread(target=loading_animation)
            loader.start()
            
            try:
                convert_image_to_webp(input_file_path, output_file_path)
                print("\rConversion complete: ", output_file_path)
            except Exception as e:
                print(f"Failed to convert {file}: {e}")
            finally:
                loader.do_run = False
                loader.join()
    
    print("All images have been converted.")
    print("Press CTRL+C or ESC to exit.")

def loading_animation():
    for char in "|/-\\":
        if getattr(threading.currentThread(), "do_run", True):
            print(char, end="\r")
            time.sleep(0.1)

def monitor_input_directory(input_dir, output_dir):
    print("Monitoring 'Input' directory for changes...\n")
    previous_files = set()
    for root, _, files in os.walk(input_dir):
        previous_files.update(os.path.join(root, f) for f in files)

    display_directory_tree(input_dir)

    while True:
        time.sleep(1)
        current_files = set()
        for root, _, files in os.walk(input_dir):
            current_files.update(os.path.join(root, f) for f in files)

        if current_files != previous_files:
            print("\nChange detected! Refreshing directory tree...\n")
            display_directory_tree(input_dir)
            previous_files = current_files

            input("Press enter to convert to webp...")
            start_conversion(input_dir, output_dir)
            print("Waiting for further changes...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor directory and convert images to .webp format")
    parser.add_argument("--input-dir", default="Input", help="Directory to monitor for images")
    parser.add_argument("--output-dir", default="Output", help="Directory to save converted .webp images")
    parser.add_argument("--convert-now", action="store_true", help="Convert existing files immediately without monitoring")

    args = parser.parse_args()

    try:
        create_folders(args.input_dir, args.output_dir)
        if args.convert_now:
            start_conversion(args.input_dir, args.output_dir)
        else:
            monitor_input_directory(args.input_dir, args.output_dir)
    except (KeyboardInterrupt, SystemExit):
        print("\nExiting program gracefully.")
        sys.exit(0)
