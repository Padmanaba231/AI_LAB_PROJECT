import os
import shutil
import random

# Path folder dataset
source_folder = 'Images_Cleaned'

# Path untuk menyimpan dataset yang sudah di-split
destination_folder = 'Split'

# Rasio split (train, validation, test)
split_ratios = {
    'train': 0.8,
    'validation': 0.1,
    'test': 0.1
}

# Membuat folder tujuan jika belum ada
for split in split_ratios.keys():
    split_path = os.path.join(destination_folder, split)
    if not os.path.exists(split_path):
        os.makedirs(split_path)

# Fungsi untuk split dataset per folder kategori (A-Z)
def split_dataset():
    # Mendapatkan semua subfolder (A-Z) dalam folder sumber
    categories = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]

    for category in categories:
        category_path = os.path.join(source_folder, category)
        files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]

        # Mengacak urutan file
        random.shuffle(files)

        # Menghitung jumlah file untuk setiap split
        total_files = len(files)
        train_count = int(total_files * split_ratios['train'])
        validation_count = int(total_files * split_ratios['validation'])

        # Membagi file sesuai dengan rasio
        train_files = files[:train_count]
        validation_files = files[train_count:train_count + validation_count]
        test_files = files[train_count + validation_count:]

        # Membuat subfolder untuk kategori di setiap split
        for split in split_ratios.keys():
            split_category_path = os.path.join(destination_folder, split, category)
            if not os.path.exists(split_category_path):
                os.makedirs(split_category_path)

        # Memindahkan file ke folder masing-masing
        for file, split in zip([train_files, validation_files, test_files], split_ratios.keys()):
            for f in file:
                source_file_path = os.path.join(category_path, f)
                destination_file_path = os.path.join(destination_folder, split, category, f)
                shutil.copy(source_file_path, destination_file_path)

    print("Dataset berhasil di-split per kategori!")

# Memanggil fungsi split_dataset
split_dataset()
