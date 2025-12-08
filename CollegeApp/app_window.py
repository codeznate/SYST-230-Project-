"""
-> This puts everything together, focusing on the widgets and the construction
-> of the application. This serves as the frontend mainly, what the users see
-> and implementing the backend code into buttons and scheduling features.
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox,
    QGroupBox, QScrollArea, QHBoxLayout, QLineEdit, QCheckBox, QDialog, QTextEdit, QMessageBox
)
import schedule_grid
from quiz_dialog import QuizDialog
from descriptions import major_descriptions
from clubs import major_clubs
from account_manage import AccountManager
from account_dialog import AccountDialog
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
import random

class NextClassWidget(QWidget):
    def __init__(self, schedule_grid, parent=None):
        super().__init__(parent)
        self.schedule_grid = schedule_grid
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("Today's Next Class")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.layout.addWidget(self.title_label)

        self.info_label = QLabel("No class info yet")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.info_label, stretch=1)

        self.layout.addStretch()
        self.about_btn = QPushButton("About Us!")
        self.layout.addWidget(self.about_btn)
        self.quiz_btn = QPushButton("Take Quiz")
        self.layout.addWidget(self.quiz_btn)

    def update_info(self):
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute
        current_day = now.weekday()
        days_map = ["Mon", "Tue", "Wed", "Thu", "Fri"]

        next_class = None
        min_time_diff = float('inf')

        for (col, row), widget in self.schedule_grid.cell_occupancy.items():
            if col != current_day:
                continue
            start_min = row * 30 + 8 * 60
            time_diff = start_min - current_minutes
            if time_diff >= 0 and time_diff < min_time_diff:
                min_time_diff = time_diff
                next_class = widget.text()

        if next_class:
            hours, minutes = divmod(min_time_diff, 60)
            self.info_label.setText(
                f"Today: {days_map[current_day]}\n"
                f"Next class: {next_class}\n"
                f"In: {hours}h {minutes}m"
            )
        else:
            self.info_label.setText(f"Today: {days_map[current_day]}\nNo more classes")

class MajorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Major Pick - Scheduling Enabled")
        self.setGeometry(120, 80, 1000, 900)
        
        # Initialize account manager
        self.account_manager = AccountManager()
        self.quiz_result = None

        self.layout = QHBoxLayout(self)

        # ------------------ RIGHT PANEL ------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.right_layout = QVBoxLayout(container)

        self.build_account_section()
        self.build_major_info_section()
        self.build_schedule_section()

        scroll.setWidget(container)
        self.layout.addWidget(scroll)

        # ------------------ LEFT PANEL ------------------
        self.next_class_widget = NextClassWidget(self.schedule_grid)
        self.next_class_widget.quiz_btn.clicked.connect(self.open_quiz_dialog)
        self.next_class_widget.about_btn.clicked.connect(self.show_about_info)
        self.layout.insertWidget(0, self.next_class_widget)

        self.update_next_class_info()
        timer = QTimer(self)
        timer.timeout.connect(self.update_next_class_info)
        timer.start(60000)
        
        self.update_account_display()

    # ------------------ ACCOUNT SECTION ------------------
    def build_account_section(self):
        box = QGroupBox("Account")
        layout = QVBoxLayout()
        
        self.account_status_label = QLabel("Not logged in")
        self.account_status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.account_status_label)
        
        btn_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.open_account_dialog)
        btn_layout.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.handle_logout)
        self.logout_btn.setVisible(False)
        btn_layout.addWidget(self.logout_btn)
        
        layout.addLayout(btn_layout)
        
        btn_layout2 = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.handle_save)
        btn_layout2.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.handle_load)
        self.load_btn.setVisible(False)
        btn_layout2.addWidget(self.load_btn)
        
        layout.addLayout(btn_layout2)
        
        box.setLayout(layout)
        self.right_layout.addWidget(box)
    
    def open_account_dialog(self, auto_load=True):
        dialog = AccountDialog(self.account_manager, self)
        if dialog.exec():
            self.update_account_display()
            # Only load user data if auto_load is True and user has existing data
            if auto_load:
                user_data = self.account_manager.get_current_user_data()
                # Only load if there's actually saved schedule data
                if user_data.get("schedule"):
                    self.load_user_data()
                else:
                    # New account with no data - just update UI elements
                    self.update_remove_dropdown()
                    self.update_next_class_info()
    
    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Logout", 
            "Are you sure you want to logout? Unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.account_manager.logout()
            self.clear_schedule()
            self.update_account_display()
            QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")
    
    def handle_save(self):
        # Gather schedule data first (before any account operations)
        schedule_data = []
        classes_added = set()
        
        for (col, row), widget in self.schedule_grid.cell_occupancy.items():
            class_name = widget.text()
            if class_name not in classes_added:
                # Find all cells for this class to determine days and times
                class_cells = [(c, r) for (c, r), w in self.schedule_grid.cell_occupancy.items() if w.text() == class_name]
                
                days = sorted(set(c for c, r in class_cells))
                rows = [r for c, r in class_cells if c == days[0]]
                start_row = min(rows)
                end_row = max(rows) + 1
                
                start_min = start_row * 30 + 8 * 60
                end_min = end_row * 30 + 8 * 60
                
                schedule_data.append({
                    "name": class_name,
                    "days": days,
                    "start_min": start_min,
                    "end_min": end_min,
                    "color": widget.styleSheet().split("background:")[1].split(";")[0]
                })
                classes_added.add(class_name)
        
        if not self.account_manager.is_logged_in():
            # Prompt to create account or login
            reply = QMessageBox.question(
                self, "Account Required",
                "You need an account to save your data. Would you like to create an account or login?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.open_account_dialog()
                # If still not logged in, don't save
                if not self.account_manager.is_logged_in():
                    return
            else:
                return
        
        # Save data (schedule_data was already gathered before account dialog)
        success, message = self.account_manager.save_current_user_data(
            schedule_data, 
            self.quiz_result,
            self.major_dropdown.currentText()
        )
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)
    
    def handle_load(self):
        if not self.account_manager.is_logged_in():
            QMessageBox.warning(self, "Not Logged In", "Please login first.")
            return
        
        self.load_user_data()
    
    def load_user_data(self):
        """Load user data from account manager."""
        user_data = self.account_manager.get_current_user_data()
        
        # Clear current schedule
        self.clear_schedule()
        
        # Load schedule
        for class_data in user_data.get("schedule", []):
            self.schedule_grid.add_class_block(
                class_data["name"],
                class_data["days"],
                class_data["start_min"],
                class_data["end_min"],
                class_data.get("color", "#CCCCCC")
            )
        
        # Load quiz result
        if user_data.get("quiz_results"):
            self.quiz_result = user_data["quiz_results"]
        
        # Load selected major
        if user_data.get("selected_major"):
            index = self.major_dropdown.findText(user_data["selected_major"])
            if index >= 0:
                self.major_dropdown.setCurrentIndex(index)
        
        self.update_remove_dropdown()
        self.update_next_class_info()
        
        QMessageBox.information(self, "Success", "Data loaded successfully!")
    
    def clear_schedule(self):
        """Clear all classes from the schedule grid."""
        to_remove = list(self.schedule_grid.cell_occupancy.keys())
        for key in to_remove:
            widget = self.schedule_grid.cell_occupancy.pop(key)
            self.schedule_grid.grid.removeWidget(widget)
            widget.deleteLater()
        
        self.update_remove_dropdown()
        self.update_next_class_info()
    
    def update_account_display(self):
        """Update the account section UI based on login status."""
        if self.account_manager.is_logged_in():
            username = self.account_manager.get_current_username()
            self.account_status_label.setText(f"Logged in as: {username}")
            self.login_btn.setVisible(False)
            self.logout_btn.setVisible(True)
            self.load_btn.setVisible(True)
        else:
            self.account_status_label.setText("Not logged in")
            self.login_btn.setVisible(True)
            self.logout_btn.setVisible(False)
            self.load_btn.setVisible(False)

    # ------------------ MAJOR INFO ------------------
    def build_major_info_section(self):
        box = QGroupBox("Major Information")
        layout = QVBoxLayout()

        self.major_dropdown = QComboBox()
        self.major_dropdown.addItems(list(major_descriptions.keys()))
        layout.addWidget(self.major_dropdown)

        btn = QPushButton("Show Info")
        btn.clicked.connect(self.show_major_info_from_dropdown)
        layout.addWidget(btn)

        self.show_clubs_btn = QPushButton("Show Clubs")
        self.show_clubs_btn.clicked.connect(self.show_clubs_for_major)
        layout.addWidget(self.show_clubs_btn)

        self.major_info_label = QLabel("Major info will appear here.")
        self.major_info_label.setWordWrap(True)
        self.major_info_label.setStyleSheet("font-size:16px;")
        layout.addWidget(self.major_info_label)

        box.setLayout(layout)
        self.right_layout.addWidget(box)

    def show_major_info_from_dropdown(self):
        major = self.major_dropdown.currentText()
        info = major_descriptions.get(major)
        if info:
            desc = random.choice(info["descriptions"])
            example = random.choice(info["examples"])
            self.major_info_label.setText(f"{major}\n\n{desc}\n\n{example}")
        else:
            self.major_info_label.setText(f"{major}\n\nNo description available.")

    def show_clubs_for_major(self):
        major = self.major_dropdown.currentText()
        clubs = major_clubs.get(major, [])

        if not clubs:
            msg = "No clubs found for this major."
        else:
            msg = ""
            for club in clubs:
                msg += f"{club['name']}\n{club['description']}\n\n"

        dialog = QDialog(self)
        dialog.setWindowTitle(f"{major} Clubs")
        dialog.setMinimumSize(400, 300)

        dlg_layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(msg)
        dlg_layout.addWidget(text_edit)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(dialog.accept)
        dlg_layout.addWidget(back_btn)

        dialog.exec()

    # ------------------ SCHEDULE ------------------
    def build_schedule_section(self):
        outer = QWidget()
        outer_layout = QVBoxLayout()
        outer.setLayout(outer_layout)

        # ADD CLASS
        input_box = QGroupBox("Add Class")
        input_layout = QVBoxLayout()

        name_row = QHBoxLayout()
        self.class_name_input = QLineEdit()
        self.class_name_input.setPlaceholderText("Class name (e.g. CS112)")
        name_row.addWidget(QLabel("Class:"))
        name_row.addWidget(self.class_name_input)
        input_layout.addLayout(name_row)

        days_row = QHBoxLayout()
        days_row.addWidget(QLabel("Days:"))
        self.day_checks = {}
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            cb = QCheckBox(d)
            self.day_checks[d] = cb
            days_row.addWidget(cb)
        input_layout.addLayout(days_row)

        time_row = QHBoxLayout()
        self.start_hour = QComboBox(); self.start_hour.addItems([f"{i:02d}" for i in range(1, 13)])
        self.start_min = QComboBox(); self.start_min.addItems(["00","15","30","45"])
        self.start_ampm = QComboBox(); self.start_ampm.addItems(["AM","PM"])
        time_row.addWidget(QLabel("Start:"))
        time_row.addWidget(self.start_hour)
        time_row.addWidget(self.start_min)
        time_row.addWidget(self.start_ampm)

        self.end_hour = QComboBox(); self.end_hour.addItems([f"{i:02d}" for i in range(1, 13)])
        self.end_min = QComboBox(); self.end_min.addItems(["00","15","30","45"])
        self.end_ampm = QComboBox(); self.end_ampm.addItems(["AM","PM"])
        time_row.addWidget(QLabel("End:"))
        time_row.addWidget(self.end_hour)
        time_row.addWidget(self.end_min)
        time_row.addWidget(self.end_ampm)

        input_layout.addLayout(time_row)

        add_btn = QPushButton("Add Class")
        add_btn.clicked.connect(self.on_add_class)
        input_layout.addWidget(add_btn)

        self.schedule_status = QLabel("")
        input_layout.addWidget(self.schedule_status)

        input_box.setLayout(input_layout)
        outer_layout.addWidget(input_box)

        # SCHEDULE GRID
        self.schedule_grid = schedule_grid.ScheduleGrid()
        outer_layout.addWidget(self.schedule_grid)

        # REMOVE CLASS
        remove_box = QGroupBox("Remove Class")
        remove_layout = QHBoxLayout()
        self.remove_class_dropdown = QComboBox()
        self.update_remove_dropdown()
        remove_layout.addWidget(self.remove_class_dropdown)

        remove_btn = QPushButton("Remove Class")
        remove_btn.clicked.connect(self.on_remove_class)
        remove_layout.addWidget(remove_btn)

        remove_box.setLayout(remove_layout)
        outer_layout.addWidget(remove_box)

        self.right_layout.addWidget(outer)

    def random_pastel_color(self):
        r = lambda: random.randint(150, 255)
        return f'#{r():02X}{r():02X}{r():02X}'

    # ------------------ ADD CLASS ------------------
    def on_add_class(self):
        name = self.class_name_input.text().strip()
        if not name:
            self.schedule_status.setText("Please enter a class name.")
            return

        days = []
        day_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4}
        for d, cb in self.day_checks.items():
            if cb.isChecked():
                days.append(day_map[d])
        if not days:
            self.schedule_status.setText("Please select at least one day.")
            return

        try:
            start_hour = int(self.start_hour.currentText())
            start_min = int(self.start_min.currentText())
            if self.start_ampm.currentText()=="PM" and start_hour !=12: start_hour+=12
            if self.start_ampm.currentText()=="AM" and start_hour==12: start_hour=0
            start_total = start_hour*60 + start_min

            end_hour = int(self.end_hour.currentText())
            end_min = int(self.end_min.currentText())
            if self.end_ampm.currentText()=="PM" and end_hour !=12: end_hour+=12
            if self.end_ampm.currentText()=="AM" and end_hour==12: end_hour=0
            end_total = end_hour*60 + end_min
        except ValueError:
            self.schedule_status.setText("Invalid time selection.")
            return

        if end_total <= start_total:
            self.schedule_status.setText("End time must be after start time.")
            return

        if self.schedule_grid.check_conflict(days,start_total,end_total):
            self.schedule_status.setText(f"Conflict: {name} overlaps with existing class.")
            return

        color = self.random_pastel_color()
        ok,_ = self.schedule_grid.add_class_block(name,days,start_total,end_total,color=color)
        if ok:
            self.schedule_status.setText(f"Added: {name}")
            self.class_name_input.clear()
            for cb in self.day_checks.values(): cb.setChecked(False)
            self.update_remove_dropdown()
            self.update_next_class_info()
        else:
            self.schedule_status.setText(f"Could not add: {name}")

    # ------------------ REMOVE CLASS ------------------
    def on_remove_class(self):
        class_name = self.remove_class_dropdown.currentText()
        to_remove = []
        for key, widget in self.schedule_grid.cell_occupancy.items():
            if widget.text() == class_name:
                to_remove.append(key)
        for key in to_remove:
            widget = self.schedule_grid.cell_occupancy.pop(key)
            self.schedule_grid.grid.removeWidget(widget)
            widget.deleteLater()
        self.update_remove_dropdown()
        self.update_next_class_info()
        self.schedule_status.setText(f"Removed: {class_name}")

    def update_remove_dropdown(self):
        classes = set(w.text() for w in self.schedule_grid.cell_occupancy.values())
        self.remove_class_dropdown.clear()
        self.remove_class_dropdown.addItems(sorted(classes))

    # ------------------ QUIZ ------------------
    def open_quiz_dialog(self):
        dialog = QuizDialog(self)
        if dialog.exec():
            # Store quiz result if available
            if hasattr(dialog, 'result_data'):
                self.quiz_result = dialog.result_data

    # ------------------ ABOUT ------------------
    def show_about_info(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Us")
        dialog.setMinimumSize(400, 300)
        dlg_layout = QVBoxLayout(dialog)

        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setText(
            "Major Pick helps students select majors aligned with their interests and career goals. "
            "It provides major descriptions, potential career paths, and scheduling tools to plan courses." \
            "\n\nWe understand that choosing a major can be daunting. We're here to help you every step of the way," \
            "we have implemented a quiz to help undecided students find suitable majors based on their preferences."
            "\n\nOur team is dedicated to providing the best resources and support to guide you through your academic journey," \
            "including scheduling features to help you organize your classes effectively."
        )
        dlg_layout.addWidget(about_text)

        quiz_btn = QPushButton("Take Quiz")
        quiz_btn.clicked.connect(self.open_quiz_dialog)
        dlg_layout.addWidget(quiz_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(dialog.accept)
        dlg_layout.addWidget(back_btn)
        dialog.exec()

    # ------------------ NEXT CLASS INFO ------------------
    def update_next_class_info(self):
        self.next_class_widget.update_info()