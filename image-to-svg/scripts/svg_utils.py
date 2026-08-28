import graphlib
import json
import math
import os
import re
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from scene_utils import SceneError, inspect_scene


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"
MAX_BYTES = 5 * 1024 * 1024
NUMBER = r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?"
NUMBER_RE = re.compile(NUMBER)
LENGTH_RE = re.compile(rf"({NUMBER})(px|pt|pc|mm|cm|in|em|ex|%)?")
DRAWING_TAGS = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "use"}
RESOURCE_TAGS = {"defs", "clipPath", "mask", "pattern", "marker", "symbol"}
ALLOWED_TAGS = DRAWING_TAGS | RESOURCE_TAGS | {
    "svg", "g", "title", "desc", "tspan", "textPath", "linearGradient", "radialGradient", "stop"
}
ALLOWED_ATTRS = set("""
    id class version width height viewBox preserveAspectRatio transform
    x y x1 y1 x2 y2 cx cy r rx ry d points dx dy rotate
    fill fill-rule fill-opacity stroke stroke-width stroke-linecap stroke-linejoin
    stroke-miterlimit stroke-dasharray stroke-dashoffset stroke-opacity opacity color
    display visibility vector-effect clip-path clip-rule mask mask-type
    font-family font-size font-style font-weight letter-spacing word-spacing
    text-anchor dominant-baseline alignment-baseline baseline-shift textLength lengthAdjust
    startOffset method spacing gradientUnits gradientTransform spreadMethod fx fy fr
    stop-color stop-opacity offset clipPathUnits maskUnits maskContentUnits
    patternUnits patternContentUnits patternTransform marker-start marker-mid marker-end
    markerWidth markerHeight markerUnits refX refY orient href
    role aria-label aria-labelledby aria-describedby aria-hidden focusable
""".split())
LENGTH_ATTRS = set("""
    x y x1 y1 x2 y2 cx cy r rx ry width height fx fy fr stroke-width
    stroke-dashoffset font-size markerWidth markerHeight textLength
""".split())
NONNEGATIVE_ATTRS = {
    "r", "rx", "ry", "width", "height", "fr", "stroke-width", "font-size",
    "markerWidth", "markerHeight", "textLength"
}
PAINT_REFS = {"fill", "stroke", "clip-path", "mask", "marker-start", "marker-mid", "marker-end"}
PATH_ARITY = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}
TRANSFORM_ARITY = {
    "matrix": {6}, "translate": {1, 2}, "scale": {1, 2}, "rotate": {1, 3},
    "skewX": {1}, "skewY": {1}
}


class SVGError(ValueError):
    pass


class StaticTreeBuilder(ET.TreeBuilder):
    def doctype(self, name, public_id, system_id):
        raise SVGError("DTDs and entity declarations are not supported")

    def pi(self, target, text):
        raise SVGError("XML processing instructions are not supported")


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))


def read_utf8(source):
    with Path(source).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise SVGError("Input exceeds the 5 MiB limit")
    try:
        return data.decode("utf-8-sig"), len(data)
    except UnicodeError as error:
        raise SVGError("Input must be UTF-8 encoded") from error


def local_name(name):
    return name.rsplit("}", 1)[-1]


def number_list(value):
    if re.sub(NUMBER, "", value).strip(" \t\r\n,"):
        raise SVGError(f"Invalid number list: {value[:80]!r}")
    numbers = [float(match.group()) for match in NUMBER_RE.finditer(value)]
    if not all(math.isfinite(number) for number in numbers):
        raise SVGError("Numbers must be finite")
    return numbers


def length_value(value):
    match = LENGTH_RE.fullmatch(value.strip())
    if not match or not math.isfinite(float(match.group(1))):
        raise SVGError(f"Invalid finite length: {value[:80]!r}")
    return float(match.group(1)), match.group(2) or ""


