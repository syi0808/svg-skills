import json
import math
from pathlib import Path


MAX_BYTES = 5 * 1024 * 1024
MAX_ELEMENTS = 10000
MAX_DEPTH = 128


class SceneError(ValueError):
    pass


def finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SceneError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise SceneError(f"Nonfinite JSON number: {value}")


def load_scene(source):
    with Path(source).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise SceneError("Scene exceeds the 5 MiB limit")
    try:
        content = data.decode("utf-8-sig")
    except UnicodeError as error:
        raise SceneError("Scene must be UTF-8 encoded") from error
    try:
        scene = json.loads(content, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, RecursionError) as error:
        raise SceneError(f"Invalid scene JSON: {error}") from error
    stack = [(scene, 0)]
    while stack:
        value, depth = stack.pop()
        if isinstance(value, (dict, list)):
            if depth >= MAX_DEPTH:
                raise SceneError("Scene exceeds 128 JSON container levels")
            children = value.values() if isinstance(value, dict) else value
            stack.extend((child, depth + 1) for child in children)
        elif isinstance(value, float) and not math.isfinite(value):
            raise SceneError("Scene numbers must be finite")
    return scene


def validate_document(scene, require_bound=False):
    errors = []
    version = scene.get("version") if isinstance(scene, dict) else None
    report = {"valid": False, "svg_checked": False, "errors": errors, "warnings": []}
    if type(version) is not int or version not in (1, 2):
        errors.append("Scene must be an object with integer version 1 or 2")
        return report
    phase = "bound" if version == 1 else scene.get("phase")
    report["version"] = version
    if phase not in ("plan", "bound"):
        errors.append("Scene phase must be plan or bound")
    else:
        report["phase"] = phase
    if require_bound and phase != "bound":
        errors.append("Scene is not bound; add actual SVG tags and parents and set phase to bound")
    if not nonempty_string(scene.get("intent")):
        errors.append("Scene intent must be a nonempty string")
    canvas = scene.get("canvas")
    view_box = canvas.get("viewBox") if isinstance(canvas, dict) else None
    if not isinstance(view_box, list) or len(view_box) != 4 or not all(
        finite_number(value) for value in view_box
    ) or view_box[2] <= 0 or view_box[3] <= 0:
        errors.append("Scene canvas.viewBox needs four finite numbers and positive width/height")
    if version == 2:
        direction = scene.get("art_direction")
        if not isinstance(direction, dict) or not nonempty_string(direction.get("description")):
            errors.append("Scene art_direction.description must be a nonempty string")
        if isinstance(direction, dict) and any(
            not nonempty_string(key) or not nonempty_string(value)
            for key, value in direction.items()
        ):
            errors.append("Scene art_direction entries must have nonempty string keys and values")
        if isinstance(canvas, dict) and "background" in canvas and not nonempty_string(canvas["background"]):
            errors.append("Scene canvas.background must be a nonempty string")
        for field in ("constraints", "assumptions"):
            if field in scene and (
                not isinstance(scene[field], list) or not all(nonempty_string(value) for value in scene[field])
            ):
                errors.append(f"Scene {field} must be a list of nonempty strings")
        if "palette" in scene:
            palette = scene["palette"]
            if not isinstance(palette, dict) or any(
                not nonempty_string(key) or not nonempty_string(value) for key, value in palette.items()
            ):
                errors.append("Scene palette must map nonempty names to nonempty color descriptions")
    entries = scene.get("elements")
    if not isinstance(entries, list) or not entries or len(entries) > MAX_ELEMENTS:
        errors.append("Scene elements must contain between 1 and 10,000 entries")
        return report
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or not nonempty_string(entry.get("id")):
            errors.append("Every scene element needs a nonempty string ID")
            continue
        identifier = entry["id"]
        if identifier in seen:
            errors.append(f"Scene ID {identifier} is duplicated")
        if not nonempty_string(entry.get("role")):
            errors.append(f"Scene {identifier}: role must be a nonempty string")
        if version == 2 and "geometry_hint" in entry and not nonempty_string(entry["geometry_hint"]):
            errors.append(f"Scene {identifier}: geometry_hint must be a nonempty string")
        if phase == "bound":
            if not nonempty_string(entry.get("tag")):
                errors.append(f"Scene {identifier}: bound elements need a nonempty SVG tag")
            parent = entry.get("parent")
            if "parent" not in entry or (parent is not None and (not isinstance(parent, str) or parent not in seen)):
                errors.append(f"Scene {identifier}: parent must be null or a previously mapped ID")
        elif phase == "plan" and ("tag" in entry or "parent" in entry):
            errors.append(f"Scene {identifier}: leave tag and parent unset until the scene is bound")
        seen.add(identifier)
    report["elements"] = len(entries)
    report["valid"] = not errors
    return report


def inspect_scene(source, require_bound=False):
    scene = load_scene(source)
    report = validate_document(scene, require_bound=require_bound)
    report["input"] = str(Path(source).resolve())
    return scene, report
