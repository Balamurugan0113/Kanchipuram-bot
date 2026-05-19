"""
🎮 KANCHIPURAM BOT - FiveM Business Logger
Tracks grinding, crafting, and storage logs for the FiveM server
Built with Discord.py 2.4.0
"""

import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from dotenv import load_dotenv
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from database import FiveMLogs, BUSINESS_CATEGORIES

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────
# BOT CONFIGURATION
# ─────────────────────────────────────────

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME", "Kanchipuram FiveM Logs")
MANAGER_ROLE = os.getenv("MANAGER_ROLE", "Server Developers")
MEMBER_ROLE = os.getenv("MEMBER_ROLE", "KPM Recycle")
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found in environment variables!")

# ─────────────────────────────────────────
# BOT SETUP
# ─────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Global database instance
db: FiveMLogs = None

# ─────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────

def is_manager(interaction: discord.Interaction) -> bool:
    """Check if user has manager role"""
    return any(r.name == MANAGER_ROLE for r in interaction.user.roles)

def is_member(interaction: discord.Interaction) -> bool:
    """Check if user has member role"""
    return any(r.name in [MEMBER_ROLE, MANAGER_ROLE] for r in interaction.user.roles)

def get_color(category: str) -> int:
    """Get color for category"""
    colors = {
        "Grinding": 0x3498db,  # Blue
        "Crafting": 0x2ecc71,  # Green
        "Sales": 0xf39c12,     # Orange
        "Storage": 0x9b59b6    # Purple
    }
    return colors.get(category, 0x95a5a6)

# Autocomplete functions
async def autocomplete_category(interaction: discord.Interaction, current: str):
    """Autocomplete for business categories"""
    return [
        Choice(name=cat, value=cat)
        for cat in BUSINESS_CATEGORIES
        if current.lower() in cat.lower()
    ]

async def autocomplete_item(interaction: discord.Interaction, current: str):
    """Autocomplete for storage items"""
    storage = db.get_storage()
    items = set()
    for category_items in storage.values():
        items.update(category_items.keys())
    return [
        Choice(name=item, value=item)
        for item in items
        if current.lower() in item.lower()
    ][:25]

# ─────────────────────────────────────────
# BOT EVENTS
# ─────────────────────────────────────────

@bot.event
async def on_ready():
    """Bot ready event"""
    global db

    if db is None:
        try:
            db = FiveMLogs(SHEET_NAME)
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            return

    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ Synced {len(synced)} guild command(s) to guild {GUILD_ID}")
        except Exception as e:
            print(f"❌ Guild sync error: {e}")
    else:
        try:
            synced = await bot.tree.sync()
            print(f"✅ Synced {len(synced)} global command(s)")
        except Exception as e:
            print(f"❌ Global sync error: {e}")

    print(f"✅ Logged in as {bot.user}")
    print(f"📊 Database initialized: {SHEET_NAME}")
    print(f"🎮 Ready to log FiveM business activities!")

# ─────────────────────────────────────────
# SLASH COMMANDS - LOGGING
# ─────────────────────────────────────────

