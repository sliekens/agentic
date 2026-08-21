#!/usr/bin/env python3
"""Generate the Claude adapter and synchronized catalogs from portable manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GITHUB_MARKETPLACE = ROOT / ".github" / "plugin" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PORTABLE_METADATA_FIELDS = (
    "name",
    "description",
    "version",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def render_json(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def selected_metadata(manifest: dict) -> dict:
    return {field: manifest[field] for field in PORTABLE_METADATA_FIELDS if field in manifest}


def claude_adapter(manifest: dict) -> dict:
    return selected_metadata(manifest)


def marketplace_catalog(source: dict, manifests: dict[str, dict], *, github: bool) -> dict:
    catalog = {key: value for key, value in source.items() if key != "plugins"}
    entries = []
    for old_entry in source.get("plugins", []):
        name = old_entry["name"]
        manifest = manifests[name]
        entry = dict(old_entry)
        entry["source"] = f"plugins/{name}" if github else f"./plugins/{name}"
        entry["description"] = manifest["description"]
        if "version" in entry:
            entry["version"] = manifest["version"]
        entries.append(entry)
    catalog["plugins"] = entries
    return catalog


def expected_files() -> dict[Path, str]:
    github_source = load_json(GITHUB_MARKETPLACE)
    claude_source = load_json(CLAUDE_MARKETPLACE)
    plugin_names = [entry["name"] for entry in github_source["plugins"]]
    if plugin_names != [entry["name"] for entry in claude_source["plugins"]]:
        raise ValueError("GitHub and Claude marketplace plugin order differs")

    manifests = {
        name: load_json(ROOT / "plugins" / name / "plugin.json") for name in plugin_names
    }
    files: dict[Path, str] = {}
    for name, manifest in manifests.items():
        plugin_root = ROOT / "plugins" / name
        files[plugin_root / ".claude-plugin" / "plugin.json"] = render_json(
            claude_adapter(manifest)
        )

    files[GITHUB_MARKETPLACE] = render_json(
        marketplace_catalog(github_source, manifests, github=True)
    )
    files[CLAUDE_MARKETPLACE] = render_json(
        marketplace_catalog(claude_source, manifests, github=False)
    )
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Fail when generated files are out of date."
    )
    args = parser.parse_args()

    stale = []
    for path, expected in expected_files().items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual == expected:
            continue
        if args.check:
            stale.append(path.relative_to(ROOT))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8", newline="\n")
        print(f"updated {path.relative_to(ROOT)}")

    if stale:
        for path in stale:
            print(f"out of date: {path}")
        return 1
    if args.check:
        print("Claude adapters and marketplace metadata are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
