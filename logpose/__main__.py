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
    update_parser = subparsers.add_parser("update", help="Update index files")
    update_parser.add_argument("vault_path", type=str, help="Path to Obsidian vault")
    update_parser.add_argument("--vault_name", type=str, help="Optional vault name for backlinking")

    # Subcommand: todo
    todo_parser = subparsers.add_parser("todo", help="Generate global TODO list")
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
        update.update_indexes(Path(args.vault_path), args.vault_name or Path(args.vault_path).name)
    elif args.command == "todo":
        todo.main()
    elif args.command == "backup":
        backup.main()
    elif args.command == "kanban":
        kanban.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
