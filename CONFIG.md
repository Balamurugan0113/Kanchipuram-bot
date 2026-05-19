# ⚙️ CONFIGURATION GUIDE

Advanced configuration options for the Kanchipuram Bot.

---

## 🎯 Environment Variables

All available configuration options:

```env
# ─────── DISCORD ──────────
BOT_TOKEN=your_token_here
  # Get from: Discord Developer Portal → Applications → Your Bot → TOKEN
  # Required: YES
  # Type: String
  # Max length: 70 chars

MANAGER_ROLE=Server Developers
  # Discord role name for admin commands
  # Required: NO (default: "Server Developers")
  # Type: String
  # Example: "Admins", "Mods", "Bot Manager"

MEMBER_ROLE=KPM Recycle
  # Discord role name for logging commands
  # Required: NO (default: "KPM Recycle")
  # Type: String
  # Example: "Members", "Grinders", "Workers"

# ─────── GOOGLE SHEETS ────────
SHEET_NAME=Kanchipuram FiveM Logs
  # Name of Google Sheet to use
  # Required: YES
  # Type: String
  # Must be exactly as named in Google Sheets

# ─────── GOOGLE AUTH ──────────
# Option A: JSON File (Simple)
GOOGLE_CREDS_FILE=credentials.json
  # Path to service account JSON file
  # Required: NO (if using Option B)
  # Type: Filepath
  # Default: "credentials.json"

# Option B: Environment Variable (Secure)
GOOGLE_CREDS={"type":"service_account",...}
  # Full JSON content as environment variable
  # Required: NO (if using Option A)
  # Type: JSON string
  # Best for: Deployment platforms (Koyeb, Railway, etc.)

# ─────── SERVER ────────
LOG_CHANNEL_ID=123456789
  # Discord channel ID for bot logs (optional)
  # Required: NO
  # Type: Integer
  # Get by: Enable Developer Mode → Right-click channel → Copy ID

ADMIN_GUILD_ID=123456789
  # Your Discord server ID (optional)
  # Required: NO
  # Type: Integer
  # Used for admin commands scope
```

---

## 🔑 Getting Credentials

### Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name: "Kanchipuram Bot"
4. Go to "Bot" tab
5. Click "Add Bot"
6. Under "TOKEN" click "Copy"
7. **Keep it secret!** Never share or commit to GitHub

### Google Service Account

**Method 1: Console (Recommended)**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Kanchipuram Bot"
3. Enable APIs:
   ```
   Search "Google Sheets API" → Enable
   Search "Google Drive API" → Enable
   ```
4. Go to "Credentials" tab
5. Click "Create Credentials" → "Service Account"
6. Fill form:
   - Service account name: "kanchipuram-bot"
   - Description: "FiveM Logging Bot"
   - Click "Create and Continue"
7. Skip "Grant this service account access to project"
8. Click "Create Key"
9. Choose "JSON"
10. Save as `credentials.json`
11. **Keep it secret!**

**Method 2: Using .json File**

```env
# In .env file:
GOOGLE_CREDS_FILE=credentials.json

# Place credentials.json in bot folder
# File contents will be read automatically
```

**Method 3: Environment Variable**

```env
# Copy entire JSON content from credentials.json
GOOGLE_CREDS={"type":"service_account","project_id":"xxx","private_key_id":"xxx",...}

# Best for: Hosting platforms (Koyeb, Railway, Render)
# Security: More secure than storing file
```

---

## 📋 Role Setup in Discord

### Create Required Roles

1. Go to Server Settings → Roles
2. Create "Server Developers" role
   - Color: Purple
   - Permissions: Admin (for testing)
3. Create "KPM Recycle" role
   - Color: Blue
   - Permissions: View Channels, Send Messages

### Assign Roles

1. Go to Member list
2. Right-click user → Add role
3. Assign based on responsibility:
   - **Server Developers** → Admin/Managers
   - **KPM Recycle** → Regular workers

---

## 🗂️ Google Sheets Setup

### Sheet Structure

The bot creates these automatically:

**Logs Sheet**
```
Timestamp | User | Category | Action | Item | Amount | Screenshot | User ID
2024-01-01 | John | Grinding | LOG | Copper | 100 | [image] | 123456
```

**Storage Sheet**
```
KANCHIPURAM FiveM - STORAGE STATUS
📦 Grinding
  • Copper: 100
  • Iron: 50
🔹 Crafting
  (Empty)
```

**Stats Sheet**
```
INVENTORY STATS
Total Transactions: 42
Grinding: 20
Crafting: 15
Sales: 7
Top Users:
  John: 15
```

**Data Sheet**
```
{
  "storage": {...},
  "stats": {...}
}
```

---

## 🔧 Customization

### Change Business Categories

Edit `database.py`:

```python
BUSINESS_CATEGORIES = ["Grinding", "Crafting", "Storage", "Sales", "Farming"]
```

Restart bot for changes to take effect.

### Custom Colors

Edit `bot.py`:

```python
def get_color(category: str) -> int:
    colors = {
        "Grinding": 0x3498db,  # Blue
        "Crafting": 0x2ecc71,  # Green
        "Sales": 0xf39c12,     # Orange
        "Storage": 0x9b59b6    # Purple
        "Farming": 0xe8b71f    # Gold
    }
    return colors.get(category, 0x95a5a6)
```

