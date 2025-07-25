import os
from pathlib import Path
import argparse

def strip_prefix(name: str) -> str:
    return name.split("-", 1)[-1] if "-" in name else name

def get_backlinks(path: Path, vault_root: Path, vault_index_name: str) -> list:
    backlinks = []
    current = path
    while current != vault_root.parent:
        if current == vault_root:
            backlinks.append(f"[[{vault_index_name}]]")
        else:
            name_stripped = strip_prefix(current.name)
            backlinks.append(f"[[{current.name}/{name_stripped}INDEX]]")
        current = current.parent
    return list(reversed(backlinks))

def update_readme(path: Path, vault_root: Path, vault_index_name: str):
    name_stripped = strip_prefix(path.name)
    readme_name = f"{name_stripped}INDEX.md"
    readme_path = path / readme_name

    try:
        lines = [f"# {name_stripped}\n"]

        backlinks = get_backlinks(path, vault_root, vault_index_name)
        if backlinks:
            lines.append("Backlinks: " + " ← ".join(backlinks) + "\n\n")

        lines.append("## Contents:\n")
        for item in sorted(path.iterdir()):
            if item.name == readme_name or item.name.startswith("."):
                continue
            if item.is_dir():
                sub_name = strip_prefix(item.name)
                lines.append(f"- [[{item.name}/{sub_name}INDEX|{sub_name}]]\n")
            else:
                lines.append(f"- [[{item.name}]]\n")

        readme_path.write_text("".join(lines), encoding="utf-8")
        print(f"✅ Updated {readme_path}")
    except Exception as e:
        print(f"❌ Failed to update {path}: {e}")

def walk_and_update(vault_path: Path, vault_name: str):
    for dirpath, _, _ in os.walk(vault_path):
        path = Path(dirpath)
        if not path.name.startswith(".") and path.is_dir():
            update_readme(path, vault_path, f"{vault_name}INDEX")

def update_indexes(vault_path: Path, vault_name: str = None):
    walk_and_update(vault_path, vault_name or vault_path.name)

def main():
    parser = argparse.ArgumentParser(description="Update Obsidian vault folder indexes.")
    parser.add_argument("vault_path", type=Path, help="Path to the Obsidian vault.")
    parser.add_argument("--vault_name", type=str, help="Optional vault name (used in backlink)")
    args = parser.parse_args()
    walk_and_update(args.vault_path, args.vault_name or args.vault_path.name)

if __name__ == "__main__":
    main()