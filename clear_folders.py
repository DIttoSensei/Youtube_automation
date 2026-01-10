import os
import shutil

# ================= CONFIG =================
# List the folders you want to empty here
FOLDERS_TO_CLEAN = [
    "output",
    "audio_segments",
    "images",
    # "images",  <-- Add more paths here if needed
]

# SAFETY SWITCH: Set this to False to actually delete files
DRY_RUN = True 
# ==========================================

def clean_folders():
    if DRY_RUN:
        print("--- 🛡️ DRY RUN MODE: No files will be deleted ---")
    else:
        print("--- ⚠️ WARNING: Deleting files for real ---")

    for folder in FOLDERS_TO_CLEAN:
        if not os.path.exists(folder):
            print(f"❓ Folder not found, skipping: {folder}")
            continue

        print(f"🧹 Cleaning folder: {folder}")

        # Loop through every file/folder inside the target folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            try:
                if DRY_RUN:
                    print(f"  [WOULD DELETE] {file_path}")
                else:
                    # Check if it's a file or a sub-folder
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path) # Delete file or link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path) # Delete sub-folder
                    print(f"  [DELETED] {file_path}")
                    
            except Exception as e:
                print(f"  ❌ Failed to delete {file_path}. Reason: {e}")

    if DRY_RUN:
        print("\n✨ Dry run complete. Set 'DRY_RUN = False' to execute.")
    else:
        print("\n✅ Cleanup finished.")

if __name__ == "__main__":
    clean_folders()