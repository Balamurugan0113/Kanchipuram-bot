# 🎮 Kanchipuram Bot - FiveM Business Logger

A Discord bot for tracking FiveM server business activities: **Grinding**, **Crafting**, **Sales**, and **Storage** management with real-time logging to Google Sheets.

---

## ✨ Features

✅ **Business Activity Logging**
- Log grinding, crafting, and sales activities
- Automatic screenshot capture for proof
- Real-time database updates

✅ **Storage Management**
- Track inventory across multiple categories
- Add/remove items from storage
- View current storage status

✅ **Statistics & Analytics**
- User activity tracking
- Category-wise breakdown
- Top contributors ranking

✅ **Admin Controls**
- Clear logs and reset storage
- User data management
- Role-based permissions

✅ **Free 24/7 Hosting**
- Health check server (port 8000)
- Deploy to Koyeb, Railway, or Render for free
- No credit card required

---

## 📋 Prerequisites

- Python 3.9+
- Discord Bot Token
- Google Service Account (for Sheets)
- Free hosting platform account (Koyeb/Railway/Render)

---

## 🚀 Quick Setup

### 1. **Get Discord Bot Token**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → name it "Kanchipuram Bot"
3. Go to "Bot" section → "Add Bot"
4. Copy the **TOKEN** (keep it secret!)
5. Go to "OAuth2" → "URL Generator"
6. Select scopes: `bot`
7. Select permissions: `applications.commands`, `send_messages`, `embed_links`, `attach_files`, `add_reactions`
8. Copy generated URL and open in browser to invite bot to your server

### 2. **Setup Google Sheets**

#### Option A: Using Service Account JSON
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "Kanchipuram Bot"
3. Enable "Google Sheets API" and "Google Drive API"
4. Go to "Credentials" → "Create Credentials" → "Service Account"
5. Create a key (JSON) → download it
6. Rename to `credentials.json` and save in bot folder

#### Option B: Using Environment Variable
1. Open `credentials.json` with a text editor
2. Copy the entire JSON content
3. Create a `.env` file and set: `GOOGLE_CREDS={paste_json_here}`

### 3. **Create Google Sheet**

1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet: "Kanchipuram FiveM Logs"
3. Share it with your service account email (from credentials.json)
4. The bot will create worksheets automatically

### 4. **Configure Bot**

Create `.env` file in bot folder:

```env
BOT_TOKEN=your_discord_token_here
SHEET_NAME=Kanchipuram FiveM Logs
MANAGER_ROLE=Server Developers
MEMBER_ROLE=KPM Recycle
GOOGLE_CREDS_FILE=credentials.json
```

Or use environment variable (recommended for hosting):

```env
BOT_TOKEN=your_discord_token
GOOGLE_CREDS={"type":"service_account","project_id":"...","...":"..."}
SHEET_NAME=Kanchipuram FiveM Logs
MANAGER_ROLE=Server Developers
MEMBER_ROLE=KPM Recycle
```

### 5. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 6. **Test Locally**

```bash
python bot.py
```

You should see:
```
✅ Logged in as Kanchipuram Bot#1234
📊 Database initialized: Kanchipuram FiveM Logs
🎮 Ready to log FiveM business activities!
```

---

## 📖 Bot Commands

### 📝 Logging Commands

| Command | Role | Description |
|---------|------|-------------|
| `/log_grind` | Member | Log grinding activity |
| `/log_craft` | Member | Log crafting activity |
| `/log_sale` | Member | Log sales activity |

**Parameters:**
- `item` - Item name (autocomplete enabled)
- `amount` - Quantity processed
- `screenshot` - Proof image
- `member` - (Optional) Tag the member who did the work

### 📦 Storage Commands

| Command | Role | Description |
|---------|------|-------------|
| `/storage_add` | Member | Add items to storage |
| `/storage_remove` | Member | Remove items from storage |
| `/storage_view` | Member | View storage status |

### 📊 Stats Commands

| Command | Role | Description |
|---------|------|-------------|
| `/stats` | Member | View overall statistics |
| `/user_stats` | Member | Check specific user stats |

