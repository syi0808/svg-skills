import argparse

from svg_utils import SVGError, emit, inspect_svg


def main():
    parser = argparse.ArgumentParser(description="Measure SVG structural complexity, not visual quality or bounds.")
    parser.add_argument("input")
    arguments = parser.parse_args()
    try:
        root, report = inspect_svg(arguments.input)
        if not report["valid"]:
            emit(report)
            return 1
        emit({"input": report["input"], "viewBox": report["viewBox"], **report["stats"], "warnings": report["warnings"]})
        return 0
    except (OSError, SVGError) as error:
        emit({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
