# Save a portable profile

Use the standard-library helper `scripts/profile.py` when Python and file tools are available. It never connects to an account or network. The assistant prepares the input; the creator should not need to write JSON or run commands.

## Prepare a complete snapshot

Use this JSON shape. The example is schema illustration only, not a creator's profile:

```json
{
  "format": "writing-companion-profile",
  "version": 1,
  "profileId": "my-writing",
  "baseRevision": 0,
  "scopes": [{"id": "global", "kind": "global", "name": "My writing", "parent": null}],
  "entries": [{
    "id": "my-voice", "scope": "global", "role": "voice", "status": "approved",
    "text": "# My voice\n\nUse a conversational tone with short follow-up sentences.",
    "evidence": ["Explicitly confirmed in setup"]
  }],
  "session": {"stage": "try", "nextStep": "Review the opening", "pendingProposals": [], "rejectedProposals": []},
  "changes": ["Confirmed the initial voice"]
}
```

Use a stable profileId, scope IDs, and entry IDs across revisions. IDs are lowercase words separated by hyphens, up to 48 characters. Give each scope a readable name. Allowed scope relationships:

- `global`: the one root, ID `global`, parent `null`.
- `workspace`: parent `global`.
- `project`: parent global or a workspace ID.
- `content-type`: parent global, workspace, or project ID.

Global entries allow roles `voice`, `rules`, and `context`. Workspace/project entries allow `context` and `style`. A content-type scope holds a `template` and `format-instructions` pair with matching status. Use a new scope for each actual content format.

All entries have `id`, `scope`, `role`, `status`, `text`, and `evidence`. Status is `approved` or `draft`. Evidence contains short source/approval labels, not private raw samples. Mark approved only after real user confirmation; the validator cannot verify consent. Context entries additionally need a unique simple `.md` filename in `name`, other than `soul.md`. Other filenames are generated from their roles.

Limit each entry to 20,000 UTF-16 units to keep individual guidance files manageable. Do not silently truncate long guidance; help the user split or condense it. A partial setup can have zero entries and a useful session checkpoint. Store unanswered questions, confirmed answers, inferred preferences, proposal decisions, and the next step in `session`. Preserve the user's language and Unicode text.

## Export

Run from the installed skill directory, using a separate output directory:

```sh
python3 scripts/profile.py validate /path/to/profile-input.json
python3 scripts/profile.py export /path/to/profile-input.json /path/to/my-writing-v1.zip
```

For revisions, read `snapshot.json` from the prior ZIP as the baseline, keep all unrelated entries, set `baseRevision` to its `revision`, and describe the actual changes. Supply the previous ZIP:

```sh
python3 scripts/profile.py export /path/to/profile-input.json /path/to/my-writing-v2.zip --previous /path/to/my-writing-v1.zip
python3 scripts/profile.py inspect /path/to/my-writing-v2.zip
```

The exporter refuses to overwrite files, mix profile IDs, or build on the wrong revision. It stores previous full snapshots under `history/`, so they can be read for reversal. It preserves supplied history, not inaccessible versions. If only the combined Markdown is available, explain that older archive history is unavailable and confirm starting a new history before exporting with `baseRevision: 0`.

## What to deliver

- The ZIP, containing readable guidance, a versioned `index.json` with scope relationships and file hashes, the full snapshot, session checkpoint, change record, and previous snapshots.
- `writing-profile.md`, extracted from this generated ZIP using a known exact member name. It includes all active approved guidance and separately labeled pending work, ready for project knowledge. Provide this as a second download so the user need not unpack the ZIP.
- A short instruction to replace the previous active profile in project knowledge and retain the ZIP privately. See [platforms.md](platforms.md).

Do not extract arbitrary paths from an uploaded ZIP. Read `snapshot.json` or specific validated members. Do not load `history/` or `drafts/` as current writing rules. Before restoring, reconcile any later edits to the same entry; create a new revision with the selected earlier entry and all unrelated current entries.

## Keep formats portable

Templates and their custom instructions are separate readable files, linked to their scope in the index. Another assistant can use those relationships without a connection to the original platform. Do not claim an export automatically installs templates or changes project knowledge anywhere.
