#!/usr/bin/env python3
"""Build catalog.json from listing YAML + compose files. Does not rewrite listings."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

STORE_FILES = ("omarchy-app-store.yml", "umbrel-app-store.yml")
APP_FILES = ("omarchy-app.yml", "umbrel-app.yml")
COMPOSE_FILES = ("omarchy-compose.yml", "docker-compose.yml")
ABOUT = (
    "Apps My Own Data Center can install from this store. Each id is a folder with "
    "omarchy-app.yml and docker-compose.yml. My Own Data Center still copies compose "
    "from that folder on install."
)
PROVIDED = {
    "APP_DATA_DIR",
    "APP_DATA_ROOT",
    "APP_ID",
    "APP_DOMAIN",
    "APP_VERSION",
    "APP_PROXY_PORT",
    "APP_HIDDEN_SERVICE",
    "GATEWAY_IP",
    "DEVICE_HOSTNAME",
    "DEVICE_DOMAIN_NAME",
    "APP_PASSWORD",
    "APP_SEED",
    "APP_SEED_32",
    "UMBREL_ROOT",
    "DOCKER_HOST",
    "TZ",
    "NETWORK_IP",
    "TOR_PROXY_IP",
    "TOR_PROXY_PORT",
    "TOR_DATA_DIR",
    "TOR_PASSWORD",
    "SERVER_IP",
    "DOWNLOADS_DIR",
    "VIDEOS_DIR",
    "MUSIC_DIR",
    "PICTURES_DIR",
    "DOCUMENTS_DIR",
    "PUID",
    "PGID",
    "DOCKER_SOCKET",
    "APP_GATEWAY_KEY",
}
APP_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
FOLDER_ID_RE = re.compile(r"^[a-z][a-z0-9_]{0,30}$")
FOLDER_VAR_RE = re.compile(r"^FOLDER_[A-Z0-9_]+$")
SUGGEST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_ .-]{0,60}$")
MEDIA_FILE_RE = re.compile(r"^[\w.-]+$")
EXPORT_RE = re.compile(r"\bexport\s+([A-Za-z_][A-Za-z0-9_]*)\b")
VAR_RE = re.compile(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)([^}]*)\}|([A-Za-z_][A-Za-z0-9_]*))")
HAS_DEFAULT_RE = re.compile(r"^:?[-=]")
HTTPS_RE = re.compile(r"^https://")


def store_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def first_existing(directory: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        path = directory / name
        if path.is_file():
            return path
    return None


def js_number(value) -> float:
    if value is None or value is False:
        return 0.0
    if value is True:
        return 1.0
    if isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text == "":
            return 0.0
        try:
            return float(text)
        except ValueError:
            return float("nan")
    return float("nan")


def js_is_integer(value) -> bool:
    number = js_number(value)
    if number != number or number in (float("inf"), float("-inf")):
        return False
    return number == float(int(number))


def js_int(value) -> int | None:
    if not js_is_integer(value):
        return None
    return int(js_number(value))


def strings(values) -> list[str]:
    if not isinstance(values, list):
        return []
    return [item for item in values if isinstance(item, str)]


def folder_choices(listing) -> list[dict]:
    folders = listing.get("folders")
    if not isinstance(folders, list):
        return []
    out = []
    for folder in folders:
        if not isinstance(folder, dict):
            continue
        folder_id = folder.get("id")
        if not isinstance(folder_id, str) or not FOLDER_ID_RE.fullmatch(folder_id):
            continue
        choice = {
            "id": folder_id,
            "label": str(folder.get("label", folder_id))[:80],
            "detail": folder.get("detail")[:400] if isinstance(folder.get("detail"), str) else "",
        }
        suggest = folder.get("suggest")
        if isinstance(suggest, str) and SUGGEST_RE.fullmatch(suggest):
            choice["suggest"] = suggest
        out.append(choice)
        if len(out) == 4:
            break
    return out


def missing_vars(text: str, also_provided: list[str]) -> list[str]:
    extra = set(also_provided)
    found: list[str] = []
    seen: set[str] = set()
    for match in VAR_RE.finditer(text.replace("$$", "")):
        name = match.group(1) or match.group(3)
        rest = match.group(2) or ""
        if HAS_DEFAULT_RE.match(rest):
            continue
        if name in PROVIDED or name in extra or FOLDER_VAR_RE.fullmatch(name):
            continue
        if name not in seen:
            seen.add(name)
            found.append(name)
    return found


def exported_names(text: str) -> list[str]:
    return EXPORT_RE.findall(text)


def media_url(value, gallery: str | None, app_id: str) -> str | None:
    if not isinstance(value, str):
        return None
    if HTTPS_RE.match(value):
        return value
    if gallery and MEDIA_FILE_RE.fullmatch(value):
        return f"{gallery}/{app_id}/{value}"
    return None


def needs_of(app_id: str, by_id: dict[str, dict], seen: set[str] | None = None) -> set[str]:
    if seen is None:
        seen = set()
    for dep in strings(by_id.get(app_id, {}).get("listing", {}).get("dependencies")):
        if dep in seen:
            continue
        seen.add(dep)
        needs_of(dep, by_id, seen)
    return seen


def order_needs(app_id: str, by_id: dict[str, dict], seen: set[str] | None = None, out: list[str] | None = None) -> list[str]:
    if seen is None:
        seen = set()
    if out is None:
        out = []
    for dep in strings(by_id.get(app_id, {}).get("listing", {}).get("dependencies")):
        if dep in seen:
            continue
        seen.add(dep)
        order_needs(dep, by_id, seen, out)
        out.append(dep)
    return out


def load_found(root: Path) -> list[dict]:
    found = []
    for entry in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        app_path = first_existing(entry, APP_FILES)
        if app_path is None:
            continue
        listing = read_yaml(app_path) or {}
        app_id = listing.get("id")
        if not isinstance(app_id, str) or app_id != entry.name or not APP_ID_RE.fullmatch(app_id):
            continue
        compose_path = first_existing(entry, COMPOSE_FILES)
        if compose_path is None:
            continue
        compose = compose_path.read_text(encoding="utf-8")
        exports_path = entry / "exports.sh"
        exports_text = exports_path.read_text(encoding="utf-8") if exports_path.is_file() else ""
        found.append(
            {
                "id": app_id,
                "listing": listing,
                "compose": compose,
                "exported": exported_names(exports_text),
            }
        )
    return found


def store_gallery(root: Path) -> str | None:
    meta_path = first_existing(root, STORE_FILES)
    if meta_path is None:
        return None
    meta = read_yaml(meta_path) or {}
    gallery = meta.get("gallery")
    if isinstance(gallery, str) and HTTPS_RE.match(gallery):
        return gallery.rstrip("/")
    return None


def listing_object(item: dict, by_id: dict[str, dict], found: list[dict], needed_by_others: set[str], gallery: str | None) -> dict:
    listing = item["listing"]
    app_id = item["id"]
    compose = item["compose"]
    deps = strings(listing.get("dependencies"))
    all_needs = list(needs_of(app_id, by_id))
    absent = [dep for dep in all_needs if dep not in by_id]
    from_deps = [name for dep in all_needs for name in by_id.get(dep, {}).get("exported", [])]
    missing = missing_vars(compose, item["exported"] + from_deps)
    unsupported = f"Needs {', '.join(absent)}, which isn’t in this store." if absent else None
    optional_from = []
    seen_names = set()
    for var in missing:
        for other in found:
            if var in other["exported"]:
                name = str(other["listing"].get("name") or other["id"])
                if name not in seen_names:
                    seen_names.add(name)
                    optional_from.append(name)
    unknown = [var for var in missing if not any(var in other["exported"] for other in found)]
    if optional_from:
        pronoun = "them" if len(optional_from) > 1 else "it"
        caution = f"Works with {', '.join(optional_from)} too: install {pronoun} to use those features."
    elif unknown:
        caution = (
            "Some features may not work here: it expects settings My Own Data Center doesn’t have "
            f"({', '.join(unknown[:3])})."
        )
    else:
        caution = None

    icon = media_url(listing.get("icon"), gallery, app_id)
    if icon is None and gallery:
        icon = f"{gallery}/{app_id}/icon.svg"

    app = {
        "id": app_id,
        "name": str(listing["name"] if listing.get("name") is not None else app_id),
    }
    if listing.get("tagline") is not None:
        app["tagline"] = listing["tagline"]
    if icon:
        app["icon"] = icon
    if listing.get("category") is not None:
        app["category"] = listing["category"]
    if listing.get("version") is not None:
        app["version"] = str(listing["version"])
    port = js_int(listing.get("port"))
    if port:
        app["port"] = port
    app["path"] = listing["path"] if isinstance(listing.get("path"), str) else ""
    if listing.get("description") is not None:
        app["description"] = listing["description"]
    if listing.get("developer") is not None:
        app["developer"] = listing["developer"]
    if listing.get("website") is not None:
        app["website"] = listing["website"]
    gallery_urls = []
    raw_gallery = listing.get("gallery") if isinstance(listing.get("gallery"), list) else []
    for item_url in raw_gallery:
        url = media_url(item_url, gallery, app_id)
        if url:
            gallery_urls.append(url)
    app["gallery"] = gallery_urls
    if listing.get("releaseNotes"):
        app["releaseNotes"] = listing["releaseNotes"]
    if deps:
        app["dependencies"] = deps
        app["needs"] = order_needs(app_id, by_id)
    implements = strings(listing.get("implements")) if isinstance(listing.get("implements"), list) else []
    if implements:
        app["implements"] = implements
    shared = bool(deps) or app_id in needed_by_others or "ipv4_address" in compose
    if shared:
        app["shared"] = True
    if listing.get("defaultUsername"):
        app["defaultUsername"] = listing["defaultUsername"]
    if listing.get("defaultPassword"):
        app["defaultPassword"] = listing["defaultPassword"]
    if listing.get("deterministicPassword") is True:
        app["deterministicPassword"] = True
    if listing.get("requiresHttps") is True:
        app["requiresHttps"] = True
    if isinstance(listing.get("openPorts"), list):
        open_ports = []
        for raw in listing["openPorts"]:
            number = js_int(raw)
            if number is not None and 1 <= number <= 65535 and number != 22 and number not in open_ports:
                open_ports.append(number)
            if len(open_ports) == 16:
                break
        if open_ports:
            app["openPorts"] = open_ports
    folders = folder_choices(listing)
    if folders:
        app["folders"] = folders
    web = listing.get("web")
    if isinstance(web, dict) and isinstance(web.get("service"), str) and js_is_integer(web.get("port")):
        web_obj = {"service": web["service"], "port": int(js_number(web["port"]))}
        if web.get("https") is True:
            web_obj["https"] = True
        app["web"] = web_obj
    if unsupported:
        app["unsupported"] = unsupported
    if caution:
        app["caution"] = caution
    return app


def render(root: Path) -> str:
    gallery = store_gallery(root)
    found = load_found(root)
    by_id = {item["id"]: item for item in found}
    needed_by_others = {dep for item in found for dep in strings(item["listing"].get("dependencies"))}
    apps = [listing_object(item, by_id, found, needed_by_others, gallery) for item in found]
    catalog = {"version": 1, "about": ABOUT, "apps": apps}
    return json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render catalog.json from app listings.")
    parser.add_argument("--check", action="store_true", help="exit 1 if catalog.json would change")
    args = parser.parse_args()
    root = store_root()
    text = render(root)
    dest = root / "catalog.json"
    if args.check:
        current = dest.read_text(encoding="utf-8") if dest.is_file() else None
        if current != text:
            print("catalog.json is stale; run scripts/render-catalog.py", file=sys.stderr)
            return 1
        print(f"catalog.json is up to date ({len(json.loads(text)['apps'])} apps, {len(text.encode('utf-8'))} bytes)")
        return 0
    dest.write_text(text, encoding="utf-8")
    print(f"Wrote {dest} ({len(json.loads(text)['apps'])} apps, {len(text.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