def absolute_pixels(value):
    number, unit = length_value(value)
    factors = {"": 1, "px": 1, "pt": 96 / 72, "pc": 16, "in": 96, "cm": 96 / 2.54, "mm": 96 / 25.4}
    if unit not in factors:
        return None
    pixels = number * factors[unit]
    if not math.isfinite(pixels):
        raise SVGError("Absolute length exceeds the finite pixel range")
    return pixels


def path_segments(data):
    position = 0
    command = None
    segments = 0
    while position < len(data):
        while position < len(data) and data[position] in " \t\r\n,":
            position += 1
        if position == len(data):
            break
        if data[position].isalpha():
            command = data[position]
            position += 1
            if segments == 0 and command.upper() != "M":
                raise SVGError("Path must start with moveto")
            if command.upper() == "Z":
                segments += 1
                command = None
                continue
            if command.upper() not in PATH_ARITY:
                raise SVGError("Unsupported path command")
        if command is None:
            raise SVGError("Path numbers need a command")
        for argument_index in range(PATH_ARITY[command.upper()]):
            while position < len(data) and data[position] in " \t\r\n,":
                position += 1
            if command.upper() == "A" and argument_index in {3, 4}:
                if position == len(data) or data[position] not in "01":
                    raise SVGError("Arc flags must be 0 or 1")
                position += 1
                continue
            match = NUMBER_RE.match(data, position)
            if match is None:
                raise SVGError(f"Path command {command} has missing or invalid arguments")
            number = float(match.group())
            if not math.isfinite(number):
                raise SVGError("Path coordinates must be finite")
            if command.upper() == "A" and argument_index < 2 and number < 0:
                raise SVGError("Arc radii cannot be negative")
            position = match.end()
        segments += 1
        if command == "M":
            command = "L"
        elif command == "m":
            command = "l"
    if segments == 0:
        raise SVGError("Path data must not be empty")
    return segments


def check_transform(value):
    position = 0
    for match in re.finditer(r"([A-Za-z]+)\s*\(([^()]*)\)", value):
        if value[position:match.start()].strip(" \t\r\n,"):
            raise SVGError("Invalid transform syntax")
        arguments = number_list(match.group(2))
        if len(arguments) not in TRANSFORM_ARITY.get(match.group(1), set()):
            raise SVGError("Invalid transform name or argument count")
        position = match.end()
    if position == 0 or value[position:].strip(" \t\r\n,"):
        raise SVGError("Invalid transform syntax")


def walk_elements(root):
    stack = [(root, ())]
    count = 0
    while stack:
        element, ancestors = stack.pop()
        if not isinstance(element.tag, str):
            continue
        count += 1
        if count > 10000 or len(ancestors) >= 128:
            raise SVGError("SVG exceeds 10,000 elements or 128 levels of nesting")
        yield element, ancestors
        stack.extend((child, ancestors + (element,)) for child in reversed(element))


