import argparse
from PIL import Image
from . import __version__


def main():
    parser = argparse.ArgumentParser(prog="picdiredit", description="Small image utilities")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--info", metavar="PATH", help="Show image size info")
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


if __name__ == "__main__":
    main()
