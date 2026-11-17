#!/usr/bin/env python3
"""Rebuild the category app lists in README.md from */omarchy-app.yml listings."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

CAT_TO_HEADING = {
    "media": "Media",
    "photography": "Photos",
    "photos": "Photos",
    "files": "Files & productivity",
    "finance": "Finance",
    "social": "Social & reading",
    "automation": "Home & automation",
    "networking": "Networking",
    "ai": "AI",
    "developer": "Developer tools",
    "gaming": "Gaming",
    "crypto": "Crypto",
    "bitcoin": "Bitcoin",
}

HEADING_ORDER = [
    "Media",
    "Photos",
    "Files & productivity",
    "Finance",
    "Social & reading",
    "Home & automation",
    "Networking",
    "AI",
    "Developer tools",
    "Gaming",
    "Crypto",
    "Bitcoin",
]


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_listing(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        if not raw or raw.startswith("#") or raw[:1] in " \t":
            continue
        if ":" not in raw:
            continue
        key, val = raw.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in (">-", ">", "|", "|+", "|-"):
            continue
        data[key] = unquote(val)
    return data


def load_apps() -> list[dict[str, str]]:
    apps = []
    for listing in sorted(ROOT.glob("*/omarchy-app.yml")):
        data = parse_listing(listing)
        name = data.get("name")
        category = data.get("category")
        if not name or not category:
            raise SystemExit(f"{listing}: missing name or category")
        apps.append(
            {
                "name": name,
                "website": data.get("website", "").strip(),
                "category": category,
            }
        )
    return apps


def item_markdown(app: dict[str, str]) -> str:
    name = app["name"]
    website = app["website"]
    if website:
        return f"[{name}]({website})"
    return name


def render_sections(apps: list[dict[str, str]]) -> str:
    by_heading: dict[str, list[dict[str, str]]] = defaultdict(list)
    unknown = set()
    for app in apps:
        heading = CAT_TO_HEADING.get(app["category"])
        if heading is None:
            unknown.add(app["category"])
            continue
        by_heading[heading].append(app)
    if unknown:
        raise SystemExit(f"unknown listing categor(y/ies): {sorted(unknown)}")

    lines = [f"{len(apps)} apps today.", ""]
    for heading in HEADING_ORDER:
        group = by_heading.get(heading)
        if not group:
            continue
        group.sort(key=lambda a: (a["name"].casefold(), a["name"]))
        items = ", ".join(item_markdown(a) for a in group)
        lines.append(f"**{heading} ({len(group)}):** {items}")
        lines.append("")
    return "\n".join(lines) + "\n"


APPS_TODAY_RE = re.compile(r"^\d+ apps today\.", re.MULTILINE)
END_MARKER = "### Apps that ask for extra access"


def update_readme(text: str, section: str) -> str:
    start = APPS_TODAY_RE.search(text)
    end = text.find(END_MARKER)
    if not start or end < 0 or end <= start.start():
        raise SystemExit("README.md: could not find category app lists to replace")
    if not section.endswith("\n"):
        section += "\n"
    return text[: start.start()] + section + text[end:]


def main() -> int:
    apps = load_apps()
    section = render_sections(apps)
    readme = README.read_text()
    updated = update_readme(readme, section)
    if updated == readme:
        print(f"README.md already in sync ({len(apps)} apps)")
        return 0
    README.write_text(updated)
    print(f"updated README.md ({len(apps)} apps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
