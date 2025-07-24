
# LogPose

A toolkit to create, maintain, and visualize a structured Obsidian vault.

## Scripts

- `Assets/python-scripts/initialize_vault.py`: Create a new vault from YAML structure
- `Assets/python-scripts/iupdate_index.py`: Update all folder-level readmes with internal links
- `Assets/python-scripts/ibackup_obsidian_config.py`: Backup Obsidian `.obsidian/*.json` config
- `Assets/python-scripts/igenerate_kanban_and_graphs.py`: Generate Kanban + task progress graph

## Setup
Requirements:
1. Python (>=3.9)
2. uv
3. Obsidian

```bash
uv sync
uv venv pyenv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

```bash
python Assets/python-scripts/iinitialize_vault.py Assets/vault-templates/vault_config.yaml
python Assets/python-scripts/iupdate_index.py MyVault/
python Assets/python-scripts/ibackup_obsidian_config.py MyVault/ MyVault/0-Assets/config/
python Assets/python-scripts/igenerate_kanban_and_graphs.py MyVault/6-Logbook/todolist.md MyVault/7-Visualizations/kanban.md MyVault/7-Visualizations/progress.png
```
