import argparse
from pathlib import Path

from svg_utils import SVGError, emit, inspect_svg, serialize_svg, walk_elements, write_output


def main():
    parser = argparse.ArgumentParser(description="Normalize XML serialization without changing SVG geometry or text whitespace.")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--force", action="store_true", help="Replace an existing output, but never the input")
    arguments = parser.parse_args()
    try:
        root, report = inspect_svg(arguments.input)
        if not report["valid"]:
            emit(report)
            return 1
        for element, ancestors in walk_elements(root):
            attributes = sorted(element.attrib.items())
            element.attrib.clear()
            element.attrib.update(attributes)
        output = serialize_svg(root)
        write_output(output, arguments.output, [arguments.input], arguments.force)
        emit({
            "ok": True,
            "output": str(Path(arguments.output).resolve()),
            "input_bytes": report["stats"]["bytes"],
            "output_bytes": len(output),
            "geometry_changed": False,
            "visual_review": "not_performed",
        })
        return 0
    except (OSError, SVGError) as error:
        emit({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
