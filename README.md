# LogPose
**LogPose** is a command-line toolkit for managing structured [Obsidian](https://obsidian.md) vaults. Inspired by One Piece's Log Pose, it helps you navigate, organize, and automate knowledge management usingsimple Python CLI.

## Setup
Requirements:
1. Python (>=3.9)
2. [uv](https://github.com/astral-sh/uv)
3. Obsidian

---

## Installation
```sh
cd logpose

# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate

# Install CLI
uv pip install -e .
```

---

## 📦 Features

- 🔒 `track`: Mark a folder as LogPose-tracked (`vault` or `assets` role). Every other command refuses to run on an untracked folder — this is a safety guard against accidentally indexing, rewriting, or moving files in the wrong directory.
- 🔨 `init`: Initialize a new vault from a configurable YAML template. Auto-tracks the vault as it's created.
- 🔁 `update`: Automatically generate backlink-aware index files for each folder, including into linked project folders (see `link` below). Optionally moves loose images/videos into the vault's media folders (never reaches into linked project folders for this).
- 🗒 `todo`: Aggregate `#todo` tags across your vault (and linked project folders) into per-project todo files, plus a global dashboard.
- 🔗 `link`: Symlink another project's `assets/` folder into a vault's `1-Assets/` folder, so its notes show up alongside the vault's own content — browsable and editable in Obsidian, indexed and todo-scanned by `update`/`todo`, but still physically stored (and git-backed) in the original project.
- ✅ (WIP incomplete) `kanban`: Generate kanban-style Markdown boards and task completion graphs.
- 💾 (WIP incomplete) `backup`: Save `.obsidian/*.json` settings to version-controlled backups. Also backup the vault as a submodule in another github repo.

---

## Usage
Vaults live outside this repo (e.g. `~/obsidian-vaults/MyVault/`), managed as their own git repositories. Every folder LogPose touches — vaults and linked project `assets/` folders alike — must be tracked first with `logpose track`. `init` tracks a new vault automatically.

```sh
# One-time: track a project's assets/ folder so it can be linked into a vault
logpose track ~/2025/projects/batnav/assets --role assets

# Create a vault (auto-tracked with role "vault"). If --vault_path/-o is
# omitted, the vault is created as ./<vault_name> in the current directory.
logpose init vault-templates/default_config.yaml --vault_path ~/obsidian-vaults

# Link the project's assets/ into the vault's 1-Assets/ folder
logpose link ~/2025/projects/batnav/assets ~/obsidian-vaults/MyVault --as batnav

# Regenerate indexes (walks into linked folders too) and move stray media
logpose update ~/obsidian-vaults/MyVault/ --config vault-templates/default_config.yaml

# Aggregate #todo tags (including from linked folders) into per-project + global todolists
logpose todo ~/obsidian-vaults/MyVault/ --config vault-templates/default_config.yaml

logpose kanban ~/obsidian-vaults/MyVault/ # WIP
logpose backup ~/obsidian-vaults/MyVault/ ~/obsidian-vaults/MyVault/0-Assets/config/    # WIP
```

For a vault whose sole purpose is aggregating other projects' `assets/` folders (rather than being a general project/todo vault), use `vault-templates/notes_vault_config.yaml` instead of `default_config.yaml`.

---

## 📸 Screenshots
<img src="https://github.com/thehalfspace/LogPose/blob/main/Index_Example.png" alt="drawing" width="600"/>
<img src="https://github.com/thehalfspace/LogPose/blob/main/Todo_Example.png" alt="drawing" width="600"/>

---

## 📁 Directory Structure

