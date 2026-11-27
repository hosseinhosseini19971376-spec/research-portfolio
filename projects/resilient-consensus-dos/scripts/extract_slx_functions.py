#!/usr/bin/env python3
"""Extract MATLAB Function block scripts from original Simulink .slx files.

Usage:
    python scripts/extract_slx_functions.py models/withoutDOS.slx --output extracted

The script reads the Stateflow XML stored inside an SLX (ZIP) archive and writes
each embedded MATLAB Function script as a separate .m file. It does not modify
the source model.
"""
from __future__ import annotations

import argparse
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def safe_name(value: str) -> str:
    value = value.strip().replace("/", "__").replace("\\", "__")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("._") or "function"


def extract(model_path: Path, output_dir: Path) -> list[Path]:
    if not model_path.is_file():
        raise FileNotFoundError(model_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    with zipfile.ZipFile(model_path) as slx:
        try:
            xml_bytes = slx.read("simulink/stateflow.xml")
        except KeyError as exc:
            raise RuntimeError(
                f"{model_path} does not contain simulink/stateflow.xml"
            ) from exc

    root = ET.fromstring(xml_bytes)
    model_name = model_path.stem

    for chart in root.findall(".//chart"):
        chart_name = next(
            (
                node.text or ""
                for node in chart.findall("./P")
                if node.attrib.get("Name") == "name"
            ),
            "unnamed_chart",
        )
        for index, eml in enumerate(chart.findall(".//eml"), start=1):
            script_node = eml.find("./P[@Name='script']")
            if script_node is None or not (script_node.text or "").strip():
                continue

            filename = f"{safe_name(model_name)}__{safe_name(chart_name)}__{index}.m"
            destination = output_dir / filename
            destination.write_text(script_node.text.strip() + "\n", encoding="utf-8")
            written.append(destination)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models", nargs="+", type=Path, help="Input .slx files")
    parser.add_argument("--output", type=Path, default=Path("extracted"))
    args = parser.parse_args()

    total = 0
    for model in args.models:
        files = extract(model, args.output)
        total += len(files)
        print(f"{model}: extracted {len(files)} MATLAB Function script(s)")
        for file in files:
            print(f"  {file}")

    print(f"Total scripts extracted: {total}")


if __name__ == "__main__":
    main()
