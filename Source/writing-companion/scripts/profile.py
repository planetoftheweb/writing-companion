#!/usr/bin/env python3
"""Validate and export writing profiles. Standard library only; no network or account access."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import zipfile

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
KINDS = {"global", "workspace", "project", "content-type"}
ROLES = {"voice", "rules", "context", "style", "template", "format-instructions"}
NAMES = {"voice": "soul.md", "rules": "rules.md", "style": "voice.md",
         "template": "template.md", "format-instructions": "ai-instructions.md"}
FOLDERS = {"global": "global", "workspace": "workspaces", "project": "projects",
           "content-type": "content-types"}
MAX_ARCHIVE = 25_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def slug(value):
    return isinstance(value, str) and len(value) <= 48 and bool(SLUG.fullmatch(value))


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate(data):
    require(isinstance(data, dict), "The profile must be an object.")
    require(data.get("format") == "writing-companion-profile" and data.get("version") == 1,
            "Use writing-companion-profile version 1.")
    require(slug(data.get("profileId")), "Give the profile a stable lowercase ID.")
    scopes, entries = data.get("scopes"), data.get("entries")
    require(isinstance(scopes, list) and 1 <= len(scopes) <= 100, "Use 1–100 scopes.")
    require(isinstance(entries, list) and len(entries) <= 500, "Use at most 500 entries.")
    by_id = {}
    for scope in scopes:
        require(isinstance(scope, dict) and slug(scope.get("id")), "Invalid scope ID.")
        require(scope["id"] not in by_id, "Scope IDs must be unique.")
        require(scope.get("kind") in KINDS and nonempty(scope.get("name")), "Invalid scope.")
        by_id[scope["id"]] = scope
    require("global" in by_id and by_id["global"]["kind"] == "global", "Include the global scope.")
    for scope in scopes:
        if scope["kind"] == "global":
            require(scope["id"] == "global" and scope.get("parent") is None, "Use one global root.")
            continue
        parent = scope.get("parent")
        require(isinstance(parent, str) and parent in by_id, "Every scope needs an existing parent.")
        allowed = {"workspace": {"global"}, "project": {"global", "workspace"},
                   "content-type": {"global", "workspace", "project"}}[scope["kind"]]
        require(by_id[parent]["kind"] in allowed, "Invalid scope relationship.")
    ids, paths = set(), set()
    formats = defaultdict(dict)
    for entry in entries:
        require(isinstance(entry, dict) and slug(entry.get("id")), "Invalid entry ID.")
        require(entry["id"] not in ids, "Entry IDs must be unique.")
        ids.add(entry["id"])
        scope_id, role = entry.get("scope"), entry.get("role")
        require(isinstance(scope_id, str) and scope_id in by_id and role in ROLES, "Invalid entry scope or role.")
        require(entry.get("status") in {"approved", "draft"}, "Mark each entry approved or draft.")
        text = entry.get("text")
        require(nonempty(text) and len(text.encode("utf-16-le")) // 2 <= 20_000,
                "Each entry needs text of at most 20,000 UTF-16 units.")
        evidence = entry.get("evidence")
        require(isinstance(evidence, list) and all(nonempty(item) for item in evidence), "Evidence must be a list of source labels.")
        require(entry["status"] != "approved" or evidence, "Approved entries need an approval/evidence label.")
        kind = by_id[scope_id]["kind"]
        allowed = {"global": {"voice", "rules", "context"}, "workspace": {"context", "style"},
                   "project": {"context", "style"}, "content-type": {"template", "format-instructions"}}[kind]
        require(role in allowed, "That role belongs in a different scope.")
        if role == "context":
            name = entry.get("name")
            require(isinstance(name, str) and name.endswith(".md") and slug(name[:-3])
                    and name != "soul.md", "Use a short context filename other than soul.md.")
        path = entry_path(entry, by_id)
        require(path not in paths, "Two entries would overwrite the same file.")
        paths.add(path)
        if kind == "content-type":
            formats[scope_id][role] = entry["status"]
    for pair in formats.values():
        require(set(pair) == {"template", "format-instructions"} and len(set(pair.values())) == 1,
                "A content format needs both a template and instructions with the same status.")
    require(isinstance(data.get("session", {}), dict), "Session checkpoint must be an object.")
    changes = data.get("changes", [])
    require(isinstance(changes, list) and all(nonempty(item) for item in changes), "Changes must be short text entries.")
    return by_id


def entry_path(entry, scopes):
    scope = scopes[entry["scope"]]
    folder = FOLDERS[scope["kind"]]
    if scope["kind"] != "global":
        folder += "/" + scope["id"]
    name = NAMES.get(entry["role"], entry.get("name"))
    return f"{folder}/{name}"


def read_archive(path):
    """Read only known snapshot members. Never extract user-provided ZIP paths."""
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        require(len(infos) <= 10000 and sum(i.file_size for i in infos) <= MAX_ARCHIVE,
                "This profile archive is too large.")
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), "Duplicate archive members are not supported.")
        current = json.loads(archive.read("snapshot.json"))
        scopes = validate(current)
        revision = current.get("revision")
        require(type(revision) is int and 1 <= revision <= 1000, "Invalid saved revision.")
        for entry in current["entries"]:
            name = entry_path(entry, scopes)
            if entry["status"] == "draft":
                name = "drafts/" + name
            require(archive.read(name) == entry["text"].encode("utf-8"),
                    "A guidance file differs from its snapshot. Review the edited text before continuing.")
        history = []
        for number in range(1, revision):
            old = json.loads(archive.read(f"history/revision-{number:04d}.json"))
            validate(old)
            require(old.get("revision") == number and old["profileId"] == current["profileId"],
                    "The profile history is inconsistent.")
            history.append(old)
        return current, history


def render(data, scopes, revision):
    files, index_entries = {}, []
    readable = ["# My writing profile", f"Profile: {data['profileId']} · Revision: {revision}",
                "Only the approved sections below guide writing. Apply the selected scope and its parents. "
                "The checkpoint is unfinished work, not writing instructions."]
    for scope in data["scopes"]:
        readable += [f"## {scope['name']}", f"Scope: {scope['id']} ({scope['kind']}); parent: {scope.get('parent') or 'none'}"]
        for entry in data["entries"]:
            if entry["scope"] != scope["id"]:
                continue
            path = entry_path(entry, scopes)
            if entry["status"] == "draft":
                path = "drafts/" + path
            raw = entry["text"].encode("utf-8")
            files[path] = raw
            index_entries.append({key: entry[key] for key in ("id", "scope", "role", "status", "evidence")} |
                                 {"path": path, "sha256": hashlib.sha256(raw).hexdigest()})
            if entry["status"] != "approved":
                continue
            readable += [f"### {entry['role'].replace('-', ' ').title()}", entry["text"]]
    readable += ["## Session checkpoint (not approved guidance)",
                 json.dumps(data.get("session", {}), ensure_ascii=False, indent=2),
                 "## Pending profile entries (not approved guidance)"]
    for entry in data["entries"]:
        if entry["status"] == "draft":
            readable += [f"### Draft: {entry['id']} ({entry['scope']})", entry["text"]]
    files["writing-profile.md"] = ("\n\n".join(readable) + "\n").encode("utf-8")
    files["index.json"] = encode({"format": "writing-companion-index", "version": 1,
                                   "profileId": data["profileId"], "revision": revision,
                                   "scopes": data["scopes"], "entries": index_entries})
    return files


def export_profile(data, output, previous=None):
    scopes = validate(data)
    history = []
    if previous:
        old, history = read_archive(previous)
        require(old["profileId"] == data["profileId"], "Cannot merge different writing profiles.")
        require(data.get("baseRevision") == old["revision"], "Reload the latest profile before creating a revision.")
        require(bool(data.get("changes")), "Describe the approved changes or checkpoint update.")
        history.append(old)
    else:
        require(data.get("baseRevision") in (None, 0), "Supply the previous ZIP to preserve existing history.")
    revision = len(history) + 1
    require(revision <= 1000, "Archive this history before starting a new profile history.")
    snapshot = dict(data, revision=revision, savedAt=datetime.now(timezone.utc).isoformat())
    files = render(snapshot, scopes, revision)
    files["snapshot.json"] = encode(snapshot)
    files["session.json"] = encode(data.get("session", {}))
    for old in history:
        files[f"history/revision-{old['revision']:04d}.json"] = encode(old)
    files["changes.md"] = ("# Profile changes\n\n" + "\n\n".join(
        f"## Revision {item['revision']}\n" + "\n".join("- " + change for change in item.get("changes", []))
        for item in [*history, snapshot]) + "\n").encode("utf-8")
    require(sum(len(raw) for raw in files.values()) <= MAX_ARCHIVE, "Export exceeds the profile archive limit.")
    output = Path(output)
    # Exclusive creation preserves the previous archive and any existing output.
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw)
    return revision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("input", type=Path)
    export = sub.add_parser("export")
    export.add_argument("input", type=Path)
    export.add_argument("output", type=Path)
    export.add_argument("--previous", type=Path)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            current, history = read_archive(args.archive)
            print(json.dumps({"profileId": current["profileId"], "revision": current["revision"],
                              "entries": len(current["entries"]), "previousRevisions": len(history)}, indent=2))
        else:
            data = json.loads(args.input.read_text(encoding="utf-8"))
            validate(data)
            if args.command == "validate":
                print("Profile is valid.")
            else:
                revision = export_profile(data, args.output, args.previous)
                print(f"Exported revision {revision} to {args.output}")
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Profile could not be processed: {error}\n")


if __name__ == "__main__":
    main()
