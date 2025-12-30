import argparse
from PIL import Image
from . import __version__
from .mover import move_files_from_csv


def main():
    parser = argparse.ArgumentParser(prog="picdiredit", description="Small image utilities and file mover")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--info", metavar="PATH", help="Show image size info")

    # CSV mover options
    parser.add_argument("--move-csv", metavar="CSV", help="CSV file with list of file paths to move (one column)")
    parser.add_argument("--dest", metavar="DIR", help="Destination directory for moved files")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without moving files")
    parser.add_argument("--preserve-structure", action="store_true", help="Preserve source directory structure under destination")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.info:
        try:
            with Image.open(args.info) as im:
                print(f"{args.info}: {im.format}, {im.size[0]}x{im.size[1]}")
        except FileNotFoundError:
            print(f"File not found: {args.info}")
        except Exception as e:
            print(f"Error reading image: {e}")

    # Handle CSV-based moving
    if args.move_csv:
        if not args.dest:
            print("Error: --dest is required when using --move-csv")
            return
        moved, errors = move_files_from_csv(args.move_csv, args.dest, preserve_structure=args.preserve_structure, dry_run=args.dry_run)
        print(f"Moved {moved} files")
        if errors:
            print("Errors:")
            for e in errors:
                print(" -", e)


if __name__ == "__main__":
    main()
