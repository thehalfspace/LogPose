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

- 🔨 `init`: Initialize a new vault from a configurable YAML template.
- 🔁 `update`: Automatically generate backlink-aware index files for each folder.
- 🗒 `todo`: Aggregate `#todo` tags across your vault into their respective folders. Also generate a global todolist with those todo notes in your vault. 
- ✅ (WIP incomplete) `kanban`: Generate kanban-style Markdown boards and task completion graphs.
- 💾 (WIP incomplete) `backup`: Save `.obsidian/*.json` settings to version-controlled backups. Also backup the vault as a submodule in another github repo.

---

## Usage
```sh
logpose init vault-templates/default_config.yaml
logpose update MyVault/ 
logpose todo MyVault/
logpose kanban MyVault/ # WIP
logpose backup MyVault/ MyVault/0-Assets/config/    # WIP

```

## 📁 Directory Structure

