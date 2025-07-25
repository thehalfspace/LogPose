
import json
from pathlib import Path


def backup_obsidian_config(vault_path: Path, backup_path: Path):
    obsidian_config_dir = vault_path / ".obsidian"
    backup_output = backup_path / "obsidian-config-backup.json"
    config_data = {}

    if not obsidian_config_dir.exists():
        print(f"⚠️  No .obsidian folder found at {obsidian_config_dir}")
        return

    for file in obsidian_config_dir.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                config_data[file.name] = json.load(f)
        except Exception as e:
            print(f"❌ Could not read {file.name}: {e}")

    try:
        with open(backup_output, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        print(f"✅ Backup written to: {backup_output}")
    except Exception as e:
        print(f"❌ Failed to write backup: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Backup Obsidian configuration JSONs.")
    parser.add_argument("vault_path", type=Path, help="Path to the Obsidian vault.")
    parser.add_argument("backup_path", type=Path, help="Where to save the backup JSON.")
    args = parser.parse_args()
    backup_obsidian_config(args.vault_path, args.backup_path)


if __name__ == "__main__":
    main()
