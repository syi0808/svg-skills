import argparse
import math
import warnings

from svg_utils import SVGError, emit


def compare_images(before_path, after_path):
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError as error:
        raise SVGError("Comparison needs Pillow in the selected Python environment") from error

    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        try:
            with Image.open(before_path) as before_source, Image.open(after_path) as after_source:
                if before_source.size != after_source.size:
                    raise SVGError("Render dimensions differ; rerender at the same viewport instead of resizing")
                if before_source.width * before_source.height > 16000000:
                    raise SVGError("Comparison exceeds the 16-million-pixel limit")
                before = before_source.convert("RGBA")
                after = after_source.convert("RGBA")
        except (Image.DecompressionBombWarning, Image.DecompressionBombError) as error:
            raise SVGError("Image exceeds Pillow's safe image size") from error
    rmse_by_background = {}
    for background_name, background_color in [("black", "#000000"), ("white", "#FFFFFF")]:
        background = Image.new("RGBA", before.size, background_color)
        before_flat = Image.alpha_composite(background, before).convert("RGB")
        after_flat = Image.alpha_composite(background, after).convert("RGB")
        difference = ImageChops.difference(before_flat, after_flat)
        channel_rms = ImageStat.Stat(difference).rms
        rmse_by_background[background_name] = math.sqrt(sum(value * value for value in channel_rms) / 3) / 255
    alpha_difference = ImageChops.difference(before.getchannel("A"), after.getchannel("A"))
    return {
        "width": before.width,
        "height": before.height,
        "rmse": max(rmse_by_background.values()),
        "rmse_by_background": rmse_by_background,
        "alpha_rmse": ImageStat.Stat(alpha_difference).rms[0] / 255,
    }


def main():
    parser = argparse.ArgumentParser(description="Measure visible pixel differences, not semantic similarity or aesthetic quality.")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--max-rmse", type=float, help="Optional normalized 0..1 threshold; 0 requires identical visible pixels")
    arguments = parser.parse_args()
    try:
        if arguments.max_rmse is not None and (not math.isfinite(arguments.max_rmse) or not 0 <= arguments.max_rmse <= 1):
            raise SVGError("--max-rmse must be a finite number in 0..1")
        result = compare_images(arguments.before, arguments.after)
        passed = arguments.max_rmse is None or result["rmse"] <= arguments.max_rmse
        emit({**result, "threshold": arguments.max_rmse, "passed": passed})
        return 0 if passed else 1
    except (OSError, SVGError) as error:
        emit({"ok": False, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
