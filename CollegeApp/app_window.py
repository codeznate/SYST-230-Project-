from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox,
    QGroupBox, QScrollArea, QHBoxLayout, QLineEdit, QCheckBox, QDialog, QTextEdit
)
from distro import info
import schedule_grid
from quiz_dialog import QuizDialog
from descriptions import major_descriptions
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

        self.layout = QHBoxLayout(self)

        # ------------------ RIGHT PANEL ------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.right_layout = QVBoxLayout(container)

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
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
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
        dialog.exec()

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