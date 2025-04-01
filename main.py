import hashlib, time, os

BUF_SIZE = 65536 # 64KB

def get_files(path):
    fileSet = set()
    for (root, dirs, files) in os.walk(path):
        for file in files:
            fileSet.add(os.path.join(root, file))
    return fileSet


def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def startUp(files, file_hashes):
    for file in files:
        file_hashes[file] = hash_file(file)



def detectChanges(files, file_hashes):
    changes = []
    for file in files:
        latest_hash  = hash_file(file)
        if file in file_hashes:
            if file_hashes[file] != latest_hash:
                changes.append(file)
                file_hashes[file] = latest_hash


    if changes == []:
        print('No changes in files detected')
    else:
        print(f"ALERT: Following files have been changed in the last 20 seconds: {changes}")


def main():
    directory = None # replace with directory you want to scan
    path = os.path.expanduser(directory)
    file_hashes = {}
    files = get_files(path)
    startUp(files, file_hashes)
    while True:
        time.sleep(20)
        files = get_files(path)
        detectChanges(files, file_hashes)

main()