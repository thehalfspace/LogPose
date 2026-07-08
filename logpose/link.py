import sys
from pathlib import Path
import yaml

from . import tracking

LINKS_REGISTRY = "1-Assets/.links.yaml"


def read_links(vault_path: Path) -> dict:
    registry = vault_path / LINKS_REGISTRY
    if not registry.exists():
        return {}
    with registry.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_links(vault_path: Path, links: dict):
    registry = vault_path / LINKS_REGISTRY
    registry.parent.mkdir(parents=True, exist_ok=True)
    with registry.open("w", encoding="utf-8") as f:
        yaml.safe_dump(links, f, sort_keys=True)


def link_assets(assets_path: Path, vault_path: Path, name: str | None = None):
    assets_path = assets_path.resolve()
    vault_path = vault_path.resolve()

    tracking.require_tracked(assets_path, expected_role="assets")
    tracking.require_tracked(vault_path, expected_role="vault")

    link_name = name or assets_path.parent.name
    target = vault_path / "1-Assets" / link_name

    if target.exists() or target.is_symlink():
        print(f"❌ {target} already exists. Choose a different --as name or remove it first.")
        sys.exit(1)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(assets_path, target_is_directory=True)
    print(f"🔗 Linked {assets_path} → {target}")

    links = read_links(vault_path)
    links[link_name] = str(assets_path)
    write_links(vault_path, links)


def list_links(vault_path: Path) -> dict:
    tracking.require_tracked(vault_path, expected_role="vault")
    links = read_links(vault_path)
    if not links:
        print("No linked projects.")
    for name, source in sorted(links.items()):
        print(f"  {name} → {source}")
    return links


def unlink_assets(vault_path: Path, name: str):
    tracking.require_tracked(vault_path, expected_role="vault")
    links = read_links(vault_path)
    if name not in links:
        print(f"❌ No link named '{name}' found.")
        sys.exit(1)

    target = vault_path / "1-Assets" / name
    if target.is_symlink():
        target.unlink()
        print(f"🔗 Removed link {target}")

    del links[name]
    write_links(vault_path, links)
