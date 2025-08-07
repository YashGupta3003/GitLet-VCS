# Gitlet - A Simplified Version Control System

A Python implementation of a simplified Git-like version control system that demonstrates the core concepts of how Git works internally.

## Features

- **Commit Management**: Create commits with messages and timestamps
- **File Tracking**: Add files to staging area and track changes
- **Commit History**: View complete commit history with parent references
- **Diff Visualization**: Colored diff output showing file changes between commits
- **Command Line Interface**: Easy-to-use CLI similar to Git commands

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd gitlet
```

2. Install dependencies:
```bash
pip install termcolor
```

3. Make the script executable:
```bash
chmod +x gitlet.py
```

## Usage

### Basic Commands

```bash
# Initialize a new repository
./gitlet.py init

# Add files to staging area
./gitlet.py add <filename>

# Create a commit
./gitlet.py commit "Your commit message"

# View commit history
./gitlet.py log

# Show differences between commits
./gitlet.py diff <commit-hash>
```

### Example Workflow

```bash
# Initialize repository
./gitlet.py init

# Add a file
./gitlet.py add sample.txt

# Make first commit
./gitlet.py commit "Initial commit"

# Modify file and commit again
./gitlet.py add sample.txt
./gitlet.py commit "Updated file"

# View history
./gitlet.py log

# Show changes in latest commit
./gitlet.py diff <latest-commit-hash>
```

## Architecture

### Data Structure
- **Objects Directory**: Stores file contents and commit metadata using SHA1 hashing
- **HEAD File**: Points to the current commit
- **Index File**: Tracks staged files
- **Commit Tree**: Linear tree structure with parent references

### Key Components
- **Hash-based Storage**: Files and commits stored by SHA1 hash
- **JSON Metadata**: Commit information stored in JSON format
- **Colored Diff Output**: Uses termcolor for enhanced diff visualization

## Technical Details

### Commit Structure
```json
{
  "timestamp": "2025-08-08 03:40:09",
  "message": "Commit message",
  "files": [{"path": "file.txt", "hash": "abc123..."}],
  "parent": "parent-commit-hash"
}
```

### File Organization
```
.gitlet/
├── HEAD (current commit hash)
├── index (staged files)
└── objects/
    ├── abc123... (file content)
    ├── def456... (commit metadata)
    └── ghi789... (commit metadata)
```

## Learning Objectives

This project demonstrates:
- **Version Control Concepts**: How Git-like systems work internally
- **Data Structures**: Tree structures, hash tables, linked lists
- **File I/O**: Binary file handling and JSON serialization
- **Command Line Programming**: Argument parsing and CLI design
- **System Design**: Object-oriented design and modular architecture

## Future Enhancements

- [ ] Branch management
- [ ] Merge functionality
- [ ] Remote repository support
- [ ] Conflict resolution
- [ ] Unit tests
- [ ] Better error handling

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE). 