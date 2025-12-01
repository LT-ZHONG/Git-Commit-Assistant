#!/usr/bin/env python3
"""
Git Commit Assistant

This script automatically generates Git commit messages based on the staged changes
in your repository. It runs `git status` and `git diff --staged` commands, analyzes
the changes, and uses an AI model to generate an appropriate commit message.
"""

import os
import argparse
import subprocess
from openai import OpenAI
from dotenv import load_dotenv


class GitCommitAssistant:
    def __init__(self, repo_path=None):
        load_dotenv()

        self.base_url = os.getenv('BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.model = os.getenv('MODEL')

        # Initialize OpenAI client with ModelScope configuration
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        
        # Configuration for thinking control
        self.extra_body = {
            "enable_thinking": True,
        }
        
        # Set repository path
        self.repo_path = repo_path
        if self.repo_path:
            # Convert to absolute path if not already
            self.repo_path = os.path.abspath(self.repo_path)
            print(f"📁 Using repository path: {self.repo_path}")

        print(f"🔧 Loaded configuration:")
        print(f"  - Base URL: {self.base_url}")
        print(f"  - API Key: {self.api_key}")
        print(f"  - Model: {self.model}")

    def run_command(self, command):
        """Execute a shell command and return its output."""
        try:
            # Run command in the specified repository directory if provided
            cwd = self.repo_path if self.repo_path else None
            
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                text=True, 
                capture_output=True,
                cwd=cwd
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Error output: {e.stderr}")
            return None

    def get_git_status(self):
        """Run git status command and return the output."""
        return self.run_command("git status")

    def get_git_diff(self):
        """Run git diff --staged command and return the output."""
        return self.run_command("git --no-pager diff --staged")

    def is_git_repository(self):
        """Check if the specified directory is a Git repository."""
        result = self.run_command("git rev-parse --is-inside-work-tree")
        return result is not None and "true" in result

    def has_staged_changes(self, git_status):
        """Check if there are staged changes ready to commit."""
        return "Changes to be committed" in git_status

    def generate_commit_message(self, git_status, git_diff):
        """Generate a commit message based on git status and diff."""
        prompt = f"""
        Based on the following git status and diff information, generate a concise and descriptive git commit message.
        
        Follow these guidelines:
        1. Start with an appropriate prefix (feat:, fix:, docs:, style:, refactor:, perf:, test:, build:, ci:, chore:)
        2. Keep the subject line under 50 characters
        3. Add a blank line after the subject
        4. Provide a brief description in the body (wrap at 72 characters)
        5. Focus on what changed and why, not how
        6. Use imperative mood (e.g., "Add feature" not "Added feature")
        
        Git Status:
        {git_status}
        
        Git Diff:
        {git_diff}
        
        Commit message:
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=True,
                extra_body=self.extra_body
            )
            
            thinking_output = []
            commit_message = []
            done_thinking = False
            
            print("\n=== AI is analyzing your changes ===")
            
            for chunk in response:
                thinking_chunk = getattr(chunk.choices[0].delta, 'reasoning_content', '')
                answer_chunk = getattr(chunk.choices[0].delta, 'content', '')
                
                if thinking_chunk:
                    thinking_output.append(thinking_chunk)
                    print(thinking_chunk, end='', flush=True)
                elif answer_chunk:
                    if not done_thinking:
                        print('\n\n=== Generated Commit Message ===\n')
                        done_thinking = True
                    commit_message.append(answer_chunk)
                    print(answer_chunk, end='', flush=True)
            
            return ''.join(commit_message).strip()
            
        except Exception as e:
            print(f"\nError generating commit message: {e}")
            return None

    def run(self):
        """Main execution flow."""
        print("🚀 Git Commit Assistant")
        print("=======================")
        
        # Check if the specified directory is a Git repository
        if not self.is_git_repository():
            print("❌ Error: Not a Git repository.")
            if self.repo_path:
                print(f"Please make sure '{self.repo_path}' is a valid Git repository.")
            else:
                print("Please run this command from within a Git repository or specify a valid repository path.")
            return
        
        # Get git status
        print("\n📊 Checking git status...")
        git_status = self.get_git_status()
        
        if git_status is None:
            print("❌ Failed to get git status.")
            return
        
        print(git_status)
        
        # Check if there are staged changes
        if not self.has_staged_changes(git_status):
            print("\n❌ No staged changes found.")
            print("Please stage your changes with 'git add' before running this command.")
            return
        
        # Get git diff of staged changes
        print("\n📝 Getting diff of staged changes...")
        git_diff = self.get_git_diff()
        
        if git_diff is None:
            print("❌ Failed to get git diff.")
            return

        print(git_diff)
        
        # Generate commit message
        commit_message = self.generate_commit_message(git_status, git_diff)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automatically generate Git commit messages based on staged changes.')
    parser.add_argument('--path', '-p', type=str, help='Path to the Git repository (default: current directory)')

    args = parser.parse_args()

    assistant = GitCommitAssistant(repo_path=args.path)
    assistant.run()
