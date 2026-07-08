import sys
from datetime import date
from pathlib import Path
import yaml

MARKER_NAME = ".logpose.yaml"
VALID_ROLES = ("vault", "assets")


class LogPoseTrackingError(Exception):
    pass


def marker_path(path: Path) -> Path:
    return path / MARKER_NAME


def read_marker(path: Path) -> dict | None:
    marker = marker_path(path)
    if not marker.exists():
        return None
    with marker.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_marker(path: Path, role: str):
    if role not in VALID_ROLES:
        raise LogPoseTrackingError(f"Invalid role '{role}'. Expected one of {VALID_ROLES}.")
    path.mkdir(parents=True, exist_ok=True)
    marker = marker_path(path)
    if marker.exists():
        raise LogPoseTrackingError(f"{path} is already tracked ({marker}).")
    content = {"role": role, "tracked_since": date.today().isoformat()}
    with marker.open("w", encoding="utf-8") as f:
        yaml.safe_dump(content, f, sort_keys=False)
    print(f"✅ Tracked {path} as role '{role}' ({marker})")


def track(path: Path, role: str = "assets"):
    try:
        write_marker(path, role)
    except LogPoseTrackingError as e:
        print(f"❌ {e}")
        sys.exit(1)


def is_under_linked_assets(file_path: Path, vault_path: Path) -> bool:
    """True if any ancestor of file_path (up to vault_path) is a symlink whose
    target is tracked with role 'assets' — i.e. file_path lives inside a
    linked project folder, not physically inside the vault."""
    current = file_path.parent
    while current != vault_path and vault_path in current.parents:
        if current.is_symlink():
            data = read_marker(current.resolve())
            if data and data.get("role") == "assets":
                return True
        current = current.parent
    return False


def require_tracked(path: Path, expected_role: str | None = None) -> dict:
    """Guard used by every command that operates on an existing tracked folder.
    Exits the process with an error if the folder isn't tracked (or has the
    wrong role, when expected_role is given)."""
    data = read_marker(path)
    if data is None:
        print(
            f"❌ {path} is not a LogPose-tracked folder "
            f"(missing {MARKER_NAME}). Run 'logpose track {path}' first."
        )
        sys.exit(1)
    role = data.get("role")
    if expected_role and role != expected_role:
        print(
            f"❌ {path} is tracked with role '{role}', but this command requires "
            f"role '{expected_role}'."
        )
        sys.exit(1)
    return data
