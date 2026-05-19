"""
Database Manager - Handles Google Sheets Integration
Manages all data persistence for FiveM business logs
"""

import json
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ─────────────────────────────────────────
# WORKSHEETS & STRUCTURE
# ─────────────────────────────────────────

WORKSHEETS = {
    "LOGS": "Logs",  # All transaction logs
    "STATS": "Stats",  # Statistics and summaries
    "DATA": "Data",  # Persistent JSON data
    "STORAGE": "Storage",  # Current inventory/storage state
}

BUSINESS_CATEGORIES = ["Grinding", "Crafting", "Storage", "Sales"]

# ─────────────────────────────────────────
# GOOGLE SHEETS CONNECTION
# ─────────────────────────────────────────

class GoogleSheetsDB:
    def __init__(self, sheet_name: str):
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self._connect()

    def _connect(self):
        """Initialize Google Sheets connection"""
        creds_json = os.getenv("GOOGLE_CREDS")
        creds_file = os.getenv("GOOGLE_CREDS_FILE", "credentials.json")

        if creds_json:
            try:
                creds_info = json.loads(creds_json)
                creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
            except Exception as e:
                print(f"[DB Error] Failed to parse GOOGLE_CREDS env variable: {e}")
                raise
        else:
            if not os.path.exists(creds_file):
                raise FileNotFoundError(
                    f"Credentials file not found: {creds_file}\n"
                    "Please set GOOGLE_CREDS env variable or create credentials.json"
                )
            creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)

        self.client = gspread.authorize(creds)
        try:
            self.sheet = self.client.open(self.sheet_name)
            print(f"✅ Connected to Google Sheet: {self.sheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"❌ Sheet '{self.sheet_name}' not found. Creating new sheet...")
            raise

    def get_worksheet(self, ws_name: str):
        """Get or create a worksheet"""
        try:
            return self.sheet.worksheet(ws_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"   Creating worksheet: {ws_name}")
            return self.sheet.add_worksheet(title=ws_name, rows=1000, cols=15)

    def clear_worksheet(self, ws_name: str):
        """Clear all data from worksheet"""
        ws = self.get_worksheet(ws_name)
        ws.clear()
        return ws


# ─────────────────────────────────────────
# IN-MEMORY CACHE
# ─────────────────────────────────────────

class DataCache:
    """In-memory cache for business data"""
    
    def __init__(self):
        self.data = None
        self.last_updated = None

    def initialize(self, initial_data: Dict):
        """Initialize cache with data"""
        self.data = initial_data
        self.last_updated = datetime.now(timezone.utc)

    def update(self, data: Dict):
        """Update cache"""
        self.data = data
        self.last_updated = datetime.now(timezone.utc)

    def get(self) -> Dict:
        """Get cached data"""
        if self.data is None:
            raise RuntimeError("Cache not initialized")
        return self.data

    def is_stale(self, max_age_seconds: int = 300) -> bool:
        """Check if cache is older than max_age"""
        if self.last_updated is None:
            return True
        age = (datetime.now(timezone.utc) - self.last_updated).total_seconds()
        return age > max_age_seconds


# ─────────────────────────────────────────
# DATA MANAGER
# ─────────────────────────────────────────

class FiveMLogs:
    """Manages FiveM business logging"""
    
    def __init__(self, sheet_name: str):
        self.db = GoogleSheetsDB(sheet_name)
        self.cache = DataCache()
        self._ensure_worksheets()
        self._load_data()

    def _ensure_worksheets(self):
        """Ensure all worksheets exist"""
        for ws_name in WORKSHEETS.values():
            self.db.get_worksheet(ws_name)

    def _load_data(self) -> Dict:
        """Load data from sheets"""
        try:
            ws = self.db.get_worksheet(WORKSHEETS["DATA"])
            val = ws.acell("A1").value
            if val:
                data = json.loads(val)
            else:
                data = self._create_default_data()
                self._save_to_sheets(data)
            self.cache.initialize(data)
            return data
        except Exception as e:
            print(f"[Load Error] {e}")
            data = self._create_default_data()
            self.cache.initialize(data)
            return data

    def _create_default_data(self) -> Dict:
        """Create default data structure"""
        return {
            "storage": {
                "Grinding": {},  # item: amount
                "Crafting": {},
                "Sales": {}
            },
            "stats": {
                "total_by_category": {cat: 0 for cat in BUSINESS_CATEGORIES},
                "total_by_user": {},
                "total_transactions": 0,
                "user_actions": {}
            },
            "logs": []  # Historical logs
        }

    def save_data(self, data: Dict):
        """Save data to Google Sheets"""
        self.cache.update(data)
        try:
            ws = self.db.get_worksheet(WORKSHEETS["DATA"])
            ws.update("A1", [[json.dumps(data, indent=2)]])
        except Exception as e:
            print(f"[Save Error] {e}")

    def get_data(self) -> Dict:
        """Get data from cache or sheets"""
        return self.cache.get()

    # ─────────────────────────────────────────
    # LOGGING OPERATIONS
    # ─────────────────────────────────────────

    def add_log_entry(
        self,
        user: str,
        category: str,
        action: str,
        item: str,
        amount: int,
        screenshot_url: str = "",
        user_id: str = ""
    ) -> bool:
        """Add a log entry"""
        try:
            ws = self.db.get_worksheet(WORKSHEETS["LOGS"])
            self._ensure_log_headers(ws)

            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            image_formula = f'=IMAGE("{screenshot_url}")' if screenshot_url else ""

            ws.append_row(
                [timestamp, user, category, action, item, amount, image_formula, user_id],
                value_input_option="USER_ENTERED"
            )

            # Update stats
            data = self.get_data()
            data["stats"]["total_transactions"] += 1
            data["stats"]["total_by_category"][category] = data["stats"]["total_by_category"].get(category, 0) + 1
            data["stats"]["total_by_user"][user] = data["stats"]["total_by_user"].get(user, 0) + 1
            data["stats"]["user_actions"][user] = data["stats"]["user_actions"].get(user, 0) + 1

            self.save_data(data)
            return True
        except Exception as e:
            print(f"[Log Error] {e}")
            return False

    def _ensure_log_headers(self, ws):
        """Ensure log worksheet has headers"""
        if not ws.row_values(1):
            ws.append_row(["Timestamp", "User", "Category", "Action", "Item", "Amount", "Screenshot", "User ID"])

    # ─────────────────────────────────────────
    # STORAGE OPERATIONS
    # ─────────────────────────────────────────

    def update_storage(self, category: str, item: str, amount: int, action: str = "add") -> bool:
        """Update storage count"""
        try:
            if category not in BUSINESS_CATEGORIES:
                return False

            data = self.get_data()
            if action == "add":
                data["storage"][category][item] = data["storage"][category].get(item, 0) + amount
            elif action == "remove":
                current = data["storage"][category].get(item, 0)
                if current < amount:
                    return False
                data["storage"][category][item] = current - amount
            elif action == "set":
                data["storage"][category][item] = amount

            self.save_data(data)
            self._update_storage_sheet(data)
            return True
        except Exception as e:
            print(f"[Storage Update Error] {e}")
            return False

    def _update_storage_sheet(self, data: Dict):
        """Update storage summary sheet"""
        try:
            ws = self.db.get_worksheet(WORKSHEETS["STORAGE"])
            ws.clear()

            rows = [
                ["📦 KANCHIPURAM FiveM - STORAGE STATUS", ""],
                [f"Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}", ""],
                []
            ]

            for category in BUSINESS_CATEGORIES:
                rows.append([f"🔹 {category}", ""])
                storage = data["storage"].get(category, {})
                if storage:
                    for item, amount in storage.items():
                        rows.append([f"  • {item}", amount])
                else:
                    rows.append(["  (Empty)", ""])
                rows.append([])

            # Stats section
            rows += [
                ["📊 STATISTICS", ""],
                ["Total Transactions", data["stats"]["total_transactions"]],
                []
            ]

            for category, count in data["stats"]["total_by_category"].items():
                rows.append([f"  {category}", count])

            rows += [[], ["👥 TOP USERS", ""]]
            for user, count in sorted(data["stats"]["total_by_user"].items(), key=lambda x: -x[1])[:10]:
                rows.append([f"  {user}", count])

            ws.update(rows)
        except Exception as e:
            print(f"[Storage Sheet Error] {e}")

    def get_storage(self) -> Dict[str, Dict]:
        """Get current storage"""
        return self.get_data()["storage"]

    def get_storage_by_category(self, category: str) -> Dict:
        """Get storage for specific category"""
        if category not in BUSINESS_CATEGORIES:
            return {}
        return self.get_data()["storage"].get(category, {})

    # ─────────────────────────────────────────
    # STATS OPERATIONS
    # ─────────────────────────────────────────

    def get_stats(self) -> Dict:
        """Get all statistics"""
        return self.get_data()["stats"]

    def get_user_stats(self, user: str) -> Dict:
        """Get stats for specific user"""
        data = self.get_data()
        return {
            "actions": data["stats"]["user_actions"].get(user, 0),
            "items_added": data["stats"]["total_by_user"].get(user, 0)
        }

    # ─────────────────────────────────────────
    # ADMIN OPERATIONS
    # ─────────────────────────────────────────

    def clear_logs(self) -> bool:
        """Clear all logs"""
        try:
            self.db.clear_worksheet(WORKSHEETS["LOGS"])
            self._ensure_log_headers(self.db.get_worksheet(WORKSHEETS["LOGS"]))
            return True
        except Exception as e:
            print(f"[Clear Error] {e}")
            return False

    def reset_storage(self) -> bool:
        """Reset all storage"""
        try:
            data = self.get_data()
            for category in BUSINESS_CATEGORIES:
                data["storage"][category] = {}
            data["stats"] = {
                "total_by_category": {cat: 0 for cat in BUSINESS_CATEGORIES},
                "total_by_user": {},
                "total_transactions": 0,
                "user_actions": {}
            }
            self.save_data(data)
            self._update_storage_sheet(data)
            return True
        except Exception as e:
            print(f"[Reset Error] {e}")
            return False

    def clear_user_data(self, user: str) -> bool:
        """Clear specific user's data"""
        try:
            data = self.get_data()
            if user in data["stats"]["total_by_user"]:
                del data["stats"]["total_by_user"][user]
            if user in data["stats"]["user_actions"]:
                del data["stats"]["user_actions"][user]
            self.save_data(data)
            self._update_storage_sheet(data)
            return True
        except Exception as e:
            print(f"[Clear User Error] {e}")
            return False
