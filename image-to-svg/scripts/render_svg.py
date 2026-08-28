import argparse
import importlib.util
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from svg_utils import SVGError, absolute_pixels, emit, inspect_svg, serialize_svg, write_output


def render_dimensions(root, view_box, width):
    if not 1 <= width <= 8192:
        raise SVGError("Width must be in 1..8192 pixels")
    source_width = absolute_pixels(root.get("width", "0"))
    source_height = absolute_pixels(root.get("height", "0"))
    if not source_width or not source_height:
        source_width, source_height = view_box[2:]
    ratio = source_height / source_width
    scaled_height = width * ratio
    if not math.isfinite(scaled_height) or scaled_height > 8192:
        raise SVGError("Output exceeds the 8192-pixel edge limit")
    height = max(1, round(scaled_height))
    if width * height > 16000000:
        raise SVGError("Output exceeds the 16-million-pixel limit")
    return width, height


def renderer_command(backend, width, height):
    rsvg = shutil.which("rsvg-convert")
    if backend == "rsvg" or (backend == "auto" and rsvg):
        if not rsvg:
            raise SVGError("rsvg-convert is not installed or not on PATH")
        return "rsvg", [rsvg, "--format", "png", "--width", str(width), "--height", str(height)]
    if importlib.util.find_spec("cairosvg") is None:
        raise SVGError("No renderer found. Install rsvg-convert or CairoSVG in the selected Python environment; see references/tooling.md")
    return "cairosvg", [
        sys.executable, "-m", "cairosvg", "--format", "png",
        "--output-width", str(width), "--output-height", str(height), "-"
    ]


def main():
    parser = argparse.ArgumentParser(description="Preflight and render a local static SVG to PNG without fetching assets.")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--backend", choices=["auto", "rsvg", "cairosvg"], default="auto")
    parser.add_argument("--force", action="store_true", help="Replace an existing output, but never the input")
    arguments = parser.parse_args()
    try:
        root, report = inspect_svg(arguments.input)
        if not report["valid"]:
            emit(report)
            return 1
        width, height = render_dimensions(root, report["viewBox"], arguments.width)
        backend, command = renderer_command(arguments.backend, width, height)
        result = subprocess.run(command, input=serialize_svg(root), capture_output=True, timeout=30)
        if result.returncode:
            raise SVGError(f"{backend} failed: {result.stderr.decode('utf-8', errors='replace')[:2000].strip()}")
        output = result.stdout
        if len(output) < 24 or output[:8] != b"\x89PNG\r\n\x1a\n":
            raise SVGError("Renderer did not return a PNG")
        actual_dimensions = struct.unpack(">II", output[16:24])
        if actual_dimensions != (width, height):
            raise SVGError(f"Renderer returned {actual_dimensions}, expected {(width, height)}")
        write_output(output, arguments.output, [arguments.input], arguments.force)
        emit({
            "ok": True,
            "output": str(Path(arguments.output).resolve()),
            "backend": backend,
            "width": width,
            "height": height,
            "visual_review": "not_performed",
            "warnings": report["warnings"],
        })
        return 0
    except subprocess.TimeoutExpired:
        emit({"ok": False, "error": "Rendering timed out after 30 seconds"})
        return 2
    except (OSError, SVGError) as error:
        emit({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
