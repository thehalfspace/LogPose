
from pathlib import Path


def is_index_file(path: Path) -> bool:
    return path.name.endswith("INDEX.md")


def extract_todo_lines(file_path: Path, vault_path: Path):
    todos = []
    if not file_path.is_file() or is_index_file(file_path):
        return todos

    try:
        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Skip entire file if #ignoretodo is present
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


def generate_todolist(vault_path: Path):
    logbook_path = vault_path / "6-Logbook"
    output_file = logbook_path / "TODOList.md"
    logbook_path.mkdir(parents=True, exist_ok=True)

    all_todos = []

    for file_path in vault_path.rglob("*.md"):
        if file_path.name in ["TODOList.md"] or file_path.name.endswith("INDEX.md"):
            continue
        all_todos.extend(extract_todo_lines(file_path, vault_path))

    with output_file.open("w", encoding="utf-8") as f:
        f.write("# 📝 Global TODO List\n\n")
        if not all_todos:
            f.write("No tasks found.\n")
        else:
            f.write("\n".join(all_todos))

    print(f"✅ TODO list written to: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate TODOList.md from Obsidian notes.")
    parser.add_argument("vault_path", type=Path, help="Path to your Obsidian vault")
    args = parser.parse_args()

    generate_todolist(args.vault_path)
