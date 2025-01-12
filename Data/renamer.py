import os

def rename_images(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

    image_files.sort()

    for file_name in image_files:
        old_path = os.path.join(folder_path, file_name)
        capitalized_name = file_name.capitalize()
        capitalized_path = os.path.join(folder_path, capitalized_name)
        if file_name != capitalized_name:
            os.rename(old_path, capitalized_path)
    
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    image_files.sort()

    counter = 1
    previous_prefix = None

    for file_name in image_files:
        name, ext = os.path.splitext(file_name)

        prefix = name[:2].upper()

        if prefix != previous_prefix:
            counter = 1
            previous_prefix = prefix

        new_name = f"{prefix}{counter:02d}{ext}"

        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)

        increment = 1
        while os.path.exists(new_path):
            new_name = f"{prefix}{counter:02d}_{increment}{ext}"
            new_path = os.path.join(folder_path, new_name)
            increment += 1

        os.rename(old_path, new_path)
        print(f"Renamed: {file_name} -> {new_name}")

        counter += 1

folder_path = "Images_Cleaned"

rename_images(folder_path)
