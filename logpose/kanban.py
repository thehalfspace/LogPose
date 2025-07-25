
import re
from pathlib import Path
import matplotlib.pyplot as plt


def parse_todo_file(todo_path: Path):
    tasks = []
    completed_dates = []
    with todo_path.open("r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"- \[( |x)\] (.*?)(?: @(\d{4}-\d{2}-\d{2}))?", line.strip())
            if match:
                status, task, date = match.groups()
                tasks.append((status == "x", task, date))
                if status == "x" and date:
                    completed_dates.append(date)
    return tasks, completed_dates


def generate_kanban_md(tasks, output_path: Path):
    todo, doing, done = [], [], []
    for completed, task, date in tasks:
        if completed:
            done.append(f"- [x] {task} @{date}" if date else f"- [x] {task}")
        elif "doing" in task.lower():
            doing.append(f"- [ ] {task}")
        else:
            todo.append(f"- [ ] {task}")

    content = ["# Kanban Board\n", "## To Do\n"] + [f"{t}\n" for t in todo]
    content += ["## Doing\n"] + [f"{t}\n" for t in doing]
    content += ["## Done\n"] + [f"{t}\n" for t in done]

    output_path.write_text("".join(content), encoding="utf-8")
    print(f"✅ Kanban written to {output_path}")


def generate_progress_plot(dates, output_path: Path):
    if not dates:
        print("⚠️  No completed task dates found.")
        return

    from collections import Counter
    counts = Counter(dates)
    sorted_dates = sorted(counts)
    values = [counts[d] for d in sorted_dates]

    plt.figure(figsize=(8, 4))
    plt.bar(sorted_dates, values)
    plt.title("Tasks Completed Per Day")
    plt.xlabel("Date")
    plt.ylabel("Tasks Completed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"✅ Plot saved to {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Kanban board and task progress graph.")
    parser.add_argument("todo_path", type=Path, help="Path to the todo markdown file.")
    parser.add_argument("kanban_output", type=Path, help="Path to write the kanban markdown.")
    parser.add_argument("graph_output", type=Path, help="Path to save the progress PNG.")
    args = parser.parse_args()

    tasks, completed = parse_todo_file(args.todo_path)
    generate_kanban_md(tasks, args.kanban_output)
    generate_progress_plot(completed, args.graph_output)


if __name__ == "__main__":
    main()
