# LogPose
**LogPose** is a command-line toolkit for managing structured [Obsidian](https://obsidian.md) vaults. Inspired by One Piece's Log Pose, it helps you navigate, organize, and automate knowledge management using a powerful Python CLI.

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
- 🗒 `todo`: Aggregate global `#todo` tags across your vault into a checklist.
- ✅ `kanban`: Generate kanban-style Markdown boards and task completion graphs.
- 💾 `backup`: Save `.obsidian/*.json` settings to version-controlled backups.

---

## Usage
```sh
logpose init vault-templates/default_config.yaml
logpose update MyVault/ --vault_name MyVault
logpose todo MyVault/
logpose kanban MyVault/
logpose backup MyVault/ MyVault/0-Assets/config/

```

## 📁 Directory Structure

