from pathlib import Path
import yaml
import hashlib
import re

def is_index_file(path: Path) -> bool:
    return path.name.endswith("INDEX.md")

def hash_todo_content(content: str) -> str:
    return hashlib.md5(content.strip().encode('utf-8')).hexdigest()

def extract_todo_lines(file_path: Path, vault_path: Path):
    todos = []
    if not file_path.is_file() or is_index_file(file_path):
        return todos

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()

        if any("#ignoretodo" in line for line in lines):
            return todos

        for line in lines:
            if "#todo" in line:
                clean_line = line.strip().replace("#todo", "").strip()
                relative_link = file_path.relative_to(vault_path)
                content = f"{clean_line} ([[{relative_link}]])"
                todo_hash = hash_todo_content(content)
                todos.append((todo_hash, f"- [ ] {content}"))
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return todos

def parse_existing_todolist(todolist_file: Path):
    existing_lines = []
    existing_hash_map = {}
    todo_pattern = re.compile(r"^- \[( |x)\] (.+)$")

    if not todolist_file.exists():
        return existing_lines, existing_hash_map

    lines = todolist_file.read_text(encoding="utf-8").splitlines()
    for line in lines:
        match = todo_pattern.match(line)
        if match:
            content = match.group(2).strip()
            todo_hash = hash_todo_content(content)
            existing_lines.append(line)
            existing_hash_map[todo_hash] = line
        else:
            existing_lines.append(line)  # Keep headers or comments intact
    return existing_lines, existing_hash_map

def generate_project_todolists(vault_path: Path):
    folder_todo_map = {}

    for file_path in vault_path.rglob("*.md"):
        if is_index_file(file_path):
            continue
        if file_path.name.endswith("TODO.md"):
            continue
        rel_path = file_path.relative_to(vault_path)
        parts = rel_path.parts
        if len(parts) < 2:
            continue
        project_root = vault_path / parts[0] / parts[1]
        todos = extract_todo_lines(file_path, vault_path)
        if todos:
            folder_todo_map.setdefault(project_root, []).extend(todos)

    for folder, todos in folder_todo_map.items():
        project_name = folder.name
        output_file = folder / f"{project_name}TODO.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        existing_lines, existing_hash_map = parse_existing_todolist(output_file)

        # Append only new tasks
        for todo_hash, line in todos:
            if todo_hash not in existing_hash_map:
                existing_lines.append(line)

        with output_file.open("w", encoding="utf-8") as f:
            f.write("\n".join(existing_lines) + "\n")
        print(f"✅ Project TODO written to: {output_file}")

    return folder_todo_map

def generate_dashboard(vault_path: Path, config_path: Path, folder_map: dict):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        dashboard_rel = Path(config["todolist"]["location"])
    except Exception as e:
        print(f"❌ Could not read dashboard path from config: {e}")
        return

    dashboard_path = vault_path / dashboard_rel
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    with dashboard_path.open("w", encoding="utf-8") as f:
        f.write("# 📋 Global TODO Dashboard\n\n")
        if not folder_map:
            f.write("No TODOs found in the vault.")
        else:
            for folder in sorted(folder_map):
                rel = folder.relative_to(vault_path)
                project_todo_file = f"{folder.name}TODO"
                f.write(f"- 📁 [[{rel}/{project_todo_file}]]\n")
    print(f"📊 Global Dashboard updated at: {dashboard_path}")

def generate_todolists(vault_path: Path, config_path: Path):
    folder_map = generate_project_todolists(vault_path)
    generate_dashboard(vault_path, config_path, folder_map)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate project-specific TODOs and dashboard.")
    parser.add_argument("vault_path", type=Path, help="Path to your Obsidian vault")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent.parent / "vault-templates/default_config.yaml")
    args = parser.parse_args()

    generate_todolists(args.vault_path, args.config)

if __name__ == "__main__":
    main()