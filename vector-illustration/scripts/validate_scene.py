import argparse
import json

from scene_utils import SceneError, inspect_scene


def main():
    parser = argparse.ArgumentParser(description="Validate a semantic scene plan or bound map without rendering.")
    parser.add_argument("input")
    parser.add_argument("--require-bound", action="store_true", help="Reject plans that have no completed SVG mapping")
    arguments = parser.parse_args()
    try:
        report = inspect_scene(arguments.input, require_bound=arguments.require_bound)[1]
        print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if report["valid"] else 1
    except (OSError, SceneError) as error:
        print(json.dumps({"valid": False, "svg_checked": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
