# Agents

This directory holds the **source-of-truth** for Rogue Night's named agents and the skills they use. The agents themselves run on the Hyperagent platform — this directory is the version-controlled mirror, so the configurations survive across sessions, can be diffed in PRs, and can be reconstructed if Hyperagent state is ever lost.

## What's here

- **[`lois/`](lois/)** — Lois, the named Digital Health Check report-writing agent
- **[`dhc-report-writer/`](dhc-report-writer/)** — Skill that turns one Airtable Response into a populated DHC report
- **[`stack-md-maintainer/`](stack-md-maintainer/)** — Skill that keeps `catalogue/stack.md` and the Airtable Tools table in sync

## Relationship between this repo and Hyperagent

- **System prompts and skill documentation** live in `agents/*/README.md` and `agents/lois/system-prompt.md`. The Hyperagent platform reads these (when manually loaded via "Save as Agent" or skill creation flows) and stores its own copy for runtime use.
- **Skill scripts** live in `agents/*/scripts/`. Hyperagent fetches these into `/agent/workspace/skills/{skill-name}/` at runtime via `FetchSkillScripts`. After editing scripts here, push the changes to Hyperagent via `UpdateSkillAndScripts`.
- **Skill data** (mock responses, brand assets, example vars) lives in `agents/*/data/`. Same fetch-into-workspace pattern.
- **Credentials** (Airtable API keys, Stripe keys) are never stored in this repo — they live in Hyperagent's secrets store, injected at script execution time.

## Editing flow

1. Edit the file here (e.g., `agents/dhc-report-writer/scripts/match_recommendations.py`).
2. Commit and push.
3. In a Hyperagent thread, run `FetchSkillScripts({skillName: "Rogue Night DHC Report Writer", force: true})` to overwrite the workspace copy with the new version, then `UpdateSkillAndScripts` to save it back to the skill DB.

Or skip the round-trip and:

1. Edit in Hyperagent workspace.
2. Save via `UpdateSkillAndScripts`.
3. Pull the result back into this repo (copy the script file from the Hyperagent workspace into `agents/*/scripts/` and commit).

Both flows work — pick the one that suits the change.

## Known issue (2026-05-13)

The Hyperagent `UpdateSkillAndScripts.scripts` parameter has a validation quirk that prevented script registration during the migration from in-thread workspace to the skill DB. The scripts in this repo are the **canonical versions**; if a Hyperagent skill drifts from these (e.g., due to that bug or a stale fetch), this repo wins.

Resolution: run `UpdateSkillAndScripts` manually with each script's path until the bug is fixed upstream, or paste script content into the skill via the platform UI.

## Voice rules

Same as the rest of the repo. See [`docs/operations/VOICE-RULES.md`](../docs/operations/VOICE-RULES.md).

The DHC Report Writer skill bakes the voice rules into its drafting methodology (Phase 1 brand non-negotiables, locked). The Stack.md Maintainer skill auto-cleans SME → small business in any field it writes.
