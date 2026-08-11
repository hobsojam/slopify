from __future__ import annotations

import argparse
import sys
from pathlib import Path

from slopify.config import SlopifyConfig
from slopify.deslopify import deslopify
from slopify.pipeline import Pipeline
from slopify.transformlog import TransformLog


def _read_input(path: str | None) -> str:
    if path is None or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _write_output(path: str | None, text: str) -> None:
    if path is None or path == "-":
        sys.stdout.write(text)
    else:
        Path(path).write_text(text, encoding="utf-8")


def slopify_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="slopify", description="Make text look like AI slop.")
    parser.add_argument("input", nargs="?", default="-", help="Input file, or '-' for stdin (default).")
    parser.add_argument("-o", "--output", default="-", help="Output file, or '-' for stdout (default).")
    parser.add_argument("--intensity", type=int, default=50, help="0-100 slop dial (default: 50).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed, for reproducible output.")
    parser.add_argument("--log", default=None, help="Path to save the transform log (needed for deslopify).")
    args = parser.parse_args(argv)

    config = SlopifyConfig(intensity=args.intensity, seed=args.seed)
    result = Pipeline(config).run(_read_input(args.input))

    _write_output(args.output, result.text)
    if args.log:
        result.log.save(args.log)
    return 0


def deslopify_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="deslopify", description="Undo a slopify run using its transform log.")
    parser.add_argument("input", nargs="?", default="-", help="Slopified input file, or '-' for stdin (default).")
    parser.add_argument("-o", "--output", default="-", help="Output file, or '-' for stdout (default).")
    parser.add_argument("--log", required=True, help="Path to the transform log saved by slopify --log.")
    args = parser.parse_args(argv)

    log = TransformLog.load(args.log)
    restored = deslopify(_read_input(args.input), log)
    _write_output(args.output, restored)
    return 0


if __name__ == "__main__":
    sys.exit(slopify_main())
