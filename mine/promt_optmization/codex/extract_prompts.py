#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN_JSON = ROOT / "codex" / "optimized_payload.json"
DEFAULT_OUT_DIR = ROOT / "prompts"


FILENAME_RE = re.compile(r"<!--\s*filename:\s*([^\n]+?)\s*-->")


def _slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "prompt"


def _safe_basename(p: str) -> str:
    p = p.strip().replace("\\", "/")
    return Path(p).name


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Extract system prompt contents into markdown files.")
    parser.add_argument("--in", dest="in_json", default=str(DEFAULT_IN_JSON), help="input JSON payload")
    parser.add_argument("--out", dest="out_dir", default=str(DEFAULT_OUT_DIR), help="output directory")
    args = parser.parse_args()

    in_json = Path(args.in_json)
    out_dir = Path(args.out_dir)

    data: Any = json.loads(in_json.read_text(encoding="utf-8"))
    messages = data.get("messages", [])

    out_dir.mkdir(parents=True, exist_ok=True)
    # Make output deterministic: clear prior generated files.
    for p in out_dir.glob("*.md"):
        p.unlink(missing_ok=True)
    (out_dir / "index.txt").unlink(missing_ok=True)

    written = []
    for i, msg in enumerate(messages):
        if msg.get("role") != "system":
            continue
        content = msg.get("content")
        if not isinstance(content, str) or not content.strip():
            continue

        m = FILENAME_RE.search(content)
        if m:
            filename = _safe_basename(m.group(1))
            if not filename.lower().endswith(".md"):
                filename = f"{filename}.md"
        else:
            # Fallback: derive a stable readable name for prompts without filename marker.
            # Prefer first markdown heading if present.
            heading = None
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("#"):
                    heading = line.lstrip("#").strip()
                    break
            base = heading or f"system-message-{i}"
            slug = _slugify(base)
            if "function-calling" in slug or "function-calling" in slug.replace("-", ""):
                filename = "AI_FUNCTION_CALLING_SYSTEM_PROMPT.md"
            else:
                filename = f"{slug}.md"

        out_path = out_dir / filename
        out_path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written.append(out_path)

    index = out_dir / "index.txt"
    lines = []
    for p in written:
        rp = p.resolve()
        try:
            lines.append(str(rp.relative_to(ROOT)))
        except ValueError:
            lines.append(str(p))
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
