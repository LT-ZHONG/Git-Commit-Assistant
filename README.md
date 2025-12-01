# Git Commit Assistant

A smart tool that automatically generates meaningful Git commit messages based on your staged changes.

## Features

- 🤖 **AI-Powered**: Uses advanced language models to analyze your code changes and generate descriptive commit messages
- 📝 **Follows Best Practices**: Automatically includes appropriate prefixes (feat:, fix:, docs:, etc.)
- ✅ **Interactive**: Allows you to review, edit, or reject the generated commit message
- 🎯 **Time-Saving**: Eliminates the struggle of writing commit messages manually

## Requirements

- Python 3.6 or higher
- Git installed and configured
- OpenAI Python client
- Access to ModelScope API (for AI model inference)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install openai
```

3. Make the script executable:

```bash
chmod +x git_commit_assistant.py
```

4. (Optional) Move the script to a directory in your PATH for easy access:

```bash
mv git_commit_assistant.py /usr/local/bin/git-commit-assistant
```

## Usage

1. Stage your changes in Git:

```bash
git add <files>
```

2. Run the Git Commit Assistant:

```bash
# Run in current directory
python git_commit_assistant.py

# Run with a specific repository path
python git_commit_assistant.py --path /path/to/repo
# Or using the short form
python git_commit_assistant.py -p /path/to/repo

# If you moved it to your PATH:
git-commit-assistant
git-commit-assistant --path /path/to/repo
```

3. Review the generated commit message
4. Choose an option:
   - `y` - Use the generated message and commit
   - `n` - Cancel the commit
   - `e` - Edit the generated message before committing

## Example Workflow

```bash
# Make changes to your files
echo "New feature" >> feature.js

# Stage the changes
git add feature.js

# Run Git Commit Assistant
python git_commit_assistant.py

# Review the generated message and confirm
```

## Configuration

The script uses the ModelScope API with the Qwen/Qwen3-32B model by default. You can modify the following parameters in the script:

- `base_url`: The API endpoint for ModelScope
- `api_key`: Your ModelScope API key
- `model`: The model to use for generating commit messages
- `extra_body`: Configuration for thinking control

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.