# ✅ INSTALLATION & DEPLOYMENT CHECKLIST

Complete checklist for getting your Kanchipuram Bot up and running.

---

## 📋 PRE-SETUP CHECKLIST

### Requirements Check
- [ ] Python 3.9+ installed on your computer
- [ ] Git installed (for deployment)
- [ ] Discord server admin access
- [ ] Google account active

### Credentials Preparation
- [ ] Discord bot token obtained
- [ ] Google Cloud project created
- [ ] Service account created
- [ ] credentials.json downloaded (or GOOGLE_CREDS ready)
- [ ] Google Sheet created ("Kanchipuram FiveM Logs")

---

## 🖥️ LOCAL SETUP (Step-by-Step)

### Step 1: Download/Extract Files
- [ ] All files in `d:\Kanchipuram bot\` folder
- [ ] No "Kanchipuram bot" subfolder inside another folder
- [ ] Files list matches: bot.py, database.py, requirements.txt, etc.

### Step 2: Run Setup Script

**Windows:**
```bash
Double-click setup.bat
Answer questions in command window
```
- [ ] setup.bat executed successfully
- [ ] Virtual environment created (venv/ folder exists)
- [ ] Dependencies installed (no errors)
- [ ] .env file created

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```
- [ ] setup.sh executed successfully
- [ ] Virtual environment created (venv/ folder exists)
- [ ] Dependencies installed (no errors)
- [ ] .env file created

### Step 3: Configure .env File

Open `.env` file and fill in:

```env
BOT_TOKEN=your_discord_token_here
↓ Check box after adding
- [ ] BOT_TOKEN added (from Discord Developer Portal)
- [ ] BOT_TOKEN is 70+ characters long
- [ ] No quotes around token

GOOGLE_CREDS_FILE=credentials.json
↓ Check boxes
- [ ] Google credentials file ready
- [ ] credentials.json in bot folder OR
- [ ] GOOGLE_CREDS env variable in .env

SHEET_NAME=Kanchipuram FiveM Logs
- [ ] Sheet name matches exactly
- [ ] Service account has access to sheet

MANAGER_ROLE=Server Developers
- [ ] Role name matches your Discord server
- [ ] Role created in Discord

MEMBER_ROLE=KPM Recycle
- [ ] Role name matches your Discord server
- [ ] Role created in Discord
```

### Step 4: Test Bot Locally

```bash
python bot.py
```

You should see:
```
✅ Logged in as Kanchipuram Bot#XXXX
📊 Database initialized: Kanchipuram FiveM Logs
🎮 Ready to log FiveM business activities!
```

- [ ] Bot started without errors
- [ ] Bot logged into Discord
- [ ] Google Sheets connected successfully
- [ ] No error messages in console

### Step 5: Test Discord Commands

In Discord, type: `/` (slash)

- [ ] Command list appears
- [ ] `/log_grind` visible
- [ ] `/storage_view` visible
- [ ] `/stats` visible

Try in test channel:
```
/storage_view
```

- [ ] Command executes successfully
- [ ] Shows current storage status
- [ ] Includes all categories

### Step 6: Verify Google Sheets

Check Google Sheets for auto-created worksheets:

1. Open "Kanchipuram FiveM Logs" sheet
2. Look for tabs at bottom:
   - [ ] "Logs" sheet exists
   - [ ] "Storage" sheet exists
   - [ ] "Stats" sheet exists
   - [ ] "Data" sheet exists

3. Check "Storage" sheet:
   - [ ] Shows current inventory
   - [ ] Formatted nicely
   - [ ] Categories visible

---

## 🌐 CLOUD DEPLOYMENT CHECKLIST

