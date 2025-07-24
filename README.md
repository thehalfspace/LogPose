
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
source pyenv/bin/activate
uv pip install -r requirements.txt
```

## Usage

```bash
# Create new obsidian vault, you can edit the default_config.yaml to create your own folder structure
python Assets/python-scripts/initialize_vault.py Assets/vault-templates/default_config.yaml

# Once the above step is done, you can open obsidian and open vault from folder.

# Periodically index the backlinks for obsidian
python Assets/python-scripts/update_index.py --vault_name=MyVault MyVault/

# Create a TODOList.md in 6-Logbook folder. This script will scan all the .md files that are not *INDEX.md, look for the tag #todo, and create a list from the lines that contain the #todo tag. It will ignore the files that contain #ignoretodo, and it will add completed check marks to the lines that contain #done.
python Assetes/python-scripts/generate_todolist MyVault/

# WIP: backup the obsidian settings and generate visualizations
python Assets/python-scripts/backup_obsidian_config.py MyVault/ MyVault/0-Assets/config/
python Assets/python-scripts/generate_kanban_and_graphs.py MyVault/6-Logbook/todolist.md MyVault/7-Visualizations/kanban.md MyVault/7-Visualizations/progress.png
```

Testing example: run the `initialize_vault.py` script, then open obsidian, and create a few random notes in different subfolders. Then run the `update_index.py` script. You can keep obsidian open while running the `update_index.py` script.

# Features to add:
- To do list in logbook: a python script to generate and update todo list by:
    - searching the tag #todo everywhere except for index files. 
    - adding a backlink to the note where #todo is mentioned for that tag. 
    - once project is complete, I will manually add tag #done, adjacent to #todo, the python script will search done tag and strikethrough the todo. Alternatively, if a completed task is back again in agenda, the script can mark it undone again.
    - (Brainstorm a better workflow for this): a python script that will archive the older todolist (e.g., todoarchive-timestamp.md), and copy the unfinished tasks into the current todolist (e.g., todoCurrent.md).

- Right now I don't have any backup for the vault, only git version control for python. Come up with some vault backup strategy.