def inspect_svg(source):
    content, byte_count = read_utf8(source)
    try:
        root = ET.fromstring(content, parser=ET.XMLParser(target=StaticTreeBuilder(insert_comments=True)))
    except ET.ParseError as error:
        raise SVGError(f"Invalid XML: {error}") from error
    errors = []
    warnings = []
    if root.tag != f"{{{SVG_NS}}}svg":
        errors.append("Root must be svg in the http://www.w3.org/2000/svg namespace")
    try:
        view_box = number_list(root.get("viewBox", ""))
        if len(view_box) != 4 or view_box[2] <= 0 or view_box[3] <= 0:
            raise SVGError("viewBox needs four finite numbers and positive width/height")
    except SVGError as error:
        errors.append(str(error))
        view_box = None
    nodes = list(walk_elements(root))
    counts = Counter(local_name(element.tag) for element, ancestors in nodes)
    identifiers = {}
    references = []
    accessibility_refs = []
    segment_count = 0
    for element, ancestors in nodes:
        tag = local_name(element.tag)
        identifier = element.get("id")
        label = f"{tag}#{identifier}" if identifier else tag
        if element.tag != f"{{{SVG_NS}}}{tag}" or tag not in ALLOWED_TAGS:
            errors.append(f"{label}: unsupported element")
        if tag == "svg" and element is not root:
            errors.append(f"{label}: nested SVG viewports are outside this profile")
        if identifier is not None:
            if not identifier or re.search(r"\s", identifier):
                errors.append(f"{label}: ID must be nonempty and contain no whitespace")
            if identifier in identifiers:
                errors.append(f"{label}: duplicate ID")
            identifiers[identifier] = element
        in_resource = any(local_name(ancestor.tag) in RESOURCE_TAGS for ancestor in ancestors)
        if tag in DRAWING_TAGS | {"g"} and not identifier and not in_resource:
            warnings.append(f"{label}: add a stable semantic ID for editing")
        owners = [ancestor.get("id") for ancestor in ancestors + (element,) if ancestor.get("id")]
        for attribute, value in element.attrib.items():
            name = local_name(attribute)
            if attribute.startswith("{") and attribute not in {
                f"{{{XLINK_NS}}}href", f"{{{XML_NS}}}space", f"{{{XML_NS}}}lang"
            }:
                errors.append(f"{label}: unsupported namespaced attribute {name}")
                continue
            if attribute in {f"{{{XML_NS}}}space", f"{{{XML_NS}}}lang"}:
                continue
            if name not in ALLOWED_ATTRS and not name.startswith("data-"):
                errors.append(f"{label}: unsupported attribute {name}")
                continue
            try:
                if name in LENGTH_ATTRS:
                    number, unit = length_value(value)
                    if name in NONNEGATIVE_ATTRS and number < 0:
                        raise SVGError(f"{name} cannot be negative")
                    if element is root and name in {"width", "height"} and number <= 0:
                        raise SVGError(f"Root {name} must be positive")
                if name in {"opacity", "fill-opacity", "stroke-opacity", "stop-opacity", "offset"}:
                    number, unit = length_value(value)
                    if unit not in {"", "%"} or not 0 <= number <= (100 if unit == "%" else 1):
                        raise SVGError(f"{name} must be in 0..1 or 0..100%")
                if name in {"transform", "gradientTransform", "patternTransform"}:
                    check_transform(value)
                if name in {"dx", "dy", "rotate"}:
                    if not number_list(value):
                        raise SVGError(f"{name} must contain numbers")
                if name == "stroke-dasharray" and value != "none":
                    dash_values = number_list(value)
                    if not dash_values or any(number < 0 for number in dash_values):
                        raise SVGError("stroke-dasharray needs nonnegative numbers")
                if name == "href":
                    if not value.startswith("#") or len(value) < 2:
                        raise SVGError("Only local #id references are allowed")
                    references.append((label, value[1:], owners))
                if name in PAINT_REFS:
                    if "\\" in value or "/*" in value:
                        raise SVGError("CSS escapes/comments are outside the static profile")
                    matches = list(re.finditer(r"url\s*\(([^)]*)\)", value, re.IGNORECASE))
                    if re.search(r"url\s*\(", value, re.IGNORECASE) and not matches:
                        raise SVGError("Malformed URL reference")
                    for match in matches:
                        target = match.group(1).strip().strip("\"'")
                        if not target.startswith("#") or len(target) < 2:
                            raise SVGError("Only local url(#id) references are allowed")
                        references.append((label, target[1:], owners))
                if name in {"aria-labelledby", "aria-describedby"}:
                    accessibility_refs.extend((label, target) for target in value.split())
            except SVGError as error:
                errors.append(f"{label}: {error}")
        try:
            if tag == "path":
                segment_count += path_segments(element.get("d", ""))
            elif tag in {"polygon", "polyline"}:
                points = number_list(element.get("points", ""))
                minimum = 6 if tag == "polygon" else 4
                if len(points) < minimum or len(points) % 2:
                    raise SVGError(f"{tag} needs at least {minimum // 2} coordinate pairs")
        except SVGError as error:
            errors.append(f"{label}: {error}")
    graph = {identifier: set() for identifier in identifiers}
    for label, target, owners in references:
        if target not in identifiers:
            errors.append(f"{label}: unresolved reference #{target}")
        else:
            for owner in owners:
                graph[owner].add(target)
    try:
        graphlib.TopologicalSorter(graph).prepare()
    except graphlib.CycleError as error:
        errors.append(f"Cyclic SVG references: {' -> '.join(error.args[1])}")
    for label, target in accessibility_refs:
        if target not in identifiers:
            errors.append(f"{label}: unresolved accessibility reference #{target}")
    if not any(child.tag == f"{{{SVG_NS}}}title" and (child.text or "").strip() for child in root):
        warnings.append("No nonempty root title; check the intended accessibility context")
    if counts["text"]:
        warnings.append("Text depends on installed fonts; inspect the target renderer")
    return root, {
        "valid": not errors,
        "input": str(Path(source).resolve()),
        "viewBox": view_box,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "bytes": byte_count,
            "elements": len(nodes),
            "groups": counts["g"],
            "drawing_elements": sum(counts[tag] for tag in DRAWING_TAGS),
            "path_segments": segment_count,
            "ids": len(identifiers),
            "by_tag": dict(sorted(counts.items())),
        },
    }