### 🛠️ Admin Commands

| Command | Role | Description |
|---------|------|-------------|
| `/admin_clear_logs` | Manager | Clear all logs |
| `/admin_reset_storage` | Manager | Reset all storage |
| `/admin_clear_user` | Manager | Clear specific user's data |

---

## 🌐 Free 24/7 Hosting

### Option 1: Koyeb (Recommended)

1. **Create Koyeb Account**
   - Go to [koyeb.com](https://koyeb.com)
   - Sign up (free tier available)

2. **Deploy Bot**
   - Connect GitHub account
   - Create new service
   - Select "Docker" deployment
   - Set start command: `python bot.py`

3. **Add Environment Variables**
   - Set all variables from `.env` file
   - Koyeb provides free SSL

### Option 2: Railway

1. Go to [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Add environment variables
4. Automatic deployments on git push

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repo
4. Set start command: `python bot.py`
5. Add environment variables

### Option 4: Replit (Simplest)

1. Go to [replit.com](https://replit.com)
2. Create new Repl → Python
3. Upload all bot files
4. Add `.env` with your credentials
5. Click "Run"

---

## 📂 File Structure

```
Kanchipuram bot/
├── bot.py                 # Main bot file
├── database.py            # Google Sheets integration
├── requirements.txt       # Python dependencies
├── .env.template          # Environment template
├── .env                   # Your actual config (not in git!)
├── credentials.json       # Google service account (optional)
└── README.md              # This file
```

---

## 🔧 Troubleshooting

### Bot not responding to commands?
- Check if bot has `applications.commands` permission
- Make sure members have the required roles
- Verify `BOT_TOKEN` in `.env`

### Google Sheets connection failed?
- Verify sheet name matches `SHEET_NAME` in `.env`
- Check if service account has sheet access
- Make sure credentials.json or `GOOGLE_CREDS` is valid

### Health check server not working?
- Ensure port 8000 is not blocked
- Check hosting platform allows custom ports

### Commands not showing up?
- Try: `/` then wait for command list to refresh
- Invite bot again if permissions were added
- Run: `python bot.py` again to sync commands

---

## 📊 Google Sheets Structure

Bot automatically creates these worksheets:

- **Logs** - Detailed transaction history
  - Timestamp, User, Category, Action, Item, Amount, Screenshot, User ID

- **Storage** - Current inventory status
  - Updated in real-time
  - Formatted for easy reading

- **Stats** - Analytics and summaries
  - Total transactions
  - Category breakdown
  - Top users

- **Data** - Raw JSON backup
  - Persistent storage
  - Easy recovery

---

## 🔐 Security Tips

1. **Never commit `.env` file to GitHub**
2. **Keep bot token private** - if exposed, regenerate it
3. **Use service account email** - don't share Google credentials
4. **Restrict roles** - only give Manager role to trusted users
5. **Use strong Discord server permissions**

---

## 📈 Best Practices

1. **Regular backups** - Google Sheets auto-backs up data
2. **Clean logs monthly** - Use `/admin_clear_logs` periodically
3. **Monitor storage** - Use `/storage_view` regularly
4. **Check user stats** - Track contributions with `/user_stats`
5. **Document activities** - Always take screenshots when logging

---

## 🆘 Support

**Common Issues:**

| Issue | Solution |
|-------|----------|
| "Bot not responding" | Check permissions and roles |
| "Database error" | Verify Google Sheets access |
| "Commands not syncing" | Restart bot and check permissions |
| "Storage not updating" | Check member role assignment |

---

## 📝 License

This bot is designed for the Kanchipuram FiveM Server community.

---

## 🎮 Ready to Start?

1. ✅ Get Discord bot token
2. ✅ Setup Google Sheets
3. ✅ Configure `.env` file
4. ✅ Install dependencies: `pip install -r requirements.txt`
5. ✅ Test locally: `python bot.py`
6. ✅ Deploy to free hosting
7. ✅ Invite bot to your server
8. ✅ Start logging!

**Happy logging! 🚀**
