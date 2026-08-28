import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = ("references/scene-model.md", "scripts/scene_utils.py", "scripts/validate_scene.py")
TARGETS = ("vector-illustration", "image-to-svg")


def main():
    parser = argparse.ArgumentParser(description="Check or refresh the standalone skills' bundled scene contract.")
    parser.add_argument("--write", action="store_true", help="Copy canonical files from illustration-plan into production skills")
    arguments = parser.parse_args()
    different = []
    for relative in FILES:
        source = ROOT / "illustration-plan" / relative
        for skill in TARGETS:
            destination = ROOT / skill / relative
            if arguments.write:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            elif not destination.exists() or destination.read_bytes() != source.read_bytes():
                different.append(str(destination.relative_to(ROOT)))
    if different:
        print("Scene contract copies differ: " + ", ".join(different))
        print("Update illustration-plan first, then run scripts/sync_scene_contract.py --write")
        return 1
    print("Scene contract copies are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
