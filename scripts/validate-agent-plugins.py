#!/usr/bin/env python3
"""Validate this repository's Agent Plugins v1 packages and compatibility files."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("must contain a JSON object")
    return value


def frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---"):
        return None
    closing = text.find("\n---", 3)
    if closing < 0:
        return None
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\r\n\"']+)", text[:closing])
    return match.group(1).strip() if match else None


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        return False
    return True


def validate_plugin(plugin_root: Path) -> list[str]:
    errors: list[str] = []
    relative_root = plugin_root.relative_to(ROOT)
    manifest_path = plugin_root / "plugin.json"
    if not manifest_path.is_file():
        return [f"{relative_root}: missing regular root plugin.json"]

    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [f"{manifest_path.relative_to(ROOT)}: {error}"]

    unknown = set(manifest) - ALLOWED_FIELDS
    if unknown:
        errors.append(f"{relative_root}: unsupported manifest fields {sorted(unknown)}")
    if manifest.get("$schema") != SCHEMA:
        errors.append(f"{relative_root}: incorrect Agent Plugins schema")

    name = manifest.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name) or "--" in name or ".." in name:
        errors.append(f"{relative_root}: invalid plugin name {name!r}")
    elif name != plugin_root.name:
        errors.append(f"{relative_root}: manifest name does not match directory")

    for field in ("version", "description", "license"):
        if field in manifest and not isinstance(manifest[field], str):
            errors.append(f"{relative_root}: {field} must be a string")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append(f"{relative_root}: description is required by repository policy")
    if "keywords" in manifest and (
        not isinstance(manifest["keywords"], list)
        or not all(isinstance(value, str) for value in manifest["keywords"])
    ):
        errors.append(f"{relative_root}: keywords must be an array of strings")
    if "author" in manifest:
        author = manifest["author"]
        if not isinstance(author, dict) or set(author) - {"name", "email", "url"} or not all(
            isinstance(value, str) for value in author.values()
        ):
            errors.append(f"{relative_root}: author does not match the v1 schema")
    extensions = manifest.get("extensions", {})
    if not isinstance(extensions, dict) or not all(
        re.fullmatch(r"[a-z0-9]+(?:\.[a-z0-9-]+)+", key) and isinstance(value, dict)
        for key, value in extensions.items()
    ):
        errors.append(f"{relative_root}: invalid client extension map")

    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        errors.append(f"{relative_root}: missing skills directory")
    else:
        for skill_root in sorted(path for path in skills_root.iterdir() if path.is_dir()):
            skill_file = skill_root / "SKILL.md"
            if not skill_file.is_file():
                errors.append(f"{skill_root.relative_to(ROOT)}: missing regular SKILL.md")
                continue
            text = skill_file.read_text(encoding="utf-8")
            skill_name = frontmatter_value(text, "name")
            description = frontmatter_value(text, "description")
            if skill_name != skill_root.name:
                errors.append(
                    f"{skill_file.relative_to(ROOT)}: name {skill_name!r} does not match directory"
                )
            if not description:
                errors.append(f"{skill_file.relative_to(ROOT)}: missing description")

    for path in plugin_root.rglob("*"):
        if not is_within(path, plugin_root):
            errors.append(f"{path.relative_to(ROOT)}: resolves outside the plugin package")

    if (plugin_root / ".plugin" / "plugin.json").exists():
        errors.append(f"{relative_root}: obsolete .plugin/plugin.json remains")
    if not (plugin_root / ".claude-plugin" / "plugin.json").is_file():
        errors.append(f"{relative_root}: missing Claude Code adapter")
    if (plugin_root / ".codex-plugin").exists():
        errors.append(f"{relative_root}: obsolete Codex adapter remains")
    return errors


def main() -> int:
    sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync-plugin-metadata.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    errors = []
    if sync.returncode:
        errors.append(sync.stdout.strip() or sync.stderr.strip())

    plugin_roots = sorted(
        path for path in PLUGINS.iterdir() if path.is_dir() and (path / "plugin.json").exists()
    )
    catalog_names = {
        entry["name"] for entry in load_json(ROOT / ".github" / "plugin" / "marketplace.json")["plugins"]
    }
    if catalog_names != {path.name for path in plugin_roots}:
        errors.append("GitHub marketplace entries do not match portable plugin packages")

    for plugin_root in plugin_roots:
        errors.extend(validate_plugin(plugin_root))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    skill_count = sum(
        1 for plugin_root in plugin_roots for path in (plugin_root / "skills").iterdir() if path.is_dir()
    )
    print(
        f"Validated {len(plugin_roots)} Agent Plugins v1 packages and {skill_count} independently discoverable skills."
    )
    print("Validated package containment, Claude adapters, and marketplace synchronization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
