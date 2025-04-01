import os, hashlib

BUF_SIZE = 65536  # 64KB

def get_files(path):
    fileSet = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            fileSet.add(os.path.join(root, file))
    return fileSet


def hash_file(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while data := f.read(BUF_SIZE):
                sha256.update(data)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError) as e:
        print(f"WARNING: Unable to read {file_path} - {e}")
        return None


def log(changes, interval):
    if not any(changes):
        print(f"No changes in files detected in the last {interval} seconds")
    else:
        type = ["changed", "added", "deleted"]
        for i in range(0, 3):
            if changes[i]:
                print(f"ALERT: Following files have been {type[i]} in the last {interval} seconds: {changes[i]}")


def startUp(files, file_hashes):
    for file in files:
        file_hashes[file] = hash_file(file)