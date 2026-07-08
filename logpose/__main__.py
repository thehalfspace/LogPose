import argparse
from pathlib import Path
from . import initialize, update, todo, backup, kanban, tracking, link

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

    # Subcommand: track
    track_parser = subparsers.add_parser("track", help="Mark a folder as LogPose-tracked")
    track_parser.add_argument("path", type=str, help="Path to the vault or project assets/ folder")
    track_parser.add_argument("--role", type=str, choices=["vault", "assets"], default="assets",
                               help="Role of the tracked folder (default: assets)")

    # Subcommand: link
    link_parser = subparsers.add_parser("link", help="Symlink a project's assets/ folder into a vault")
    link_parser.add_argument("assets_path", type=str, help="Path to the tracked project assets/ folder")
    link_parser.add_argument("vault_path", type=str, help="Path to the tracked vault")
    link_parser.add_argument("--as", dest="link_name", type=str, default=None,
                              help="Name to use under 1-Assets/ (defaults to the project folder name)")

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
        backup.backup_obsidian_config(Path(args.vault_path), Path(args.backup_dir))
    elif args.command == "kanban":
        kanban.generate_kanban_and_graphs(Path(args.vault_path))
    elif args.command == "track":
        tracking.track(Path(args.path), role=args.role)
    elif args.command == "link":
        link.link_assets(Path(args.assets_path), Path(args.vault_path), name=args.link_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()