import os
import shutil

# ================= CONFIG =================
# 1. Folders to empty completely
FOLDERS_TO_CLEAN = [
    "output",
    "audio_segments",
    "images",
]

# 2. Specific files in the current folder to delete
FILES_TO_DELETE = [
    "content.json",
    "prompts.json",
    "script_output.txt",
]

# SAFETY SWITCH: Set this to False to actually delete files
DRY_RUN = False 
# ==========================================

def clean_tech_mage():
    # 🛡️ PROTECT THE SYSTEM: Files that should NEVER be deleted
    PROTECTED = [os.path.basename(__file__), "client_secrets.json", "token.pickle"]

    print(f"--- {'🛡️ DRY RUN' if DRY_RUN else '⚠️ REAL DELETE'} MODE ---")

    # Part 1: Clean Folders
    for folder in FOLDERS_TO_CLEAN:
        if os.path.exists(folder):
            print(f"🧹 Emptying folder: {folder}")
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                delete_item(file_path)

    # Part 2: Clean Specific Files in current dir
    print("🎯 Cleaning specific targeted files...")
    for filename in FILES_TO_DELETE:
        if filename in PROTECTED:
            print(f"   🚫 Safety block: Refusing to delete {filename}")
            continue
            
        if os.path.exists(filename):
            delete_item(filename)
        else:
            print(f"   ❓ File not found: {filename}")

def delete_item(path):
    try:
        if DRY_RUN:
            print(f"   [WOULD DELETE] {path}")
        else:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            print(f"   [DELETED] {path}")
    except Exception as e:
        print(f"   ❌ Error on {path}: {e}")

if __name__ == "__main__":
    clean_tech_mage()
    print("\n✅ Cleanup finished.")