@bot.tree.command(name="log_grind", description="Log a grinding activity")
@app_commands.describe(
    item="Item being ground/processed",
    amount="Amount processed",
    screenshot="Screenshot proof",
    member="Member who did the activity (optional)"
)
@app_commands.autocomplete(item=autocomplete_item)
async def log_grind(
    interaction: discord.Interaction,
    item: str,
    amount: int,
    screenshot: discord.Attachment,
    member: discord.Member = None
):
    """Log grinding activity"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()
    target_user = member or interaction.user
    user_name = target_user.display_name

    success = db.add_log_entry(
        user=user_name,
        category="Grinding",
        action="LOG",
        item=item,
        amount=amount,
        screenshot_url=screenshot.url,
        user_id=str(target_user.id)
    )

    if success:
        embed = discord.Embed(
            title="⚙️ Grinding Activity Logged",
            color=get_color("Grinding"),
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Item", value=item, inline=True)
        embed.add_field(name="Amount", value=str(amount), inline=True)
        embed.add_field(name="Member", value=target_user.mention, inline=True)
        embed.set_image(url=screenshot.url)
        embed.set_footer(text="✅ Logged to database")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to log entry", ephemeral=True)

@bot.tree.command(name="log_craft", description="Log a crafting activity")
@app_commands.describe(
    item="Item being crafted",
    amount="Amount crafted",
    screenshot="Screenshot proof",
    member="Member who did the crafting (optional)"
)
@app_commands.autocomplete(item=autocomplete_item)
async def log_craft(
    interaction: discord.Interaction,
    item: str,
    amount: int,
    screenshot: discord.Attachment,
    member: discord.Member = None
):
    """Log crafting activity"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()
    target_user = member or interaction.user
    user_name = target_user.display_name

    success = db.add_log_entry(
        user=user_name,
        category="Crafting",
        action="LOG",
        item=item,
        amount=amount,
        screenshot_url=screenshot.url,
        user_id=str(target_user.id)
    )

    if success:
        embed = discord.Embed(
            title="🔨 Crafting Activity Logged",
            color=get_color("Crafting"),
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Item", value=item, inline=True)
        embed.add_field(name="Amount", value=str(amount), inline=True)
        embed.add_field(name="Member", value=target_user.mention, inline=True)
        embed.set_image(url=screenshot.url)
        embed.set_footer(text="✅ Logged to database")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to log entry", ephemeral=True)

@bot.tree.command(name="log_sale", description="Log a sales activity")
@app_commands.describe(
    item="Item being sold",
    amount="Amount sold",
    screenshot="Screenshot proof",
    member="Member who made the sale (optional)"
)
@app_commands.autocomplete(item=autocomplete_item)
async def log_sale(
    interaction: discord.Interaction,
    item: str,
    amount: int,
    screenshot: discord.Attachment,
    member: discord.Member = None
):
    """Log sales activity"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()
    target_user = member or interaction.user
    user_name = target_user.display_name

    success = db.add_log_entry(
        user=user_name,
        category="Sales",
        action="LOG",
        item=item,
        amount=amount,
        screenshot_url=screenshot.url,
        user_id=str(target_user.id)
    )

    if success:
        embed = discord.Embed(
            title="💰 Sale Activity Logged",
            color=get_color("Sales"),
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Item", value=item, inline=True)
        embed.add_field(name="Amount", value=str(amount), inline=True)
        embed.add_field(name="Member", value=target_user.mention, inline=True)
        embed.set_image(url=screenshot.url)
        embed.set_footer(text="✅ Logged to database")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to log entry", ephemeral=True)

# ─────────────────────────────────────────
# SLASH COMMANDS - STORAGE MANAGEMENT
# ─────────────────────────────────────────

@bot.tree.command(name="storage_add", description="Add items to storage")
@app_commands.describe(
    category="Storage category (Grinding/Crafting/Sales/Storage)",
    item="Item name",
    amount="Amount to add"
)
@app_commands.autocomplete(category=autocomplete_category)
async def storage_add(
    interaction: discord.Interaction,
    category: str,
    item: str,
    amount: int
):
    """Add items to storage"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    if db.update_storage(category, item, amount, action="add"):
        embed = discord.Embed(
            title="✅ Storage Updated",
            color=get_color(category),
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Category", value=category, inline=True)
        embed.add_field(name="Item", value=item, inline=True)
        embed.add_field(name="Added", value=f"+{amount}", inline=True)
        embed.add_field(name="Added By", value=interaction.user.mention, inline=False)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to update storage", ephemeral=True)

@bot.tree.command(name="storage_remove", description="Remove items from storage")
@app_commands.describe(
    category="Storage category",
    item="Item name",
    amount="Amount to remove"
)
@app_commands.autocomplete(category=autocomplete_category)
@app_commands.autocomplete(item=autocomplete_item)
async def storage_remove(
    interaction: discord.Interaction,
    category: str,
    item: str,
    amount: int
):
    """Remove items from storage"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    if db.update_storage(category, item, amount, action="remove"):
        embed = discord.Embed(
            title="✅ Storage Updated",
            color=0xe74c3c,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Category", value=category, inline=True)
        embed.add_field(name="Item", value=item, inline=True)
        embed.add_field(name="Removed", value=f"-{amount}", inline=True)
        embed.add_field(name="Removed By", value=interaction.user.mention, inline=False)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(
            f"❌ Failed to remove storage. Check if you have enough of that item.",
            ephemeral=True
        )

@bot.tree.command(name="storage_view", description="View current storage status")
@app_commands.describe(
    category="Specific category to view (optional)"
)
@app_commands.autocomplete(category=autocomplete_category)
async def storage_view(
    interaction: discord.Interaction,
    category: str = None
):
    """View storage"""
    await interaction.response.defer()

    if category:
        items = db.get_storage_by_category(category)
        embed = discord.Embed(
            title=f"📦 {category} Storage",
            color=get_color(category),
            timestamp=datetime.now(timezone.utc)
        )
        if items:
            for item, amount in items.items():
                embed.add_field(name=item, value=f"{amount} units", inline=True)
        else:
            embed.description = f"📭 No items in {category} storage"
        await interaction.followup.send(embed=embed)
    else:
        storage = db.get_storage()
        embed = discord.Embed(
            title="📊 Complete Storage Status",
            color=0x3498db,
            timestamp=datetime.now(timezone.utc)
        )

        total_items = 0
        for cat, items in storage.items():
            if items:
                cat_total = sum(items.values())
                total_items += cat_total
                item_list = "\n".join(f"  • {k}: {v}" for k, v in items.items())
                embed.add_field(name=f"🔹 {cat} ({cat_total})", value=item_list, inline=False)
            else:
                embed.add_field(name=f"🔹 {cat} (Empty)", value="📭", inline=False)

        embed.set_footer(text=f"📊 Total items in storage: {total_items}")
        await interaction.followup.send(embed=embed)

# ─────────────────────────────────────────
# SLASH COMMANDS - STATISTICS
# ─────────────────────────────────────────

@bot.tree.command(name="stats", description="View business statistics")
async def stats(interaction: discord.Interaction):
    """View statistics"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()
    stats_data = db.get_stats()

    embed = discord.Embed(
        title="📊 Business Statistics",
        color=0x3498db,
        timestamp=datetime.now(timezone.utc)
    )

    # Transaction counts
    embed.add_field(
        name="📈 Total Transactions",
        value=str(stats_data["total_transactions"]),
        inline=True
    )

    # Category breakdown
    cat_text = "\n".join(
        f"• {cat}: {count}"
        for cat, count in stats_data["total_by_category"].items()
    )
    embed.add_field(name="🎯 By Category", value=cat_text, inline=True)

    # Top users
    if stats_data["total_by_user"]:
        top_users = sorted(
            stats_data["total_by_user"].items(),
            key=lambda x: -x[1]
        )[:5]
        top_text = "\n".join(f"• {user}: {count}" for user, count in top_users)
        embed.add_field(name="👥 Top Contributors", value=top_text, inline=False)

    await interaction.followup.send(embed=embed)

@bot.tree.command(name="user_stats", description="View specific user statistics")
@app_commands.describe(member="Member to check stats for")
async def user_stats(interaction: discord.Interaction, member: discord.Member):
    """View user statistics"""
    if not is_member(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MEMBER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()
    user_stats_data = db.get_user_stats(member.display_name)

    embed = discord.Embed(
        title=f"👤 {member.display_name} Statistics",
        color=0x3498db,
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(name="📝 Actions", value=str(user_stats_data["actions"]), inline=True)
    embed.add_field(name="📊 Items Added", value=str(user_stats_data["items_added"]), inline=True)

    await interaction.followup.send(embed=embed)

# ─────────────────────────────────────────
# SLASH COMMANDS - ADMIN
# ─────────────────────────────────────────

@bot.tree.command(name="admin_clear_logs", description="[Admin] Clear all logs")
async def admin_clear_logs(interaction: discord.Interaction):
    """Clear all logs"""
    if not is_manager(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MANAGER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    if db.clear_logs():
        embed = discord.Embed(
            title="🗑️ Logs Cleared",
            color=0xe74c3c,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Cleared By", value=interaction.user.mention, inline=True)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to clear logs", ephemeral=True)

@bot.tree.command(name="admin_reset_storage", description="[Admin] Reset all storage")
async def admin_reset_storage(interaction: discord.Interaction):
    """Reset all storage"""
    if not is_manager(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MANAGER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    if db.reset_storage():
        embed = discord.Embed(
            title="🔄 Storage Reset",
            color=0xe74c3c,
            timestamp=datetime.now(timezone.utc)
        )
        embed.description = "All storage categories have been cleared"
        embed.add_field(name="Reset By", value=interaction.user.mention, inline=True)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to reset storage", ephemeral=True)

@bot.tree.command(name="admin_clear_user", description="[Admin] Clear specific user's data")
@app_commands.describe(member="Member to clear data for")
async def admin_clear_user(interaction: discord.Interaction, member: discord.Member):
    """Clear user data"""
    if not is_manager(interaction):
        await interaction.response.send_message(
            f"❌ You need the **{MANAGER_ROLE}** role!",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    if db.clear_user_data(member.display_name):
        embed = discord.Embed(
            title="🧹 User Data Cleared",
            color=0xe74c3c,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Cleared By", value=interaction.user.mention, inline=True)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Failed to clear user data", ephemeral=True)

# ─────────────────────────────────────────
# HEALTH CHECK SERVER (For Koyeb/Railway)
# ─────────────────────────────────────────

class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP health check handler for free hosting"""
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK - Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass  # Suppress logging

def run_health_server():
    """Run health check server"""
    server = HTTPServer(("0.0.0.0", 8000), HealthCheckHandler)
    print("🔧 Health check server running on port 8000")
    server.serve_forever()

# ─────────────────────────────────────────
# BOT STARTUP
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Start health check server in background
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    # Run bot
    try:
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        print("\n👋 Bot shutting down...")
    except Exception as e:
        print(f"❌ Bot error: {e}")