### Choose Hosting Platform
- [ ] Koyeb selected (recommended)
- [ ] Account created
- [ ] Connected to GitHub

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Kanchipuram Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kanchipuram-bot
git push -u origin main
```

- [ ] Code pushed to GitHub
- [ ] `.env` NOT in repository
- [ ] `credentials.json` NOT in repository
- [ ] Repository is private (optional but recommended)

### Deploy on Koyeb

1. Go to [Koyeb Dashboard](https://app.koyeb.com)
2. Click "Create Service"
3. Select "GitHub"
4. Choose "kanchipuram-bot" repository

Configuration:
- [ ] Runtime: Python 3.11
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `python bot.py`
- [ ] HTTP port: 8000

Environment Variables (add each one):
- [ ] BOT_TOKEN = your_token
- [ ] SHEET_NAME = Kanchipuram FiveM Logs
- [ ] MANAGER_ROLE = Server Developers
- [ ] MEMBER_ROLE = KPM Recycle
- [ ] GOOGLE_CREDS = {full_json_content}

Deployment:
- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes
- [ ] Deployment successful message appears
- [ ] Bot online status in Discord

### Verify Deployment

- [ ] Bot appears online in Discord (green dot)
- [ ] Commands work in Discord
- [ ] `/storage_view` returns data
- [ ] Google Sheets still updating
- [ ] No errors in Koyeb logs

---

## 🎮 DISCORD SERVER SETUP CHECKLIST

### Create Roles

1. Server Settings → Roles
2. Create "Server Developers" role
   - [ ] Role created
   - [ ] Color assigned (purple recommended)
   - [ ] Position above bot role

3. Create "KPM Recycle" role
   - [ ] Role created
   - [ ] Color assigned (blue recommended)
   - [ ] Position above bot role

### Assign Roles

- [ ] Admin users have "Server Developers"
- [ ] Regular workers have "KPM Recycle"
- [ ] Bot has manage roles permission
- [ ] Permissions hierarchy correct

### Create Test Channel

- [ ] Create #bot-logs channel
- [ ] Bot can send messages there
- [ ] Test first command there

### Bot Permissions

- [ ] Bot can send messages
- [ ] Bot can embed links
- [ ] Bot can attach files
- [ ] Bot can add reactions
- [ ] Bot can use slash commands

---

## 📊 FINAL VERIFICATION CHECKLIST

### Bot Functionality
- [ ] `/log_grind` works with screenshot
- [ ] `/log_craft` works with screenshot
- [ ] `/log_sale` works with screenshot
- [ ] `/storage_add` works
- [ ] `/storage_remove` works
- [ ] `/storage_view` displays inventory
- [ ] `/stats` shows statistics
- [ ] `/user_stats` works
- [ ] `/admin_clear_logs` works (admin only)
- [ ] `/admin_reset_storage` works (admin only)

### Data Persistence
- [ ] Data saved to Google Sheets
- [ ] Logs visible in "Logs" sheet
- [ ] Storage updated in "Storage" sheet
- [ ] Stats updated in "Stats" sheet
- [ ] Data backed up in "Data" sheet

### Error Handling
- [ ] Non-member cannot use commands (error message)
- [ ] Invalid item gracefully fails
- [ ] No token errors visible
- [ ] No database connection errors
- [ ] Proper error messages shown to users

### Security
- [ ] `.env` not in Git
- [ ] `credentials.json` not in Git
- [ ] `.gitignore` working properly
- [ ] Bot token not exposed in logs
- [ ] No secrets in code comments

### Performance
- [ ] Commands respond within 3 seconds
- [ ] Storage view loads quickly
- [ ] Stats calculation fast
- [ ] Google Sheets syncs in real-time

---

## 🚀 PRODUCTION READINESS CHECKLIST

### Before Going Live

- [ ] All tests passed
- [ ] Roles assigned to team members
- [ ] Discord permissions verified
- [ ] Google Sheet shared with team
- [ ] Documentation reviewed by team
- [ ] Backup plan in place

### Monitoring

- [ ] Set up Discord webhook for errors (optional)
- [ ] Monitor Google Sheets regularly
- [ ] Check bot uptime status
- [ ] Review statistics weekly

### Maintenance

- [ ] Clear old logs monthly
- [ ] Review storage numbers
- [ ] Check for any error patterns
- [ ] Update credentials if needed

---

## 🆘 TROUBLESHOOTING CHECKLIST

### Bot Not Starting

1. Check Python
   ```bash
   python --version
   ```
   - [ ] Python 3.9+ installed

2. Check Dependencies
   ```bash
   pip list | grep discord
   pip list | grep gspread
   ```
   - [ ] discord.py 2.4.0+
   - [ ] gspread 6.0+

3. Check .env file
   - [ ] .env exists in bot folder
   - [ ] All required variables present
   - [ ] No syntax errors in .env
   - [ ] BOT_TOKEN not empty

### Commands Not Showing

1. Check permissions
   - [ ] Bot has "applications.commands" permission
   - [ ] Bot role is positioned correctly

2. Sync commands
   - [ ] Restart bot
   - [ ] Wait 30 seconds
   - [ ] Type `/` in Discord
   - [ ] Commands should appear

### Google Sheets Error

1. Check credentials
   - [ ] credentials.json valid JSON
   - [ ] File in correct location
   - [ ] OR GOOGLE_CREDS env var set

2. Check sheet access
   - [ ] Service account email has access
   - [ ] Sheet not deleted
   - [ ] Sheet name matches exactly

### Data Not Saving

1. Check database
   - [ ] Google Sheets connection successful
   - [ ] No error messages in console
   - [ ] Service account has edit permission

2. Check sheet
   - [ ] "Data" sheet exists
   - [ ] Cell A1 has JSON data
   - [ ] "Logs" sheet has entries

---

## 📝 SIGN-OFF

Once all checkboxes are complete, your Kanchipuram Bot is:

✅ **Fully Functional**
- All commands work
- Data persists
- No errors

✅ **Properly Configured**
- Credentials secured
- Roles assigned
- Permissions verified

✅ **Production Ready**
- Running 24/7
- Backed up to Google Sheets
- Team can use it

✅ **Well Documented**
- Setup complete
- Commands tested
- Ready for training

---

## 🎉 YOU'RE DONE!

Your Kanchipuram Bot is now:
- ✅ Running and online
- ✅ Logging FiveM activities
- ✅ Managing inventory
- ✅ Generating statistics
- ✅ Backed up securely
- ✅ Available 24/7

**Happy logging!** 🎮🚀

---

## 📞 QUICK REFERENCE

**Local Testing:**
```bash
python bot.py
```

**Reinstall Dependencies:**
```bash
pip install -r requirements.txt
```

**View Active Commands:**
Type `/` in Discord

**Check Google Sheet:**
https://sheets.google.com (auto-created)

**Documentation:**
- QUICKSTART.md - Setup guide
- README.md - Commands list
- CONFIG.md - Configuration options
- HOSTING.md - Deployment guide
- PROJECT_SUMMARY.md - Overview

---

Congratulations on your new bot! 🎊