### Custom Item Defaults

Edit `database.py`:

```python
def _create_default_data(self) -> Dict:
    return {
        "storage": {
            "Grinding": {"Copper": 0, "Iron": 0, "Gold": 0},
            "Crafting": {"Weapons": 0, "Armor": 0},
            # ...
        }
    }
```

---

## 📊 Google Sheets Sharing

### Share with Service Account

1. Open your Google Sheet
2. Click "Share" button (top right)
3. Copy email from `credentials.json`:
   ```
   "client_email": "xxx@xxx.iam.gserviceaccount.com"
   ```
4. Paste in share dialog
5. Click "Share"
6. **Don't send notification**

### Multiple Sheets per Category

Instead of one master sheet, use separate sheets:

```env
# Multiple environments:
SHEET_NAME_DEV=Kanchipuram Dev Logs
SHEET_NAME_PROD=Kanchipuram Prod Logs
```

Then modify bot.py to use different sheets based on environment.

---

## 🔐 Security Best Practices

### Protecting Credentials

**DO:**
- ✅ Store credentials in `.env` file
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables on hosting platforms
- ✅ Rotate tokens if exposed

**DON'T:**
- ❌ Commit `.env` to GitHub
- ❌ Share bot token publicly
- ❌ Put credentials in code comments
- ❌ Commit `credentials.json`

### .gitignore Protection

Ensure `.gitignore` contains:
```
.env
.env.local
credentials.json
*.json
```

Verify with: `git status` (should not show .env)

### Token Rotation

If token is exposed:
1. Go to Discord Developer Portal
2. Click "Regenerate" under TOKEN
3. Update `.env` file
4. Restart bot

---

## 🌐 Deployment Configuration

### Koyeb

Environment variables in Koyeb UI:

```
BOT_TOKEN = your_token
GOOGLE_CREDS = {"type":"service_account",...}
SHEET_NAME = Kanchipuram FiveM Logs
```

### Railway

Add in `railway.json`:

```json
{
  "BOT_TOKEN": "your_token",
  "GOOGLE_CREDS": "{...}",
  "SHEET_NAME": "Kanchipuram FiveM Logs"
}
```

### Render

Environment variables section:

```
BOT_TOKEN = your_token
GOOGLE_CREDS = {full_json_here}
SHEET_NAME = Kanchipuram FiveM Logs
```

### Replit

Add to `.env` file in Replit:

```env
BOT_TOKEN=your_token
GOOGLE_CREDS={"type":"service_account",...}
SHEET_NAME=Kanchipuram FiveM Logs
```

---

## 🧪 Testing Configuration

### Test Discord Connection

```python
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('BOT_TOKEN')
print('✅ Token loaded' if token else '❌ Token not found')
print(f'Token length: {len(token) if token else 0}')
"
```

### Test Google Sheets

```python
from database import FiveMLogs
try:
    db = FiveMLogs('Your Sheet Name')
    print('✅ Google Sheets connected')
    print(db.get_storage())
except Exception as e:
    print(f'❌ Error: {e}')
```

---

## 📝 Examples

### Example: Corporate Setup

```env
BOT_TOKEN=MjkzNDU2Nzg5MDEyMzQ1Ng.XxXxXx.XxXxXxXxXxXxXxXxXxXxXxXx
SHEET_NAME=Corporate FiveM Logs
MANAGER_ROLE=Executives
MEMBER_ROLE=Employees
```

### Example: Gaming Community

```env
BOT_TOKEN=NDEzNDM2NzI5NjkwMjM0NTY.XxXxXx.XxXxXxXxXxXxXxXxXxXxXxXx
SHEET_NAME=Gaming Hub Logs
MANAGER_ROLE=Admins
MEMBER_ROLE=Members
```

### Example: Production Deployment

```env
BOT_TOKEN=YOUR_SECURE_TOKEN
GOOGLE_CREDS={"type":"service_account","project_id":"kanchipuram-bot","private_key_id":"key123",...}
SHEET_NAME=Kanchipuram FiveM Logs (Prod)
MANAGER_ROLE=Server Developers
MEMBER_ROLE=KPM Recycle
```

---

## ❓ FAQs

**Q: Can I use multiple Google Sheets?**
A: Yes, modify `SHEET_NAME` to use different sheets per environment.

**Q: Can I change role names?**
A: Yes, edit `MANAGER_ROLE` and `MEMBER_ROLE` in `.env`.

**Q: Where should I store credentials?**
A: Use environment variables on hosting platforms, `.env` locally.

**Q: Is it safe to commit `.env`?**
A: NO! Always add to `.gitignore`.

**Q: How often does data sync?**
A: In real-time! Every log/storage change updates immediately.

---

## 🔗 Related Docs

- [QUICKSTART.md](QUICKSTART.md) - Get running in 10 min
- [README.md](README.md) - Full documentation
- [HOSTING.md](HOSTING.md) - Deployment guide

---

Still need help? Check the troubleshooting sections in other docs! 🚀
