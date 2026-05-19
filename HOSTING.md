# 🚀 FREE 24/7 HOSTING GUIDE

Deploy your Kanchipuram Bot to free hosting platforms - no credit card needed!

---

## 🏆 Best Options for Free Hosting

### **1. KOYEB (Recommended) ⭐**

**Pros:**
- ✅ Free tier: 10 GB bandwidth/month
- ✅ Always-on (no sleep mode)
- ✅ Simple deployment
- ✅ Docker support

**Cons:**
- ❌ Limited bandwidth
- ❌ Free tier suspended after inactivity (but logs are safe)

**Steps:**

1. **Sign Up**
   ```bash
   Go to https://app.koyeb.com/auth/signup
   Create free account (no credit card)
   ```

2. **Connect GitHub**
   - Click "Create Service"
   - Select "GitHub"
   - Authorize Koyeb access
   - Select your bot repository

3. **Configure Deployment**
   - **Runtime**: Python 3.11
   - **Build command**: `pip install -r requirements.txt`
   - **Run command**: `python bot.py`
   - **HTTP port**: 8000

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add each variable from your `.env`:
     - `BOT_TOKEN`
     - `GOOGLE_CREDS`
     - `SHEET_NAME`
     - `MANAGER_ROLE`
     - `MEMBER_ROLE`

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Bot goes live! 🎉

---

### **2. RAILWAY (Easy) 🚂**

**Pros:**
- ✅ $5/month free credit (lasts months)
- ✅ Simple GitHub integration
- ✅ Automatic deployments
- ✅ Decent uptime

**Cons:**
- ❌ Free tier limited to $5
- ❌ Credits run out eventually

**Steps:**

1. **Sign Up**
   ```bash
   Go to https://railway.app
   Sign up with GitHub
   ```

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your bot repo

3. **Configure**
   - Add variables in Railway UI
   - Railway auto-detects Python
   - Add `Dockerfile`

4. **Deploy**
   - Push code to GitHub
   - Railway auto-deploys
   - Bot runs 24/7

---

### **3. RENDER (Alternative) 🎨**

**Pros:**
- ✅ Free tier available
- ✅ Good uptime
- ✅ Easy setup

**Cons:**
- ❌ Free tier spins down after 15 min inactivity
- ❌ Takes 30 sec to wake up

**Steps:**

1. **Sign Up**
   ```bash
   Go to https://render.com
   Sign up with GitHub
   ```

2. **Create Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub
   - Select bot repository

3. **Configure**
   - **Runtime**: Python 3.11
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python bot.py`

4. **Add Secrets**
   - Add environment variables in "Environment" tab
   - Deploy!

---

### **4. REPLIT (Simplest) 🎯**

**Pros:**
- ✅ Super easy for beginners
- ✅ No Git required
- ✅ Works immediately
- ✅ Free tier

**Cons:**
- ❌ Spins down after inactivity
- ❌ Limited resources

**Steps:**

1. Go to https://replit.com
2. Click "Create Repl"
3. Select "Python"
4. Upload all your bot files
5. Create `.env` file with your secrets
6. Click "Run"
7. Bot works! 🎉

---

### **5. HEROKU (Legacy) ⚠️**

⚠️ **Note:** Heroku removed free tier in Nov 2022. Not recommended.

---

## 🔄 Keep Bot Running 24/7

### Problem: Free tier "spins down" after inactivity

**Solution:** Use a health check service to keep bot awake.

```bash
# Add UptimeRobot (free)
Go to https://uptimerobot.com
Create account
Add HTTP monitor: https://your-bot-url.herokuapp.com:8000
Check every 5 minutes
```

The bot's built-in health check server (port 8000) responds instantly, keeping it awake!

---

## 📋 Deployment Checklist

Before deploying:

- [ ] `.env` file created locally (NOT pushed to GitHub)
- [ ] `credentials.json` or `GOOGLE_CREDS` set up
- [ ] Bot token obtained from Discord
- [ ] Google Sheets created and shared with service account
- [ ] Repository pushed to GitHub
- [ ] Python version is 3.9+
- [ ] `requirements.txt` updated
- [ ] `Dockerfile` ready for docker deployment

---

## 🆘 Troubleshooting Deployments

### Bot goes offline after 30 minutes (Render/Replit)
- Add UptimeRobot for pings every 5 minutes
- Use Koyeb/Railway instead (better uptime)

### "ImportError: No module named 'discord'"
- Check `requirements.txt` has all packages
- Rebuild after updating requirements

### Environment variables not working
- Verify exact variable names in hosting platform
- Don't use quotes: `BOT_TOKEN=abc123` not `BOT_TOKEN="abc123"`

### Google Sheets not updating
- Verify service account email has sheet access
- Check `GOOGLE_CREDS` or `credentials.json` path
- Ensure `SHEET_NAME` matches exactly

### Commands not showing in Discord
- Invite bot with correct scopes: `bot` + `applications.commands`
- Restart bot after changes
- Wait 30 seconds for command sync

---

## 💰 Cost Comparison

| Platform | Cost | Uptime | Setup |
|----------|------|--------|-------|
| **Koyeb** | Free | 99.9% | Easy |
| **Railway** | $5 credit | 99% | Easy |
| **Render** | Free* | 50% (spins down) | Easy |
| **Replit** | Free* | 50% (spins down) | Easiest |
| **VPS (DigitalOcean)** | $5/mo | 99.99% | Medium |

*Free tiers with limitations. Use UptimeRobot to extend uptime.

---

## 🎯 Recommended Setup

**For maximum uptime + free cost:**

1. **Use Koyeb** (best free option)
2. **Add UptimeRobot** (keeps it awake)
3. **GitHub auto-deploys** (updates instantly)
4. **Google Sheets backup** (data always safe)

**Result:** Bot runs 24/7 completely free! ✨

---

## 📚 Quick Links

- [Koyeb Docs](https://koyeb.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Replit Docs](https://docs.replit.com)
- [UptimeRobot](https://uptimerobot.com)

---

## ✅ Success!

Once deployed, your bot will:
- ✅ Run 24/7
- ✅ Log all FiveM activities
- ✅ Update Google Sheets automatically
- ✅ Respond to Discord commands instantly
- ✅ Cost you $0! 🎉

Happy hosting! 🚀
