from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from animal_desktop_overlay.extract import extract_animal_cutout
from animal_desktop_overlay.overlay import OverlayOptions, show_overlay


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="animal-desktop-overlay")
    p.add_argument("--image", required=True, help="Path to an input image (jpg/png/webp).")
    p.add_argument("--scale", type=float, default=1.0, help="Scale factor for the on-screen overlay.")
    p.add_argument("--seed", type=int, default=None, help="Random seed for placement (optional).")
    p.add_argument(
        "--out",
        default=None,
        help="Output cutout PNG path (default: ./out/<stem>-cutout-<timestamp>.png).",
    )
    args = p.parse_args(argv)

    in_path = Path(args.image).expanduser()
    if args.out is None:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = Path("out") / f"{in_path.stem}-cutout-{ts}.png"
    else:
        out_path = Path(args.out)

    res = extract_animal_cutout(in_path, out_path)
    return show_overlay(res.output_path, options=OverlayOptions(scale=args.scale, seed=args.seed))


raise SystemExit(main())

