#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
IN_JSON = ROOT / "unoptimized" / "TOC_generation.json"
OUT_JSON = ROOT / "codex" / "optimized_TOC_generation.json"


FILENAME_RE = re.compile(r"<!--\s*filename:\s*([^\n]+?)\s*-->")


def _compress_ws(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def compress_description(s: str, max_len: int = 220) -> str:
    s = _compress_ws(s)
    s = re.sub(r"[#*_`>{}\\[\\]]+", "", s)
    s = re.sub(r"[\U00010000-\U0010FFFF]", "", s)
    s = re.sub(
        r"\b(IMPORTANT|CRITICAL|MUST|NEVER|ALWAYS|ABSOLUTELY|REQUIRED|FORBIDDEN|ZERO TOLERANCE)\b",
        lambda m: m.group(1).lower(),
        s,
    )
    s = _compress_ws(s)
    if len(s) <= max_len:
        return s
    # Prefer first sentence.
    m = re.search(r"^(.{1,%d}?)(?:\\.|\\n|$)" % max_len, s)
    if m:
        return m.group(1).strip()
    return s[:max_len].rstrip()


def transform_values(obj: Any, predicate: Callable[[str, Any], bool], f: Callable[[Any], Any]) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if predicate(k, v):
                out[k] = f(v)
            else:
                out[k] = transform_values(v, predicate, f)
        return out
    if isinstance(obj, list):
        return [transform_values(v, predicate, f) for v in obj]
    return obj


def _get_filename_marker(content: str) -> str | None:
    m = FILENAME_RE.search(content)
    return m.group(1).strip() if m else None


def main() -> None:
    src = json.loads(IN_JSON.read_text(encoding="utf-8"))
    out = copy.deepcopy(src)

    for msg in out.get("messages", []):
        if msg.get("role") != "system":
            continue
        content = msg.get("content")
        if not isinstance(content, str):
            continue

        filename = _get_filename_marker(content)

        if filename == "COMMON.md":
            msg["content"] = _compress_ws(
                """
                <!-- filename: COMMON.md -->
                # autobe agent

                role: autobe backend agent (typescript, nestjs, prisma). produce production-ready, type-safe outputs.
                language: talk to the user in en; write code/docs/comments in english.
                time: asia/seoul, 2025-12-25T09:09:24.588Z.
                """
            )
            continue

        if filename == "ANALYZE_WRITE.md":
            msg["content"] = _compress_ws(
                """
                <!-- filename: ANALYZE_WRITE.md -->
                # analyze + write

                goal: produce one comprehensive document that backend developers can implement from. no iterations.

                process:
                - use loaded context first.
                - if missing business/flow/rules details, call `process()` to fetch the minimal required analysis files (batch when possible).
                - do not infer requirements from filenames; do not guess.

                tool usage:
                - for preliminary: `process({ thinking, request: { type: "getAnalysisFiles", fileNames } })`.
                - for final: `process({ thinking, request: { type: "complete", plan, content } })`.
                - never call `complete` together with preliminary requests.

                thinking:
                - preliminary: state what is missing and why it blocks writing.
                - completion: state what you wrote and why inputs are sufficient.
                """
            )
            continue

        # Standalone function-calling system prompt (no filename marker)
        if content.lstrip().startswith("# AI Function Calling System Prompt"):
            msg["content"] = _compress_ws(
                """
                # function calling

                - build tool calls that strictly match the provided json schema (types, required fields, enums/consts).
                - do not invent properties; do not omit required fields; use null only when schema allows it.
                - for union types, set the correct discriminator (`type`) and include only the fields for that branch.
                - if info is missing to build a valid call, request the minimal missing data first.
                - output only the tool call arguments; keep text brief and in english when the schema requires it.
                """
            )

    # Compress tool/schema descriptions without altering the schema shape.
    out["tools"] = transform_values(
        out.get("tools", []),
        predicate=lambda k, v: k == "description" and isinstance(v, str),
        f=lambda v: compress_description(v),
    )
    try:
        fn_desc = out["tools"][0]["function"].get("description", "")
        out["tools"][0]["function"]["description"] = compress_description(fn_desc, max_len=140)
    except Exception:
        pass

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

