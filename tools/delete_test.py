import os

def delete_test_folders(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            if folder.startswith("test"):
                folder_path = os.path.join(root, folder)
                print(f"Deleting folder: {folder_path}")
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        os.rmdir(item_path)
                os.rmdir(folder_path)

if __name__ == "__main__":
    target_directory = "data/AItest/"
    delete_test_folders(target_directory)
    print("Test folders and their contents deleted successfully.")
