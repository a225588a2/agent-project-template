import os
import shutil
import zipfile

def archive_council():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    council_dir = os.path.join(project_root, ".council")
    archived_dir = os.path.join(project_root, "logs", "archived")
    
    if not os.path.exists(council_dir):
        print(f"[Info] Council directory {council_dir} does not exist. Nothing to archive.")
        return
        
    os.makedirs(archived_dir, exist_ok=True)
    archive_zip_path = os.path.join(archived_dir, "council-archive.zip")
    
    # Create zip archive of the .council directory
    print(f"[Info] Archiving {council_dir} to {archive_zip_path}...")
    with zipfile.ZipFile(archive_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(council_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, council_dir)
                zipf.write(file_path, arcname)
                
    # Clean up and delete the files inside .council/ directory (leave the directory itself)
    print(f"[Info] Cleaning up files in {council_dir}...")
    for filename in os.listdir(council_dir):
        file_path = os.path.join(council_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"[Warning] Failed to delete {file_path}: {e}")
            
    print("[Info] Council archive and cleanup completed successfully.")

if __name__ == "__main__":
    archive_council()
