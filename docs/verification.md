# Verification

This records the September 2026 release. The profile and build checks now live in `tests/` and run on every push. The live platform testing below is still open.

Verified locally on September 18, 2026:

- 17 automated profile checks cover export/restart, Unicode, partial setup without samples or memory, approved versus draft guidance, rejected proposals, scope separation, format pairs, revision history, entry-level restoration, stale revisions, mixed profiles, accidental overwrite, manual edits, archive paths.
- Seven distribution checks cover the ten complete prompts, six template pairs, draft-only starter exports, embedded Project assets, reference links, archive allowlists, checksums, and protection against overwriting an existing distribution. All 24 focused tests passed.
- The two-page quickstart was generated from one Markdown source as editable Word and PDF. Both rendered pages were visually inspected after the final formatting change.
- The skill passed the skill-creator frontmatter validator.
- The optional plugin passed the plugin-creator manifest validator.
- Packaging uses an explicit source allowlist. No personal profile, raw writing sample, credentials, app connection, or MCP server is included.

Live acceptance testing remains incomplete:

- ChatGPT opened a workspace agreement. It was not acknowledged on the user's behalf, and no skill was uploaded or installed there.
- Claude opened an incognito chat, but the browser extension rejected file upload because file access was unavailable. No guide was uploaded, no prompt was submitted, and no skill was installed. Browser file-upload access must be enabled by the user before running that path.
- The full conversational scenario matrix has not been passed on either platform. Local format checks do not establish model behavior or native installation success.

The skill ZIP, Project edition, and optional plugin are prepared for installation. They have not been published to a marketplace or enabled in the user's account.

Use the included `Acceptance scenarios.md` for the remaining platform checks. A structurally valid skill does not establish that Claude or ChatGPT installed or followed it correctly.
