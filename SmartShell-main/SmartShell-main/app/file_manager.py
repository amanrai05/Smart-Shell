import os

def list_files(folder_path):
    """
    Lists all files in the given folder, sorted by last modified date (newest first).
    """
    if not os.path.exists(folder_path):
        return []

    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Sort by modified time (latest first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    return files


def delete_file(folder_path, filename):
    """
    Deletes the given file from the specified folder.
    """
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False