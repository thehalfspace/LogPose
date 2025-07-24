
import os
from pathlib import Path


def update_readme(path: Path):
    readme_path = path / "readme.md"
    try:
        lines = [f"# {path.name}\n", "Backlink: [[README]]\n", "## Updated Contents:\n"]
        for item in sorted(path.iterdir()):
            if item.name == "readme.md":
                continue
            if item.is_dir():
                sub_readme = item / "readme.md"
                if not sub_readme.exists():
                    sub_readme.write_text(f"# {item.name}\nBacklink: [[{path.name}/readme]]\n")
                lines.append(f"- [[{item.name}/readme|{item.name}]]\n")
            else:
                lines.append(f"- [[{item.name}]]\n")
        readme_path.write_text("".join(lines))
        print(f"✅ Updated {readme_path}")
    except Exception as e:
        print(f"❌ Failed to update {path}: {e}")


def walk_and_update(vault_path: Path):
    for dirpath, _, _ in os.walk(vault_path):
        path = Path(dirpath)
        if not path.name.startswith("."):
            update_readme(path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Update Obsidian vault folder indexes.")
    parser.add_argument("vault_path", type=Path, help="Path to the Obsidian vault.")
    args = parser.parse_args()
    walk_and_update(args.vault_path)


if __name__ == "__main__":
    main()
