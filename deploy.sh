#!/bin/bash

# Web Intern Platform - Automated Deployment Script
# This script automates Git push and Vercel deployment
# Usage: ./deploy.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     WEB INTERN PLATFORM - AUTOMATED DEPLOYMENT SCRIPT         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if .env exists
echo "Step 1: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found!"
    echo ""
    echo "Please create .env file with all required credentials:"
    echo "  1. Copy: cp .env.example .env"
    echo "  2. Edit: nano .env (or your editor)"
    echo "  3. Add all 11 credentials from your service dashboards"
    echo ""
    exit 1
fi
echo "✅ .env file found"
echo ""

# Step 2: Configure Git
echo "Step 2: Configuring Git..."
read -p "Enter your Git name (e.g., Your Name): " git_name
read -p "Enter your Git email (e.g., your@email.com): " git_email

git config user.name "$git_name"
git config user.email "$git_email"
echo "✅ Git configured"
echo ""

# Step 3: Add and commit changes
echo "Step 3: Staging and committing changes..."
git add .
echo "✅ Files staged"

git commit -m "Deploy: Web Intern Platform with Vercel configuration

- Removed hardcoded credentials
- Added Vercel deployment configuration
- Updated environment variable handling
- Production-ready deployment setup"

echo "✅ Changes committed"
echo ""

# Step 4: Push to GitHub
echo "Step 4: Pushing to GitHub..."
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

git remote remove origin 2>/dev/null || true
git remote add origin "$repo_url"
git branch -M main
git push -u origin main

echo "✅ Pushed to GitHub"
echo ""

# Step 5: Deploy to Vercel
echo "Step 5: Installing Vercel CLI..."
npm install -g vercel 2>/dev/null || echo "ℹ️  Vercel CLI may already be installed"
echo ""

echo "Step 6: Deploying to Vercel..."
echo "📌 IMPORTANT: You'll be prompted to:"
echo "   1. Link to your Vercel account"
echo "   2. Select or create a project"
echo "   3. Add environment variables from your .env file"
echo ""
read -p "Press Enter to continue to Vercel deployment..."

vercel --prod

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  DEPLOYMENT COMPLETE! 🎉                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Your application is now live!"
echo ""
echo "Next steps:"
echo "1. Visit your Vercel deployment URL"
echo "2. Test all features (signup, OAuth, payments)"
echo "3. Check Vercel dashboard for logs"
echo ""
echo "Need help? See documentation:"
echo "  - START_HERE.md"
echo "  - DEPLOYMENT_CHECKLIST.md"
echo "  - QUICK_REFERENCE.md"
