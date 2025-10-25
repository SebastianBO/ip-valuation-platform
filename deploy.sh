#!/bin/bash

# Quick Deployment Script for IP Valuation Platform
# This helps you deploy to Streamlit Community Cloud quickly

echo "🚀 IP Valuation Platform - Deployment Helper"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Check if there are changes
if git diff --cached --quiet; then
    echo "✅ No changes to commit"
else
    # Commit
    echo "💾 Committing changes..."
    read -p "Enter commit message (or press Enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update IP Valuation Platform"
    fi
    git commit -m "$commit_msg"
fi

echo ""
echo "Choose deployment option:"
echo "1. Push to existing GitHub repo"
echo "2. Create new GitHub repo (requires gh CLI)"
echo "3. Show manual instructions"
echo "4. Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        read -p "Enter your GitHub repo URL (e.g., https://github.com/username/repo.git): " repo_url

        # Check if remote exists
        if git remote | grep -q origin; then
            echo "🔄 Updating remote..."
            git remote set-url origin "$repo_url"
        else
            echo "➕ Adding remote..."
            git remote add origin "$repo_url"
        fi

        echo "⬆️  Pushing to GitHub..."
        git push -u origin main

        echo ""
        echo "✅ Code pushed to GitHub!"
        echo ""
        echo "📍 Next steps:"
        echo "1. Go to https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Select your repo and app.py"
        echo "5. Add your API key to Secrets"
        echo "6. Deploy!"
        ;;

    2)
        if ! command -v gh &> /dev/null; then
            echo "❌ GitHub CLI (gh) not found"
            echo "Install it from: https://cli.github.com"
            exit 1
        fi

        echo ""
        read -p "Enter repo name (e.g., ip-valuation-platform): " repo_name
        if [ -z "$repo_name" ]; then
            repo_name="ip-valuation-platform"
        fi

        echo "📦 Creating GitHub repository: $repo_name"
        gh repo create "$repo_name" --public --source=. --remote=origin --push

        echo ""
        echo "✅ Repository created and code pushed!"
        echo ""
        echo "📍 Next steps:"
        echo "1. Go to https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Select: $(gh repo view --json nameWithOwner -q .nameWithOwner)"
        echo "5. Main file: app.py"
        echo "6. Add API key to Secrets"
        echo "7. Deploy!"
        ;;

    3)
        echo ""
        echo "📋 Manual Deployment Instructions"
        echo "=================================="
        echo ""
        echo "1. Create GitHub Repository:"
        echo "   - Go to https://github.com/new"
        echo "   - Name: ip-valuation-platform"
        echo "   - Make it public"
        echo "   - Click 'Create repository'"
        echo ""
        echo "2. Push your code:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/ip-valuation-platform.git"
        echo "   git push -u origin main"
        echo ""
        echo "3. Deploy on Streamlit Cloud:"
        echo "   - Go to https://share.streamlit.io"
        echo "   - Sign in with GitHub"
        echo "   - Click 'New app'"
        echo "   - Repository: YOUR_USERNAME/ip-valuation-platform"
        echo "   - Branch: main"
        echo "   - Main file: app.py"
        echo "   - Click 'Deploy'"
        echo ""
        echo "4. Add API Key Secret:"
        echo "   - In Streamlit Cloud, go to Settings > Secrets"
        echo "   - Add: FINANCIAL_DATASETS_API_KEY = \"your_key_here\""
        echo "   - Save"
        echo ""
        echo "5. Your app will be live at:"
        echo "   https://YOUR_USERNAME-ip-valuation-platform.streamlit.app"
        echo ""
        ;;

    4)
        echo "👋 Deployment cancelled"
        exit 0
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process complete!"
echo ""
echo "📖 For more details, see DEPLOYMENT_GUIDE.md"
