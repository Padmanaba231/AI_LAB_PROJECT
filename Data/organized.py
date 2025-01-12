import os
import shutil

# Path folder tempat gambar berada
source_folder = 'Images_Cleaned'

# Path tujuan untuk pengelompokan gambar
destination_folder = 'Images_Cleaned/organized'

# Membuat folder tujuan jika belum ada
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Fungsi untuk mengelompokkan file
def organize_files():
    # Mendapatkan semua file dalam folder sumber
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    for file in files:
        # Memastikan file memiliki format yang valid (contoh: gambar)
        if file.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif')):
            # Mendapatkan awalan file (sebelum tanda '-')
            prefix = file.split('-')[0]

            # Membuat folder berdasarkan awalan jika belum ada
            target_folder = os.path.join(destination_folder, prefix)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # Memindahkan file ke folder yang sesuai
            source_file_path = os.path.join(source_folder, file)
            destination_file_path = os.path.join(target_folder, file)
            shutil.move(source_file_path, destination_file_path)

            print(f"Memindahkan {file} ke folder {prefix}")

# Memanggil fungsi organize_files
organize_files()

print("Pengelompokan selesai!")
