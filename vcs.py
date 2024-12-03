import os
import sys
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime

VCS_DIR = ".vcs"


def init():
    """Initialize a new repository."""
    if os.path.exists(VCS_DIR):
        print("Repository already initialized.")
        return
    os.makedirs(f"{VCS_DIR}/commits")
    os.makedirs(f"{VCS_DIR}/branches")
    os.makedirs(f"{VCS_DIR}/index")
    with open(f"{VCS_DIR}/HEAD", "w") as head:
        head.write("main")
    with open(f"{VCS_DIR}/branches/main", "w") as branch:
        branch.write("")
    print("Initialized empty VCS repository.")


def hash_file(filepath):
    """Generate a SHA-1 hash for the file contents."""
    with open(filepath, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def add(filepath):
    """Add a file to the staging area."""
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
    ignore_file = f"{VCS_DIR}/ignore"
    if os.path.exists(ignore_file):
        with open(ignore_file) as f:
            ignored = [line.strip() for line in f.readlines()]
        if any(Path(filepath).match(pattern) for pattern in ignored):
            print(f"Ignored file: {filepath}")
            return
    file_hash = hash_file(filepath)
    staged_path = f"{VCS_DIR}/index/{file_hash}"
    shutil.copy(filepath, staged_path)
    print(f"Staged {filepath}.")


def commit(message):
    """Commit changes from the staging area."""
    head_branch = get_head_branch()
    parent_commit = get_branch_commit(head_branch)

    # Create a new commit
    commit_data = {
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "parent": parent_commit,
        "files": {file: hash_file(f"{VCS_DIR}/index/{file}") for file in os.listdir(f"{VCS_DIR}/index")},
    }
    commit_hash = hashlib.sha1(json.dumps(commit_data).encode()).hexdigest()
    with open(f"{VCS_DIR}/commits/{commit_hash}", "w") as commit_file:
        json.dump(commit_data, commit_file)
    with open(f"{VCS_DIR}/branches/{head_branch}", "w") as branch_file:
        branch_file.write(commit_hash)
    shutil.rmtree(f"{VCS_DIR}/index")
    os.makedirs(f"{VCS_DIR}/index")
    print(f"Committed as {commit_hash}.")


def log():
    """Display the commit history."""
    head_branch = get_head_branch()
    commit_hash = get_branch_commit(head_branch)
    while commit_hash:
        with open(f"{VCS_DIR}/commits/{commit_hash}") as commit_file:
            commit_data = json.load(commit_file)
        print(f"Commit {commit_hash}\nMessage: {commit_data['message']}\n")
        commit_hash = commit_data["parent"]


def branch(name):
    """Create a new branch."""
    head_commit = get_branch_commit(get_head_branch())
    with open(f"{VCS_DIR}/branches/{name}", "w") as branch_file:
        branch_file.write(head_commit)
    print(f"Created branch {name}.")


def get_head_branch():
    """Get the current HEAD branch."""
    with open(f"{VCS_DIR}/HEAD") as head:
        return head.read().strip()


def get_branch_commit(branch):
    """Get the latest commit hash for a branch."""
    branch_path = f"{VCS_DIR}/branches/{branch}"
    if os.path.exists(branch_path):
        with open(branch_path) as branch_file:
            return branch_file.read().strip()
    return ""


def checkout(branch):
    """Switch to a different branch."""
    if not os.path.exists(f"{VCS_DIR}/branches/{branch}"):
        print(f"Branch {branch} does not exist.")
        return
    with open(f"{VCS_DIR}/HEAD", "w") as head:
        head.write(branch)
    print(f"Switched to branch {branch}.")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python vcs.py <command> [<args>]")
        return

    command = sys.argv[1]

    if command == "init":
        init()
    elif command == "add" and len(sys.argv) > 2:
        add(sys.argv[2])
    elif command == "commit" and len(sys.argv) > 2:
        commit(sys.argv[2])
    elif command == "log":
        log()
    elif command == "branch" and len(sys.argv) > 2:
        branch(sys.argv[2])
    elif command == "checkout" and len(sys.argv) > 2:
        checkout(sys.argv[2])
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
