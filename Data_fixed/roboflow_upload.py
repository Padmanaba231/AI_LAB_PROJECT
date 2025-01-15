from roboflow import Roboflow
import os

# Inisialisasi objek Roboflow dengan API Key Anda
rf = Roboflow(api_key="bFKH0E50XQlbmKsYAyNe")  # Ganti dengan API Key Anda

# Ambil proyek berdasarkan workspace dan nama proyek
workspace_id = "testing-gijbs"  # Ganti dengan workspace Anda
project_id = "labeling-sign-language-omqn0"      # Ganti dengan nama proyek Anda
project = rf.workspace(workspace_id).project(project_id)

# Path folder yang berisi gambar
folder_path = "./Data_fixed/split/val"  # Ganti dengan path folder Anda

# Fungsi untuk mengunggah semua file dari folder
def upload_images_from_folder(folder_path, batch_name="default_batch(valid)"):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Periksa apakah file adalah gambar
        if os.path.isfile(file_path) and file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"Mengunggah {file_name} ke batch '{batch_name}'...")
            try:
                project.upload(
                    image_path=file_path,
                    batch_name=batch_name,  # Anda bisa mengganti nama batch sesuai kebutuhan
                    split="valid",          # Split dataset (train/valid/test)
                    num_retry_uploads=3     # Jumlah retry jika gagal
                )
                print(f"Berhasil mengunggah: {file_name}")
            except Exception as e:
                print(f"Error saat mengunggah {file_name}: {e}")
        else:
            print(f"File {file_name} dilewati (bukan gambar).")

# Jalankan fungsi untuk mengunggah
upload_images_from_folder(folder_path)
