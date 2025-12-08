"""
Account management system for Major Pick application.
Handles account creation, login, and data persistence.
"""

import json
import os
from pathlib import Path
from hashlib import sha256

class AccountManager:
    def __init__(self):
        self.accounts_dir = Path("accounts")
        self.accounts_dir.mkdir(exist_ok=True)
        self.accounts_file = self.accounts_dir / "accounts.json"
        self.current_user = None
        self.current_user_data = {}
        
        #initialize accounts file if it doesn't exist
        if not self.accounts_file.exists():
            self._save_accounts_index({})
    
    def _hash_password(self, password):
        """Hash password using SHA-256."""
        return sha256(password.encode()).hexdigest()
    
    def _load_accounts_index(self):
        """Load the accounts index file."""
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_accounts_index(self, accounts):
        """Save the accounts index file."""
        with open(self.accounts_file, 'w') as f:
            json.dump(accounts, f, indent=2)
    
    def _get_user_file(self, username):
        """Get the file path for a user's data."""
        return self.accounts_dir / f"{username}_data.json"
    
    def create_account(self, username, password):
        """
        Create a new account.
        Returns (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters."
        
        accounts = self._load_accounts_index()
        
        if username in accounts:
            return False, "Username already exists."
        
        #add to accounts index
        accounts[username] = {
            "password_hash": self._hash_password(password),
            "created_at": str(Path(self.accounts_file).stat().st_mtime)
        }
        self._save_accounts_index(accounts)
        
        #create empty user data file
        user_data = {
            "username": username,
            "schedule": [],
            "quiz_results": None,
            "selected_major": None,
            "preferences": {}
        }
        self._save_user_data(username, user_data)
        
        return True, "Account created successfully!"
    
    def login(self, username, password):
        """
        Login to an existing account.
        Returns (success: bool, message: str)
        """
        accounts = self._load_accounts_index()
        
        if username not in accounts:
            return False, "Username not found."
        
        password_hash = self._hash_password(password)
        if accounts[username]["password_hash"] != password_hash:
            return False, "Incorrect password."
        
        #load user data
        self.current_user = username
        self.current_user_data = self._load_user_data(username)
        
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        """Logout current user."""
        self.current_user = None
        self.current_user_data = {}
    
    def is_logged_in(self):
        """Check if a user is currently logged in."""
        return self.current_user is not None
    
    def _load_user_data(self, username):
        """Load user data from file."""
        user_file = self._get_user_file(username)
        try:
            with open(user_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "username": username,
                "schedule": [],
                "quiz_results": None,
                "selected_major": None,
                "preferences": {}
            }
    
    def _save_user_data(self, username, data):
        """Save user data to file."""
        user_file = self._get_user_file(username)
        with open(user_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_current_user_data(self, schedule_data, quiz_results=None, selected_major=None):
        """
        Save current user's data.
        Returns (success: bool, message: str)
        """
        if not self.is_logged_in():
            return False, "No user logged in."
        
        self.current_user_data["schedule"] = schedule_data
        if quiz_results is not None:
            self.current_user_data["quiz_results"] = quiz_results
        if selected_major is not None:
            self.current_user_data["selected_major"] = selected_major
        
        self._save_user_data(self.current_user, self.current_user_data)
        return True, "Data saved successfully!"
    
    def get_current_user_data(self):
        """Get current user's data."""
        return self.current_user_data.copy()
    
    def get_current_username(self):
        """Get current username."""
        return self.current_user