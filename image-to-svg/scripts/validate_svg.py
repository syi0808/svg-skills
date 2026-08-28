import argparse

from svg_utils import SVGError, check_scene, emit, inspect_svg


def main():
    parser = argparse.ArgumentParser(description="Check a portable static-vector SVG and optional semantic scene.")
    parser.add_argument("input")
    parser.add_argument("--scene", help="Optional bound scene JSON (version 1 or version 2) to check against the SVG")
    arguments = parser.parse_args()
    try:
        root, report = inspect_svg(arguments.input)
        if arguments.scene:
            check_scene(arguments.scene, root, report)
        emit(report)
        return 0 if report["valid"] else 1
    except (OSError, SVGError) as error:
        emit({"valid": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
