@echo off
REM Web Intern Platform - Automated Deployment Script (Windows)
REM This script automates Git push and Vercel deployment
REM Usage: deploy.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     WEB INTERN PLATFORM - AUTOMATED DEPLOYMENT SCRIPT         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Check if .env exists
echo Step 1: Checking environment configuration...
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create .env file with all required credentials:
    echo   1. Copy: copy .env.example .env
    echo   2. Edit: Edit .env in Notepad or your editor
    echo   3. Add all 11 credentials from your service dashboards
    echo.
    pause
    exit /b 1
)
echo ✅ .env file found
echo.

REM Step 2: Configure Git
echo Step 2: Configuring Git...
set /p git_name="Enter your Git name (e.g., Your Name): "
set /p git_email="Enter your Git email (e.g., your@email.com): "

git config user.name "%git_name%"
git config user.email "%git_email%"
echo ✅ Git configured
echo.

REM Step 3: Add and commit changes
echo Step 3: Staging and committing changes...
git add .
echo ✅ Files staged

git commit -m "Deploy: Web Intern Platform with Vercel configuration - Removed hardcoded credentials - Added Vercel deployment configuration - Updated environment variable handling - Production-ready deployment setup"

echo ✅ Changes committed
echo.

REM Step 4: Push to GitHub
echo Step 4: Pushing to GitHub...
set /p repo_url="Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): "

git remote remove origin 2>nul
git remote add origin "%repo_url%"
git branch -M main
git push -u origin main

echo ✅ Pushed to GitHub
echo.

REM Step 5: Deploy to Vercel
echo Step 5: Checking Vercel CLI...
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)
echo.

echo Step 6: Deploying to Vercel...
echo 📌 IMPORTANT: You'll be prompted to:
echo    1. Link to your Vercel account
echo    2. Select or create a project
echo    3. Add environment variables from your .env file
echo.
pause

vercel --prod

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  DEPLOYMENT COMPLETE! 🎉                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ✅ Your application is now live!
echo.
echo Next steps:
echo 1. Visit your Vercel deployment URL
echo 2. Test all features (signup, OAuth, payments)
echo 3. Check Vercel dashboard for logs
echo.
echo Need help? See documentation:
echo   - START_HERE.md
echo   - DEPLOYMENT_CHECKLIST.md
echo   - QUICK_REFERENCE.md
echo.
pause