def check_scene(source, root, report):
    try:
        scene, scene_report = inspect_scene(source, require_bound=True)
    except SceneError as error:
        raise SVGError(str(error)) from error
    errors = report["errors"]
    errors.extend(scene_report["errors"])
    report["scene"] = str(Path(source).resolve())
    if not scene_report["valid"]:
        report["valid"] = False
        return
    expected_box = scene["canvas"]["viewBox"]
    if report["viewBox"] is not None and any(
        not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
        for actual, expected in zip(report["viewBox"], expected_box)
    ):
        errors.append("Scene viewBox does not match the SVG")
    entries = scene["elements"]
    nodes = list(walk_elements(root))
    by_id = {element.get("id"): (index, element, ancestors) for index, (element, ancestors) in enumerate(nodes) if element.get("id")}
    seen = set()
    previous_index = -1
    for entry in entries:
        identifier = entry["id"]
        parent = entry["parent"]
        seen.add(identifier)
        if identifier not in by_id:
            errors.append(f"Scene {identifier}: ID missing from SVG")
            continue
        index, element, ancestors = by_id[identifier]
        if entry.get("tag") != local_name(element.tag):
            errors.append(f"Scene {identifier}: tag does not match SVG")
        actual_parent = ancestors[-1] if ancestors else None
        if (parent is None and actual_parent is not root) or (
            parent is not None and (actual_parent is None or actual_parent.get("id") != parent)
        ):
            errors.append(f"Scene {identifier}: parent does not match SVG")
        if index <= previous_index:
            errors.append(f"Scene {identifier}: elements must follow SVG document order")
        previous_index = index
    for element, ancestors in nodes:
        if local_name(element.tag) in DRAWING_TAGS | {"g"} and not any(
            local_name(ancestor.tag) in RESOURCE_TAGS for ancestor in ancestors
        ) and element.get("id") not in seen:
            report["warnings"].append(f"Unmapped semantic element: {element.get('id') or local_name(element.tag)}")
    report["valid"] = not errors


def serialize_svg(root):
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XLINK_NS)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_output(data, destination, inputs, force=False):
    destination = Path(destination)
    if any(destination.resolve() == Path(source).resolve() for source in inputs):
        raise SVGError("Output must not replace an input file")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
            temporary_name = handle.name
            handle.write(data)
        if force:
            os.replace(temporary_name, destination)
        else:
            try:
                os.link(temporary_name, destination)
            except FileExistsError as error:
                raise SVGError("Output exists; choose another path or pass --force") from error
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)
