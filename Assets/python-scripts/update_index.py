
import os
from pathlib import Path


def strip_prefix(name: str) -> str:
    return name.split('-', 1)[-1] if '-' in name else name


def get_backlinks(path: Path, vault_root: Path, vault_index_name: str) -> list:
    backlinks = []
    if path != vault_root:
        backlinks.append(f"[[{vault_index_name}]]")
        relative_path = path.relative_to(vault_root)
        parents = list(relative_path.parents)
        current = vault_root
        for p in reversed(parents):
            if p.name:
                current = current / p.name
                label = strip_prefix(p.name)
                backlinks.append(f"[[{current.name}/{label}INDEX|{label}]]")
    return backlinks


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


def walk_and_update(vault_path: Path, vault_index_name: str):
    for dirpath, _, _ in os.walk(vault_path):
        path = Path(dirpath)
        if path.name == ".obsidian" or path.name.startswith("."):
            continue
        update_readme(path, vault_path, vault_index_name)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Update Obsidian vault folder indexes.")
    parser.add_argument("vault_path", type=Path, help="Path to the Obsidian vault.")
    parser.add_argument("--vault_name", type=str, required=True, help="Name of the vault (used to find top index).")
    args = parser.parse_args()
    vault_index_name = f"{args.vault_name}INDEX"
    walk_and_update(args.vault_path, vault_index_name)


if __name__ == "__main__":
    main()
