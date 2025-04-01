import time
from args import *
from utilities import *

def detectChanges(files, file_hashes):
    changed, added = [], []
    deleted = [old_f for old_f in file_hashes if old_f not in files]

    for old_f in deleted:
        del file_hashes[old_f]

    for file in files:
        latest_hash = hash_file(file)
        if latest_hash:
            if file in file_hashes:
                if file_hashes[file] != latest_hash:
                    changed.append(file)
            else:
                added.append(file)
            file_hashes[file] = latest_hash

    return changed, added, deleted


def main():
    args = get_cli_args()
    path = validate_args(args)
    print("\nStarting the scan with the File Intergity tool")
    file_hashes, files = {}, get_files(path)
    startUp(files, file_hashes)
    try:
        while True:
            time.sleep(args.interval)
            files = get_files(path)
            log(detectChanges(files, file_hashes), args.interval)
    except KeyboardInterrupt:
        print("\nTerminating the scan with the File Intergity tool")


main()
