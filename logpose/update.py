import os
from pathlib import Path
import shutil
import yaml

def strip_prefix(name: str) -> str:
    return name.split("-", 1)[-1] if "-" in name else name

def get_backlinks(path: Path, vault_root: Path, vault_index_name: str) -> list:
    backlinks = []
    current = path
    while current != vault_root.parent:
        if current == vault_root:
            backlinks.append(f"[[{vault_index_name}]]")
        else:
            name_stripped = strip_prefix(current.name)
            backlinks.append(f"[[{current.name}/{name_stripped}INDEX]]")
        current = current.parent
    return list(reversed(backlinks))

def update_readme(path: Path, vault_root: Path, vault_index_name: str):
    name_stripped = strip_prefix(path.name)
    readme_name = f"{name_stripped}INDEX.md"
    readme_path = path / readme_name

    try:
        lines = [f"# {name_stripped}\n"]
        backlinks = get_backlinks(path, vault_root, vault_index_name)
        if backlinks:
            lines.append("Backlinks: " + " ← ".join(backlinks) + "\n\n")

        lines.append("## Contents:\n")
        for item in sorted(path.iterdir()):
            if item.name == readme_name or item.name.startswith("."):
                continue
            if item.is_dir():
                sub_name = strip_prefix(item.name)
                lines.append(f"- [[{item.name}/{sub_name}INDEX|{sub_name}]]\n")
            else:
                lines.append(f"- [[{item.name}]]\n")

        readme_path.write_text("".join(lines), encoding="utf-8")
        print(f"✅ Updated {readme_path}")
    except Exception as e:
        print(f"❌ Failed to update {path}: {e}")

def walk_and_update(vault_path: Path):
    vault_name = vault_path.name
    for dirpath, _, _ in os.walk(vault_path):
        path = Path(dirpath)
        if not path.name.startswith(".") and path.is_dir():
            update_readme(path, vault_path, f"{vault_name}INDEX")

def move_media_files(vault_path: Path, config_path: Path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        image_dest = vault_path / config['media']['images']
        video_dest = vault_path / config['media']['videos']
        image_dest.mkdir(parents=True, exist_ok=True)
        video_dest.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Failed to read media paths from config: {e}")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.gif']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']

    for file_path in vault_path.rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in image_extensions and image_dest not in file_path.parents:
                shutil.move(str(file_path), str(image_dest / file_path.name))
                print(f"📷 Moved image: {file_path.name} → {image_dest}")
            elif ext in video_extensions and video_dest not in file_path.parents:
                shutil.move(str(file_path), str(video_dest / file_path.name))
                print(f"🎥 Moved video: {file_path.name} → {video_dest}")

def update_indexes(vault_path: Path, config_path: Path = None):
    walk_and_update(vault_path)
    if config_path:
        move_media_files(vault_path, config_path)
