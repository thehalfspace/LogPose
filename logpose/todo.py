
from pathlib import Path
import yaml

def is_index_file(path: Path) -> bool:
    return path.name.endswith("INDEX.md")

def extract_todo_lines(file_path: Path, vault_path: Path):
    todos = []
    if not file_path.is_file() or is_index_file(file_path):
        return todos

    try:
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        if any("#ignoretodo" in line for line in lines):
            return todos

        for line in lines:
            if "#todo" in line:
                clean_line = line.strip().replace("#todo", "").strip()
                relative_link = file_path.relative_to(vault_path)
                todos.append(f"- [ ] {clean_line} ([[{relative_link}]])")
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return todos

def get_todolist_path(vault_path: Path, config_path: Path) -> Path:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return vault_path / config["todolist"]["location"]
    except Exception as e:
        print(f"❌ Could not determine todolist path from config: {e}")
        return vault_path / "0-Assets/TODOList.md"

def generate_todolist(vault_path: Path, config_path: Path):
    output_file = get_todolist_path(vault_path, config_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    all_todos = []
    for file_path in vault_path.rglob("*.md"):
        if file_path.name in ["TODOList.md"] or file_path.name.endswith("INDEX.md"):
            continue
        all_todos.extend(extract_todo_lines(file_path, vault_path))

    with output_file.open("w", encoding="utf-8") as f:
        f.write("# 📝 Global TODO List\n\n")
        if not all_todos:
            f.write("No tasks found.")
        else:
            f.write("\n".join(all_todos))
    print(f"✅ TODO list written to: {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate TODOList.md from Obsidian notes.")
    parser.add_argument("vault_path", type=Path, help="Path to your Obsidian vault")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent.parent / "vault-templates/default_config.yaml")
    args = parser.parse_args()
    generate_todolist(args.vault_path, args.config)
