# Reading Vault

A vault for serious reading notes and critical reflection. It keeps three kinds of work apart:

| Note | One per | Purpose |
|------|---------|---------|
| **Source** (`2-Sources/`) | work read | Understand the author accurately: starting beliefs, the author's argument in their own terms, dated sessions, quotes with page references, closing assessment |
| **Reflection** (`3-Reflections/`) | claim | My own critical writing: provisional thesis, argument, strongest objection, what would change my mind |
| **Journey** (`1-Journeys/`) | ongoing inquiry | How my thinking develops: guiding question, reading path, disagreements between sources, dated changes of mind |

A reflection is not a longer book summary. It makes a claim I can defend, and possibly revise.
For example, the Journey *"When is expertise a legitimate form of authority?"* collects Source
notes on individual books, and my own answer to that question becomes one or more Reflections.

## Setup

```sh
# from the LogPose repo, with its venv active
logpose init vault-templates/reading_config.yaml -o ~/obsidian-vaults
cd ~/obsidian-vaults/ReadingVault
git init
```

`init` builds the folders and indexes, marks the vault as tracked, and copies the note
templates into `0-Meta/Templates/`. It also copies a vault-specific `CLAUDE.md` into `assets/`.

Suggested vault `.gitignore`:

```gitignore
.DS_Store
.obsidian/workspace*.json
.trash/
assets/
```

In Obsidian, open the folder as a vault, then:
- **Settings → Core plugins → Templates**: turn it on, set *Template folder location* to
  `0-Meta/Templates` and *Date format* to `YYYY-MM-DD`.
- **Settings → Files and links → Default location for new attachments**: optional.
  `logpose update` moves images and videos into `0-Meta/Media/` either way.

## Workflow

1. **Start a work.** Create a note in `2-Sources/` and insert the *Source* template. Write
   *What I believe before reading* before you read anything.
2. **Each sitting.** Insert the *Session* template under *Reading sessions*. Use quotes and
   paraphrases with page numbers, and mark your own reactions with **Me:**.
3. **Finish a work.** Complete *The author's argument*, then the *Closing assessment*.
4. **Periodically.** When one question keeps coming back, make a *Reflection* titled as a
   claim. Run the summary test in the template.
5. **When your understanding shifts.** Add a dated entry to the Journey's *Changes of mind*
   and rewrite *Where I stand now*.

Put items for the reading queue or follow-ups on their own lines tagged `#todo`, usually
under a Journey's *Next to read*. `logpose todo` gathers them into per-section TODO files
and a dashboard at `0-Meta/TODOList.md`.

## Maintenance

Always pass the reading config. Without it, LogPose falls back to `default_config.yaml`
and creates `4-Media/` folders in this vault.

```sh
logpose update ~/obsidian-vaults/ReadingVault --config vault-templates/reading_config.yaml
logpose todo   ~/obsidian-vaults/ReadingVault --config vault-templates/reading_config.yaml
```

## Using Claude with this vault

Run Claude Code from inside the vault directory, not the LogPose repo. That gives the
vault its own Claude memory, kept apart from LogPose development. `assets/CLAUDE.md` sets
Claude up as a sparring partner (objections, summary checks, checking your reconstruction
of the author) and bars it from writing your theses or assessments.

Note: `logpose update` also writes a `TemplatesINDEX.md` into `0-Meta/Templates/`, so it
shows up in Obsidian's template picker. Ignore it.
