
import argparse
from . import initialize, update, todo, backup, kanban

def main():
    parser = argparse.ArgumentParser(description="LogPose CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize a new vault")
    subparsers.add_parser("update", help="Update index files in the vault")
    subparsers.add_parser("todo", help="Generate TODO list")
    subparsers.add_parser("backup", help="Backup Obsidian config")
    subparsers.add_parser("kanban", help="Generate kanban board and graphs")

    args = parser.parse_args()

    if args.command == "init":
        initialize.main()
    elif args.command == "update":
        update.main()
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
