#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import textwrap
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = ROOT / "2025-12-25T18-12-09-207307.json"
OUT_JSON = ROOT / "codex" / "optimized_payload.json"


def _compress_ws(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def compress_description(s: str, max_len: int = 220) -> str:
    s = _compress_ws(s)
    s = re.sub(r"[#*_`>{}\\[\\]]+", "", s)  # drop common markdown-ish tokens
    s = re.sub(r"[\U00010000-\U0010FFFF]", "", s)  # drop non-bmp emoji/etc
    s = re.sub(
        r"\b(IMPORTANT|CRITICAL|MUST|NEVER|ALWAYS|ABSOLUTELY|REQUIRED|FORBIDDEN|ZERO TOLERANCE)\b",
        lambda m: m.group(1).lower(),
        s,
    )
    s = _compress_ws(s)
    if len(s) <= max_len:
        return s
    # take first sentence if it fits, else hard cut
    m = re.search(r"^(.{1,%d}?)(?:\\.|\\n|$)" % max_len, s)
    if m:
        return m.group(1).strip()
    return s[:max_len].rstrip()


def transform_values(obj: Any, predicate: Callable[[str, Any], bool], f: Callable[[Any], Any]) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if predicate(k, v):
                out[k] = f(v)
            else:
                out[k] = transform_values(v, predicate, f)
        return out
    if isinstance(obj, list):
        return [transform_values(v, predicate, f) for v in obj]
    return obj


def extract_section(content: str, heading: str) -> str:
    i = content.find(heading)
    if i < 0:
        raise ValueError(f"missing heading: {heading}")
    return content[i:]


def extract_first_codeblock(content: str, lang: str) -> str:
    m = re.search(rf"```{re.escape(lang)}\n([\s\S]*?)```", content)
    if not m:
        raise ValueError(f"missing ```{lang} block")
    return m.group(1).rstrip()


def main() -> None:
    src = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    out = copy.deepcopy(src)

    # 1) system prompts: rewrite for brevity while keeping core constraints
    out["messages"][0]["content"] = _compress_ws(
        """
        <!-- filename: COMMON.md -->
        # autobe agent

        role: autobe backend agent (typescript, nestjs, prisma). produce production-ready, type-safe outputs.
        language: talk to the user in en; write code/docs/comments in english.
        time: asia/seoul, 2025-12-25T09:09:24.588Z.
        """
    )

    out["messages"][1]["content"] = _compress_ws(
        """
        <!-- filename: INTERFACE_OPERATION.md -->
        # api operation generator

        you generate `IAutoBeInterfaceOperationApplication.IProps.operations` from provided requirements + prisma schemas.

        <inputs>
        - use already-loaded conversation data first.
        - if required info is missing, call `process()` to request it (analysis files, prisma schemas, previous ops).
        - do not guess fields, relations, validation rules, or auth requirements; request the source instead.
        </inputs>

        <output>
        - always call `process({ thinking, request: { type: "complete", operations } })`.
        - every operation must include all required fields; no undefined required fields.
        </output>

        <operation schema (minimal)>
        ```typescript
        export namespace IAutoBeInterfaceOperationApplication {
          export interface IProps { operations: IOperation[] }
          interface IOperation {
            path: string
            method: string
            name: "index"|"at"|"search"|"create"|"update"|"erase"
            description: string
            parameters?: Array<unknown>
            requestBody?: unknown
            responseBody?: unknown
            authorizationActors: string[]
            authorizationType: "login"|"join"|"refresh"|null
            authorizationActor: string|null
            prerequisites: Array<unknown>
          }
        }
        ```
        </operation schema>

        <rules>
        - method/name mapping: get=list/index|search or single=at; post=create; put/patch=update; delete=erase.
        - paths: keep consistent, stable, and REST-like; path params must be used and named consistently.
        - descriptions: 2+ short paragraphs covering purpose, auth, inputs (params/body), outputs, and key business rules/errors.
        - authorization:
          - set `authorizationType`/`authorizationActor`/`authorizationActors` consistently; keep actor ids in camelCase.
          - exclude user/session auth endpoints unless requirements explicitly say otherwise (handled by dedicated auth system).
        - data:
          - exclude purely system-generated/audit/log/metric endpoints unless explicitly required.
          - do not invent dto fields; align request/response bodies with prisma schemas and loaded requirements.
        - uniqueness: accessor (non-param path segments + operation name) must be globally unique; adjust paths/ops to avoid conflicts.
        - be conservative: prefer fewer, correct operations over speculative coverage.
        </rules>
        """
    )

    # message 3: keep the "not yet loaded" inventory, drop the long admonitions
    m3_src = src["messages"][3]["content"]
    not_yet_loaded_analysis = extract_first_codeblock(m3_src, "json")
    out["messages"][3]["content"] = _compress_ws(
        f"""
        <!-- filename: PRELIMINARY_ANALYSIS_FILE.md -->
        # preliminary loading rules (analysis files)

        - do not request already-loaded analysis files.
        - only request files listed under "not yet loaded".
        - if you need requirements/validation details, request the specific file(s); do not infer from filenames.

        not yet loaded (available on request):
        ```json
        {not_yet_loaded_analysis}
        ```
        """
    )

    # message 7: keep the schema inventory table, drop the long admonitions/examples
    m7_src = src["messages"][7]["content"]
    table_start = m7_src.find("Name | Stance | Summary")
    if table_start < 0:
        raise ValueError("missing prisma inventory table")
    table_end = m7_src.find("\n\n###", table_start)
    prisma_table = m7_src[table_start:table_end].rstrip()
    out["messages"][7]["content"] = _compress_ws(
        f"""
        <!-- filename: PRELIMINARY_PRISMA_SCHEMA.md -->
        # preliminary loading rules (prisma schemas)

        - do not request already-loaded prisma schemas.
        - only request schema names listed under "not yet loaded".
        - if you need fields/relations/constraints, request the actual schema; do not guess.

        not yet loaded (available on request):
        {prisma_table}
        """
    )

    out["messages"][8]["content"] = _compress_ws(
        """
        <!-- filename: INTERFACE_OPERATION_REVIEW.md -->
        # api operation reviewer

        you review generated operations for security, prisma/schema alignment, and logical/semantic consistency.

        <inputs>
        - use already-loaded conversation data first.
        - if required info is missing (requirements or prisma fields), call `process()` to fetch it; do not guess.
        </inputs>

        <output>
        - always call `process({ thinking, request })`.
        - on completion, use:
          `request = { type: "complete", think: { review, plan }, content: operations }`.
        </output>

        <completion schema (minimal)>
        ```typescript
        export namespace IAutoBeInterfaceOperationReviewApplication {
          export interface IProps {
            thinking: string
            request: IComplete | unknown
          }
          export interface IComplete {
            type: "complete"
            think: { review: string; plan: string }
            content: AutoBeOpenApi.IOperation[]
          }
        }
        export namespace AutoBeOpenApi {
          export interface IOperation {
            path: string
            method: string
            description: string
            parameters?: Array<unknown>
            requestBody?: unknown
            responseBody?: unknown
            authorizationType: "login"|"join"|"refresh"|null
            authorizationActor: string|null
            name: string
            prerequisites: Array<unknown>
          }
        }
        ```
        </completion schema>

        <review checklist>
        - required fields present; no undefined required fields.
        - security: no passwords/tokens/secrets in responses; enforce auth boundaries; least-privilege authorization.
        - prisma/schema: referenced fields/relations exist; types/formats match; no invented properties.
        - semantics: list endpoints return arrays/paged results; single endpoints return single; http method matches behavior.
        - path/params: every path param is used; no unused/meaningless params; consistent naming.
        - patch: use only for complex updates; otherwise use put/post patterns as per system conventions.
        - remove operations that are impossible/unsafe/contradict requirements or schema.
        </review checklist>
        """
    )

    out["messages"][11]["content"] = _compress_ws(
        """
        # function calling

        - build tool calls that strictly match the provided json schema (types, required fields, enums/consts).
        - do not invent properties; do not omit required fields; use null only when schema allows it.
        - for union types, set the correct discriminator (`type`) and include only the fields for that branch.
        - if info is missing to build a valid call, request the minimal missing data first.
        - output only the tool call arguments; keep text brief and in english when the schema requires it.
        """
    )

    # 2) tool descriptions: compress (keep schema intact)
    out["tools"] = transform_values(
        out.get("tools", []),
        predicate=lambda k, v: k == "description" and isinstance(v, str),
        f=lambda v: compress_description(v),
    )
    # also shorten the top-level function description a bit more
    try:
        fn_desc = out["tools"][0]["function"].get("description", "")
        out["tools"][0]["function"]["description"] = compress_description(fn_desc, max_len=140)
    except Exception:
        pass

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
