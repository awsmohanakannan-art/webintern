#!/usr/bin/env python3
"""
Web Intern Platform - Automated Deployment Script
Handles GitHub push and Vercel deployment
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(command, description=""):
    """Run shell command and handle errors"""
    try:
        print(f"\n📌 {description}")
        print(f"   Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════╗
║     WEB INTERN PLATFORM - AUTOMATED DEPLOYMENT SCRIPT         ║
╚════════════════════════════════════════════════════════════════╝
""")

    # Step 1: Check .env file
    print("Step 1: Checking environment configuration...")
    if not Path(".env").exists():
        print("❌ ERROR: .env file not found!")
        print("\nPlease create .env file:")
        print("  1. Copy: cp .env.example .env")
        print("  2. Edit .env with your credentials")
        print("  3. Run this script again")
        sys.exit(1)
    print("✅ .env file found\n")

    # Step 2: Configure Git
    print("Step 2: Configuring Git...")
    git_name = input("Enter your Git name (e.g., Your Name): ").strip()
    git_email = input("Enter your Git email (e.g., your@email.com): ").strip()
    
    if not git_name or not git_email:
        print("❌ Git configuration required")
        sys.exit(1)
    
    run_command(f'git config user.name "{git_name}"', "Setting Git name")
    run_command(f'git config user.email "{git_email}"', "Setting Git email")

    # Step 3: Commit changes
    print("\nStep 3: Staging and committing changes...")
    run_command("git add .", "Staging files")
    
    commit_msg = """Deploy: Web Intern Platform with Vercel configuration

- Removed hardcoded credentials
- Added Vercel deployment configuration
- Updated environment variable handling
- Production-ready deployment setup"""
    
    run_command(f'git commit -m "{commit_msg}"', "Committing changes")

    # Step 4: Push to GitHub
    print("\nStep 4: Pushing to GitHub...")
    repo_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): ").strip()
    
    if not repo_url:
        print("❌ Repository URL required")
        sys.exit(1)
    
    run_command("git remote remove origin 2>nul || true", "Removing old remote")
    run_command(f'git remote add origin "{repo_url}"', "Adding new remote")
    run_command("git branch -M main", "Ensuring main branch")
    run_command("git push -u origin main", "Pushing to GitHub")

    # Step 5: Check Vercel CLI
    print("\nStep 5: Checking Vercel CLI...")
    result = subprocess.run("vercel --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("⚠️  Vercel CLI not found, installing...")
        run_command("npm install -g vercel", "Installing Vercel CLI")

    # Step 6: Deploy to Vercel
    print("\nStep 6: Deploying to Vercel...")
    print("""
📌 IMPORTANT: You'll be prompted to:
   1. Link to your Vercel account (or login)
   2. Select or create a project
   3. Confirm project settings
   
The deployment will proceed automatically after these prompts.
""")
    
    input("Press Enter to continue to Vercel deployment...")
    
    run_command("vercel --prod", "Deploying to Vercel")

    # Success
    print("""
╔════════════════════════════════════════════════════════════════╗
║                  DEPLOYMENT COMPLETE! 🎉                      ║
╚════════════════════════════════════════════════════════════════╝

✅ Your application is now live!

Next steps:
1. Visit your Vercel deployment URL
2. Test all features (signup, OAuth, payments)
3. Check Vercel dashboard for logs
4. Share the URL with your team

Need help? See documentation:
  - START_HERE.md
  - DEPLOYMENT_CHECKLIST.md
  - QUICK_REFERENCE.md
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
