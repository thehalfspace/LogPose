
#!/usr/bin/env python3
import sys
import argparse
import yaml
from pathlib import Path


def strip_prefix(name: str) -> str:
    return name.split('-', 1)[-1] if '-' in name else name


def create_readme(folder_path: Path, backlink: str) -> None:
    name_stripped = strip_prefix(folder_path.name)
    readme_name = f"{name_stripped}INDEX.md"
    readme_path = folder_path / readme_name
    if readme_path.exists():
        print(f"⚠️  Skipping existing index: {readme_path}")
        return

    try:
        content = [
            f"# {name_stripped}\n",
            f"Backlink: {backlink}\n",
            "## Contents:\n"
        ]
        for item in sorted(folder_path.iterdir()):
            if item.name == readme_name:
                continue
            if item.is_dir():
                sub_name = strip_prefix(item.name)
                content.append(f"- [[{item.name}/{sub_name}INDEX|{sub_name}]]\n")
            else:
                content.append(f"- [[{item.name}]]\n")

        readme_path.write_text("".join(content), encoding="utf-8")
        print(f"✅ Created: {readme_path}")
    except Exception as e:
        print(f"❌ Failed to create {readme_path}: {e}")


def create_vault_index(vault_path: Path, structure: list, vault_name: str) -> None:
    index_name = f"{vault_name}INDEX.md"
    vault_index = vault_path / index_name
    if vault_index.exists():
        print(f"⚠️  Skipping existing vault index: {vault_index}")
        return

    try:
        content = [f"# {vault_name} Index\n", "## Sections:\n"]
        seen = set()
        for entry in structure:
            full_name = entry["name"].split("/")[0]
            clean_name = strip_prefix(full_name)
            if full_name not in seen:
                seen.add(full_name)
                content.append(f"- [[{full_name}/{clean_name}INDEX|{clean_name}]]\n")

        vault_index.write_text("".join(content), encoding="utf-8")
        print(f"✅ Created: {vault_index}")
    except Exception as e:
        print(f"❌ Failed to create {index_name}: {e}")


def initialize_vault(config_path: Path) -> None:
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        sys.exit(1)

    vault_name = config.get("vault_name")
    structure = config.get("structure", [])

    if not vault_name or not structure:
        print("❌ Invalid config format. Expecting 'vault_name' and 'structure'.")
        sys.exit(1)

    vault_path = Path(vault_name)
    vault_path.mkdir(parents=True, exist_ok=True)

    for entry in structure:
        folder_path = vault_path / entry["name"]
        try:
            folder_path.mkdir(parents=True, exist_ok=False)
            print(f"📁 Created folder: {folder_path}")
        except FileExistsError:
            print(f"⚠️  Folder already exists: {folder_path}")

        create_readme(folder_path, backlink=f"[[{vault_name}INDEX]]")

    create_vault_index(vault_path, structure, vault_name)



def main():
    import os
    default_config_path = Path(__file__).resolve().parent.parent / "vault_templates" / "default_config.yaml"
    if not os.path.exists(str(default_config_path)):
        print("❌ default_config.yaml not found.")
        return
    sys.argv.append(str(default_config_path)) if len(sys.argv) == 1 else None

    parser = argparse.ArgumentParser(
        description="Initialize a structured Obsidian vault from a YAML configuration file."
    )
    parser.add_argument(
        "config", type=Path, help="Path to the YAML configuration file."
    )
    args = parser.parse_args()
    initialize_vault(args.config)


if __name__ == "__main__":
    main()
