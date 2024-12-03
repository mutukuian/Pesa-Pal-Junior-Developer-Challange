# Pesa-Pal-Junior-Developer-Challange

Problem Overview
In this task, we were asked to build a distributed source control system similar to Git. The goal was to design a system that could:

Initialize a repository in a directory.
Store the repository in a hidden .vcs directory.
Support staging files (similar to git add), committing changes, viewing commit history, branching, merging, and comparing diffs.
Detect conflicting changes without providing resolution.
Clone the repository on disk (without network support).
Ignore specific files, similar to .gitignore in Git.
This solution aims to implement a basic version control system that mimics the core functionality of Git, but simplified for educational purposes.

Design Overview
The source control system was built to support essential features while maintaining simplicity. Below is an explanation of the components and their design:

Repository Structure:

The repository is initialized in a directory with a hidden .vcs directory. This .vcs directory stores all the version control data, including commit objects, branch references, and staging information.
Inside the .vcs directory, we maintain separate files for commits (commits/), branches (branches/), and the staging area (staging/).
Staging and Committing:

Files are staged using the add command. When a file is added, it is placed in a staging area (staging/), ready to be committed.
The commit command takes all staged files, creates a snapshot of them, and stores it as a new commit in the commits/ directory.
The commit history is stored as a series of snapshots that record changes made to the repository over time.
Branching and Merging:

Branches are implemented as separate references within the .vcs directory.
A branch is a pointer to a particular commit, and you can switch between branches with the checkout command.
Merging is performed by comparing the changes in two branches and applying them to the current branch. If there are conflicting changes (changes to the same lines of the same file), the system detects this, but does not attempt to resolve the conflict. It simply reports it.
Diffing:

The diff command allows the comparison of changes between two branches. This compares the files in both branches and shows the differences in their contents.
Ignoring Files:

A .vcsignore file is used to specify which files should not be tracked by the version control system. Files listed in this file will be excluded from staging, committing, and diffing.
Cloning:

The clone command is implemented to duplicate an existing repository on disk. This allows a user to create a new repository with the exact same history and file structure as the original repository.
Key Features
Distributed Architecture:

The source control system is designed to be distributed, where every repository is self-contained. There is no centralized server; each user has their own copy of the repository and can work independently.
Branching and Commit History:

Branching allows users to work on different features or fixes in parallel without interfering with each other's work. Each branch has its own commit history, and the system allows merging branches to integrate changes.
The commit history is stored in a linked list, with each commit pointing to its parent commit.
File Comparison (Diffing):

The system includes a simple mechanism for comparing changes between branches using the diff command. This allows users to see what has changed between two versions of the repository.
Staging Area:

Files need to be explicitly staged before they can be committed. This allows users to selectively commit files and group related changes together.
Conflict Detection:

The system is capable of detecting conflicting changes when merging branches. If two branches modify the same part of the same file, the merge will fail, and the system will report a conflict.
File Ignoring:

Similar to .gitignore in Git, the .vcsignore file allows users to specify files that should not be tracked by the version control system. This is useful for excluding temporary files, build artifacts, or sensitive data.
Limitations and Future Improvements
Conflict Resolution:

The system detects conflicts but does not provide automatic conflict resolution. Implementing an interactive conflict resolution system could be a future enhancement.
Performance Optimization:

The system is simple and not optimized for large repositories or binary files. Future versions could implement delta encoding to store file changes more efficiently.
Network Support:

Currently, the system is only capable of operating on the local filesystem. Adding network support for cloning and pushing/pulling changes between repositories would make it more versatile.
GUI Interface:

While the system is command-line-based, a graphical interface could make it more user-friendly, especially for non-technical users.