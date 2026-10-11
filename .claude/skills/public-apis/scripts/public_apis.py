#!/usr/bin/env python3
"""Search the public-apis catalog (github.com/public-apis/public-apis).

The catalog lives next to this script in ../data/ as TSV files built from the
upstream README. Standard library only.

  public_apis.py search forex rates --no-auth --https
  public_apis.py search -c Finance stock
  public_apis.py categories
  public_apis.py mcp stock
  public_apis.py build /path/to/public-apis/README.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
APIS_FILE = DATA_DIR / "apis.tsv"
MCP_FILE = DATA_DIR / "mcp-servers.tsv"

API_FIELDS = ["category", "name", "url", "description", "auth", "https", "cors", "sponsored"]
MCP_FIELDS = ["name", "url", "description", "auth", "transport"]

LINK_RE = re.compile(r"\[(.+?)\]\(\s*(\S+?)\s*\)")
INDEX_ENTRY_RE = re.compile(r"^\*\s+\[(.+?)\]\(#")
DEFAULT_LIMIT = 40


# --- build -------------------------------------------------------------------

def strip_tracking(url: str) -> tuple[str, bool]:
    """Drop utm_* parameters; report whether the link carried any (sponsor links do)."""
    parts = urlsplit(url.strip())
    query = parse_qsl(parts.query, keep_blank_values=True)
    kept = [(k, v) for k, v in query if not k.lower().startswith("utm_")]
    tracked = len(kept) != len(query)
    return urlunsplit(parts._replace(query=urlencode(kept))), tracked


def table_cells(line: str) -> list[str]:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return [cell.strip("`").strip() for cell in cells]


def parse_readme(text: str) -> tuple[list[dict], list[dict]]:
    lines = text.splitlines()
    categories = {m.group(1) for line in lines if (m := INDEX_ENTRY_RE.match(line.strip()))}
    apis: list[dict] = []
    mcp: list[dict] = []
    section = None  # category name, "MCP" or None
    for line in lines:
        if line.startswith("### "):
            title = line[4:].strip()
            section = title if title in categories else None
            continue
        if line.startswith("## "):
            section = "MCP" if line[3:].strip() == "MCP Servers" else None
            continue
        if section is None or not line.startswith("| ["):
            continue
        cells = table_cells(line)
        link = LINK_RE.match(cells[0])
        if not link:
            continue
        url, tracked = strip_tracking(link.group(2))
        if section == "MCP":
            if len(cells) >= 4:
                mcp.append(dict(zip(MCP_FIELDS, [link.group(1), url, cells[1], cells[2], cells[3]])))
            continue
        if len(cells) < 5:
            continue
        apis.append(dict(zip(API_FIELDS, [
            section, link.group(1), url, cells[1], cells[2], cells[3], cells[4],
            "yes" if tracked else "no",
        ])))
    return apis, mcp


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: " ".join(row[k].split()) for k in fields})


def cmd_build(args: argparse.Namespace) -> int:
    text = Path(args.readme).read_text(encoding="utf-8")
    apis, mcp = parse_readme(text)
    if not apis:
        print("No API rows found: has the upstream README format changed?", file=sys.stderr)
        return 1
    write_tsv(APIS_FILE, API_FIELDS, apis)
    write_tsv(MCP_FILE, MCP_FIELDS, mcp)
    categories = len({row["category"] for row in apis})
    print(f"{len(apis)} APIs in {categories} categories, {len(mcp)} MCP servers -> {DATA_DIR}")
    return 0


# --- query -------------------------------------------------------------------

def load(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"Missing {path}: run '{Path(__file__).name} build <README.md>' first.")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matches(row: dict, terms: list[str], fields: list[str]) -> bool:
    haystack = " ".join(row[f] for f in fields).lower()
    return all(term.lower() in haystack for term in terms)


def emit(rows: list[dict], fields: list[str], as_json: bool, total: int) -> None:
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    if not rows:
        print("No match. Try fewer or broader terms, or list categories with 'categories'.")
        return
    for row in rows:
        print(" | ".join(row[f] for f in fields))
    if total > len(rows):
        print(f"... {total - len(rows)} more (raise --limit or narrow the search)")


def cmd_search(args: argparse.Namespace) -> int:
    rows = load(APIS_FILE)
    if args.category:
        wanted = args.category.lower()
        rows = [r for r in rows if wanted in r["category"].lower()]
    rows = [r for r in rows if matches(r, args.terms, ["name", "description", "category"])]
    if args.no_auth:
        rows = [r for r in rows if r["auth"] == "No"]
    if args.https:
        rows = [r for r in rows if r["https"] == "Yes"]
    if args.cors:
        rows = [r for r in rows if r["cors"] == "Yes"]
    if args.no_sponsored:
        rows = [r for r in rows if r["sponsored"] == "no"]
    fields = ["category", "name", "auth", "https", "cors", "url", "description"]
    emit(rows[: args.limit], fields, args.json, len(rows))
    return 0


def cmd_categories(args: argparse.Namespace) -> int:
    counts: dict[str, int] = {}
    for row in load(APIS_FILE):
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    for name, count in counts.items():
        print(f"{count:4d}  {name}")
    print(f"{sum(counts.values()):4d}  total")
    return 0


def cmd_mcp(args: argparse.Namespace) -> int:
    rows = [r for r in load(MCP_FILE) if matches(r, args.terms, MCP_FIELDS)]
    emit(rows[: args.limit], ["name", "auth", "transport", "url", "description"], args.json, len(rows))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="find APIs; every term must match name, description or category")
    search.add_argument("terms", nargs="*", help="keywords (case-insensitive, all must match)")
    search.add_argument("-c", "--category", help="restrict to categories containing this text")
    search.add_argument("--no-auth", action="store_true", help="only APIs that need no key")
    search.add_argument("--https", action="store_true", help="only HTTPS APIs")
    search.add_argument("--cors", action="store_true", help="only APIs with CORS enabled (browser calls)")
    search.add_argument("--no-sponsored", action="store_true", help="hide links carrying sponsor tracking")
    search.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=cmd_search)

    categories = sub.add_parser("categories", help="list categories with their API count")
    categories.set_defaults(func=cmd_categories)

    mcp = sub.add_parser("mcp", help="search the catalog's MCP servers")
    mcp.add_argument("terms", nargs="*")
    mcp.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    mcp.add_argument("--json", action="store_true")
    mcp.set_defaults(func=cmd_mcp)

    build = sub.add_parser("build", help="rebuild data/*.tsv from an upstream README.md")
    build.add_argument("readme")
    build.set_defaults(func=cmd_build)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
