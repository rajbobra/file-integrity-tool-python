import argparse, os

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


def validate_args(args):
    if args.interval <= 0:
        print(f"ERROR: Interval '{args.interval}' must be a positive integer.")
        exit(1)

    path = os.path.expanduser(args.directory_path)
    if not os.path.exists(path):
        print(f"ERROR: The directory '{path}' does not exist.")
        exit(1)
    if not os.path.isdir(path):
        print(f"ERROR: '{path}' is not a directory.")
        exit(1)
    if not os.access(path, os.R_OK):
        print(f"ERROR: Permission denied for directory '{path}'.")
        exit(1)

    return path