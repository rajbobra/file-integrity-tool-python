import hashlib, time, os, argparse

BUF_SIZE = 65536  # 64KB


def get_files(path):
    fileSet = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            fileSet.add(os.path.join(root, file))
    return fileSet


def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
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
        latest_hash = hash_file(file)
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
        print(f"No changes in files detected in the last {args.interval} seconds")
    else:
        type = ["changed", "added", "deleted"]
        for i in range(0, 3):
            if changes[i]:
                print(f"ALERT: Following files have been {type[i]} in the last {args.interval} seconds: {changes[i]}")


def get_cli_args():
    parser = argparse.ArgumentParser(
        description="Arguments for File Integrity CLI tool"
    )
    parser.add_argument(
        "interval",
        type=int,
        help="Pass in the interval you want to run this program at",
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="Pass in the directory you want to scan for continuous integrity checks",
    )
    return parser.parse_args()


def main():
    path = os.path.expanduser(args.directory_path)
    file_hashes = {}
    files = get_files(path)
    startUp(files, file_hashes)
    while True:
        time.sleep(args.interval)
        files = get_files(path)
        log(detectChanges(files, file_hashes))


args = get_cli_args()
main()