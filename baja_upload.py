import os
import shutil
from git import Repo

# --- CONFIG ---
folder_path = r"C:\Users\nickp\Downloads\bajaslideshow"
repo_path = r"C:\Users\nickp\portfoliov4"
dest_subfolder = "public/baja-slides"

# --- RENAME FILES ---
files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

renamed = []
for i, filename in enumerate(files, start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"bajaslide{i}{ext}"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)
    renamed.append(new_name)
    print(f"Renamed: {filename} → {new_name}")

# --- COPY TO REPO ---
dest_path = os.path.join(repo_path, dest_subfolder)
os.makedirs(dest_path, exist_ok=True)

for name in renamed:
    shutil.copy(os.path.join(folder_path, name), os.path.join(dest_path, name))

# --- GIT ADD, COMMIT, PUSH ---
repo = Repo(repo_path)
repo.git.add(dest_subfolder)
repo.index.commit("Add baja slideshow images")
origin = repo.remote(name="origin")
origin.push()

print("Done! Files pushed to portfoliov4.")