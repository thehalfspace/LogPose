#!/usr/bin/env python3
import sys
import argparse
import yaml
from pathlib import Path


def create_readme(folder_path: Path, backlink: str = "[[VaultINDEX]]") -> None:
    readme_path = folder_path / "index.md"
    if readme_path.exists():
        print(f"⚠️  Skipping existing index: {readme_path}")
        return

    try:
        content = [f"# {folder_path.name}\n", f"Backlink: {backlink}\n", "## Contents:\n"]
        for item in sorted(folder_path.iterdir()):
            if item.name == "index.md":
                continue
            if item.is_dir():
                content.append(f"- [[{item.name}/index|{item.name}]]\n")
            else:
                content.append(f"- [[{item.name}]]\n")

        readme_path.write_text("".join(content), encoding="utf-8")
        print(f"✅ Created: {readme_path}")
    except Exception as e:
        print(f"❌ Failed to create {readme_path}: {e}")


def create_vault_index(vault_path: Path, structure: list) -> None:
    vault_index = vault_path / "VaultINDEX.md"
    if vault_index.exists():
        print(f"⚠️  Skipping existing VaultINDEX: {vault_index}")
        return

    try:
        content = ["# Vault Index\n", "## Sections:\n"]
        seen = set()
        for entry in structure:
            top_level = entry["name"].split("/")[0]
            if top_level not in seen:
                seen.add(top_level)
                content.append(f"- [[{top_level}/index|{top_level}]]\n")

        vault_index.write_text("".join(content), encoding="utf-8")
        print(f"✅ Created: {vault_index}")
    except Exception as e:
        print(f"❌ Failed to create VaultINDEX.md: {e}")


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

        create_readme(folder_path)

    create_vault_index(vault_path, structure)


def main():
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
