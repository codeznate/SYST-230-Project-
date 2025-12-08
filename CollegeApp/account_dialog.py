"""
Account dialog for login and account creation.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QTabWidget, QWidget
)
from PySide6.QtCore import Qt

class AccountDialog(QDialog):
    def __init__(self, account_manager, parent=None):
        super().__init__(parent)
        self.account_manager = account_manager
        self.setWindowTitle("Account Management")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        #create tab widget for Login and Create Account
        self.tabs = QTabWidget()
        
        #login Tab
        login_tab = QWidget()
        login_layout = QVBoxLayout(login_tab)
        
        login_layout.addWidget(QLabel("Login to your account:"))
        login_layout.addSpacing(20)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")
        login_layout.addWidget(QLabel("Username:"))
        login_layout.addWidget(self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(QLabel("Password:"))
        login_layout.addWidget(self.login_password)
        
        login_layout.addSpacing(20)
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(login_btn)
        
        login_layout.addStretch()
        
        #create Account Tab
        create_tab = QWidget()
        create_layout = QVBoxLayout(create_tab)
        
        create_layout.addWidget(QLabel("Create a new account:"))
        create_layout.addSpacing(20)
        
        self.create_username = QLineEdit()
        self.create_username.setPlaceholderText("Username (min 3 characters)")
        create_layout.addWidget(QLabel("Username:"))
        create_layout.addWidget(self.create_username)
        
        self.create_password = QLineEdit()
        self.create_password.setPlaceholderText("Password (min 4 characters)")
        self.create_password.setEchoMode(QLineEdit.Password)
        create_layout.addWidget(QLabel("Password:"))
        create_layout.addWidget(self.create_password)
        
        self.create_password_confirm = QLineEdit()
        self.create_password_confirm.setPlaceholderText("Confirm password")
        self.create_password_confirm.setEchoMode(QLineEdit.Password)
        create_layout.addWidget(QLabel("Confirm Password:"))
        create_layout.addWidget(self.create_password_confirm)
        
        create_layout.addSpacing(20)
        
        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.handle_create_account)
        create_layout.addWidget(create_btn)
        
        create_layout.addStretch()
        
        #add tabs
        self.tabs.addTab(login_tab, "Login")
        self.tabs.addTab(create_tab, "Create Account")
        
        layout.addWidget(self.tabs)
        
        #cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
    
    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        success, message = self.account_manager.login(username, password)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", message)
    
    def handle_create_account(self):
        username = self.create_username.text().strip()
        password = self.create_password.text()
        password_confirm = self.create_password_confirm.text()
        
        if password != password_confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        
        success, message = self.account_manager.create_account(username, password)
        
        if success:
            QMessageBox.information(self, "Success", message)
            #auto-login after account creation
            self.account_manager.login(username, password)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)