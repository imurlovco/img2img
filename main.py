import os, importlib, subprocess, sys

required_packages = [("pillow", "PIL")]

def check_package():
    missing_packages = []
    for package_name, module_name in required_packages:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing_packages.append(package_name)

    if missing_packages:
        print("This program requires these packages:")
        print(missing_packages)
        print("Do you want to install? (y/n)")
        install_input = input("> ").strip().lower()
        
        if install_input == "y":
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("\nAll required packages are install.\nRestarting program.\n")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Shutting down...")
            sys.exit(0)

def convert(original_format, target_format):
    from PIL import Image

    print("\nEnter the directory path where your images are located.")
    directory_input = input("> ").strip().strip('"')
    original_format = original_format.lower().strip().replace(".", "")
    target_format = target_format.lower().strip().replace(".", "")

    if not os.path.isdir(directory_input):
        print(f"\nInvaild directory path: {directory_input}")
        sys.exit(0)

    quality = None
    if target_format == "webp":
        while True:
            print("\Enter WebP quality (0~100 / Default: 80)")
            quality_input = input("> ").strip()
            if quality_input == "":
                quality = 80
                break
            try:
                target_quality = int(quality_input)
                if 0 <= target_quality <= 100:
                    quality = target_quality
                    break
                else:
                    print("Please enter a number between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter an integer between 0 and 100.")

    output_directory = os.path.join(directory_input, f"converted_{target_format}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    converted_count = 0

    for filename in os.listdir(directory_input):
        if filename.lower().endswith(f".{original_format}"):
            input_path = os.path.join(directory_input, filename)
            output_filename = os.path.splitext(filename)[0] + f".{target_format}"
            output_path = os.path.join(output_directory, output_filename)

            try:
                with Image.open(input_path) as img:
                    if target_format in ["jpg", "jpeg"] and img.mode in ("RGBA", "LA"):
                        img = img.convert("RGB")
                    if target_format == "webp":
                        save_kwargs = {}
                        save_kwargs["quality"] = quality

                    img.save(output_path, target_format.upper(), **save_kwargs)
                    converted_count += 1
                    print(f"Converted: {filename} --> {output_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")
    
    if converted_count == 0:
        print(f"No .{original_format} images are found in {directory_input}")
    else:
        print(f"\n{converted_count} images are successfully converted.")
        print(f"Converted images are saved in {output_directory}")

def start():
    print("Image --> Image\n")
    print("Type original image format (jpg, jpeg, png, webp, avif)")
    original_format = input("> ")
    print("\nType target image format. (jpg, jpeg, png, webp, avif)")
    target_format = input("> ")
    convert(original_format, target_format)

if __name__ == "__main__":
    check_package()
    start()