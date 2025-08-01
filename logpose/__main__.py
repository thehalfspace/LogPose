import argparse
from pathlib import Path
from . import initialize, update, todo, backup, kanban

def main():
    parser = argparse.ArgumentParser(description="LogPose CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: init
    init_parser = subparsers.add_parser("init", help="Initialize a new vault")
    init_parser.add_argument("config", type=str, help="Path to the config YAML file")

    # Subcommand: update
    update_parser = subparsers.add_parser("update", help="Update index files in a vault")
    update_parser.add_argument("vault_path", type=str, help="Path to the Obsidian vault")
    update_parser.add_argument("--config", type=str, help="Optional config file path to move media")

    # Subcommand: todo
    todo_parser = subparsers.add_parser("todo", help="Generate project-specific TODO lists and dashboard")
    todo_parser.add_argument("vault_path", type=str)
    todo_parser.add_argument("--config", type=str)

    # Subcommand: backup
    backup_parser = subparsers.add_parser("backup", help="Backup Obsidian config")
    backup_parser.add_argument("vault_path", type=str)
    backup_parser.add_argument("backup_dir", type=str)

    # Subcommand: kanban
    kanban_parser = subparsers.add_parser("kanban", help="Generate kanban boards and charts")
    kanban_parser.add_argument("vault_path", type=str)

    args = parser.parse_args()

    if args.command == "init":
        initialize.initialize_vault(Path(args.config))
    elif args.command == "update":
        config_path = Path(args.config) if args.config else Path(__file__).resolve().parent.parent / "vault-templates/default_config.yaml"
        update.update_indexes(Path(args.vault_path), config_path=config_path)
    elif args.command == "todo":
        config_path = Path(args.config) if args.config else Path(__file__).resolve().parent.parent / "vault-templates/default_config.yaml"
        todo.generate_todolists(Path(args.vault_path), config_path)
    elif args.command == "backup":
        backup.backup_config(Path(args.vault_path), Path(args.backup_dir))
    elif args.command == "kanban":
        kanban.generate_kanban_and_graphs(Path(args.vault_path))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()