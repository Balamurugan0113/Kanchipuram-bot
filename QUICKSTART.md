# ⚡ QUICK START GUIDE

Get your Kanchipuram Bot running in 10 minutes!

---

## 📋 What You Need

1. **Discord Bot Token** (5 min)
2. **Google Service Account** (3 min)
3. **Python 3.9+** installed on your computer

Total time: ~15 minutes to first test!

---

## 🚀 Step-by-Step

### **Step 1: Get Discord Bot Token (5 min)**

1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name: "Kanchipuram Bot" → Create
3. Go to "Bot" → "Add Bot"
4. Copy **TOKEN** under your bot name
5. Go to "OAuth2" → "URL Generator"
6. Check: `bot` + `applications.commands`
7. Check: `send_messages`, `embed_links`, `attach_files`
8. Copy URL at bottom → Open in browser → Invite to server

✅ Bot is now in your server (but offline)

---

### **Important: Python Version**

⚠️ **Use Python 3.11 or 3.12** (NOT 3.13)
- Python 3.13 removed `audioop` module which discord.py needs
- Check version: `python --version`
- If you have 3.13, use: `py -3.11 bot.py`

### **Step 2: Setup Google Sheets (5 min)**

**Option A: Quick Setup (Recommended)**

1. Go to https://console.cloud.google.com/
2. Create new project → "Kanchipuram Bot"
3. Enable APIs:
   - Search "Google Sheets API" → Enable
   - Search "Google Drive API" → Enable
4. Go to "Credentials" → "Create Credentials" → "Service Account"
5. Fill: Name = "kanchipuram", Skip optional steps
6. Click on created account → "Keys" tab
7. "Add Key" → "Create new key" → JSON
8. Save the file as `credentials.json` in bot folder

**Option B: Using Environment Variable**
- If above is too complex, you can use `GOOGLE_CREDS` in .env instead

✅ Google connection ready

---

### **Step 3: Create Google Sheet**

1. Go to https://sheets.google.com
2. New spreadsheet → Name: "Kanchipuram FiveM Logs"
3. Right-click sheet → "Share"
4. Share with email from credentials.json (looks like: `xxx@xxx.iam.gserviceaccount.com`)

✅ Sheet is ready

---

### **Step 4: Setup Bot Files**

**Windows:**
```bash
Double-click setup.bat
Answer the questions
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual:**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

---

### **Step 5: Create .env File**

Create file named `.env` in bot folder:

```env
BOT_TOKEN=paste_your_discord_token_here
SHEET_NAME=Kanchipuram FiveM Logs
MANAGER_ROLE=Server Developers
MEMBER_ROLE=KPM Recycle
GOOGLE_CREDS_FILE=credentials.json
```

✅ Config is ready

---

### **Step 6: Test Bot Locally**

```bash
python bot.py
```

You should see:
```
✅ Logged in as Kanchipuram Bot#XXXX
📊 Database initialized: Kanchipuram FiveM Logs
🎮 Ready to log FiveM business activities!
```

Type in Discord: `/` and see commands appear!

---

## 🧪 Test Commands

Try in your Discord server:

```
/storage_view
↓
Shows all storage (probably empty at first)

/log_grind item:Copper amount:100 screenshot:(any_image)
↓
Logs grinding activity

/storage_view
↓
Shows Copper: 100

/admin_clear_logs
↓
Clears all logs (if you have Manager role)
```

✅ Bot is working!

---

## 🌐 Deploy to Free Hosting

When ready to go 24/7:

See [HOSTING.md](HOSTING.md) for step-by-step deployment to:
- **Koyeb** (recommended)
- Railway
- Render
- Replit

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run: `pip install -r requirements.txt` |
| "Token invalid" | Check Discord token in .env |
| "No commands appear" | Restart bot, wait 30 sec, reinvite |
| "Sheets error" | Check credentials.json path |
| "Permission error" | Check Discord/Google permissions |

---

## 📚 Next Steps

1. ✅ Bot working locally? Great!
2. 📖 Read [README.md](README.md) for all commands
3. 🌐 Deploy to [free hosting](HOSTING.md)
4. 🎮 Start logging FiveM activities!
5. 📊 Check stats in Google Sheets

---

## 🎉 Success!

Your bot is ready! Next step: **Deploy to hosting** for 24/7 availability.

See [HOSTING.md](HOSTING.md) →

Questions? Check README.md for detailed help!
