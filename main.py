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
    changed, added, deleted = ([] for i in range(3))

    for old_f in file_hashes:
        if old_f not in files:
            deleted.append(old_f)
    
    for old_f in deleted:
        del file_hashes[old_f]

    for file in files:
        latest_hash  = hash_file(file)
        if file in file_hashes:
            if file_hashes[file] != latest_hash:
                changed.append(file)
                file_hashes[file] = latest_hash
        else:
            added.append(file)
            file_hashes[file] = latest_hash

    return (changed, added, deleted)



def log(changes):
    if changes[0] == [] and changes[1] == [] and changes[2] == []:
        print('No changes in files detected')
    else:
        if changes[0]:
            print(f"ALERT: Following files have been changed in the last 30 seconds: {changes[0]}")
        if changes[1]:
            print(f"ALERT: Following files have been added in the last 30 seconds: {changes[1]}")
        if changes[2]:
            print(f"ALERT: Following files have been deleted in the last 30 seconds: {changes[2]}")



def main():
    directory = None # replace with directory you want to scan
    path = os.path.expanduser(directory)
    file_hashes = {}
    files = get_files(path)
    startUp(files, file_hashes)
    while True:
        time.sleep(30)
        files = get_files(path)
        log(detectChanges(files, file_hashes))

main()