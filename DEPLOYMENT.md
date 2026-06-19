# 🚀 Deployment Guide - Railway.app

## Quick Deploy to Railway (5 minutes)

### Step 1: Initialize Git Repository (Windows Command Prompt)

```bash
cd C:\Users\Acer\OneDrive\Desktop\AI_Transaction_Validator
git init
git add .
git commit -m "Initial commit: AI Transaction Validator"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository:
   - **Repository name:** ai-transaction-validator
   - **Description:** Transaction validation web application
   - **Public** (so you can deploy)
   - Click "Create repository"

3. Copy the commands from GitHub and run them:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-transaction-validator.git
git push -u origin main
```

### Step 3: Deploy to Railway.app

1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway to access GitHub
4. Click "New Project"
5. Select "Deploy from GitHub repo"
6. Select your "ai-transaction-validator" repository
7. Wait for deployment (2-3 minutes)

### Step 4: Get Public URL

After deployment:
1. Click "Deployments" tab
2. Copy the **Railway URL** provided
3. Share this URL with anyone!

**Example:** `https://ai-transaction-validator-prod.up.railway.app`

---

## ✅ What Railway.app Provides:

- ✅ Free tier (generous limits)
- ✅ Auto-deploys from GitHub
- ✅ Public URL
- ✅ SSL/HTTPS included
- ✅ 24/7 uptime
- ✅ Automatic restarts
- ✅ Easy environment variables

---

## 📋 Files Already Ready:

- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Startup command
- ✅ `.gitignore` - Git configuration
- ✅ `pyproject.toml` - Python project config

All needed for Railway deployment!

---

## 🔗 Important: Environment Variables

Railway.app automatically sets `PORT` environment variable, which the app uses.

No additional setup needed! ✅

---

## ⚠️ Important Notes:

1. **Uploads/Outputs Directory:**
   - Railway uses ephemeral storage
   - Files disappear after app restart
   - For production: Add cloud storage (S3, etc.)

2. **For Now (Development):**
   - Works perfectly for testing
   - Suitable for demos
   - Free tier is sufficient

---

## 🎯 After Deployment:

Your application will be at:
```
https://ai-transaction-validator-[random].up.railway.app
```

Anyone can:
- ✓ Upload CSV files
- ✓ Validate transactions
- ✓ Download results
- ✓ Access from anywhere

---

## 📱 Test Deployed App:

1. Open the Railway URL
2. Upload `test_data/valid_records.csv`
3. Should work exactly like local version

---

## 🆘 Troubleshooting:

**Build fails?**
- Check `requirements.txt` is correct
- Ensure Python 3.8+ syntax

**Port error?**
- Procfile already handles it automatically

**Can't find URL?**
- Go to Railway.app → Select project → Deployments tab

---

Ready to deploy? Follow the 4 steps above! 🚀

