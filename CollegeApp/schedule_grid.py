from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt

START_HOUR = 8
END_HOUR = 25
SLOT_MINUTES = 30

def minutes_to_slot_index(minutes):
    """Convert minutes-from-midnight to grid row index (0-based)."""
    start = START_HOUR * 60
    if minutes < start:
        return None
    index = (minutes - start) // SLOT_MINUTES
    return int(index)


class ScheduleGrid(QWidget):
    """Visual weekly grid for Mon-Fri. 30-minute rows from START_HOUR to END_HOUR."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cols = 5  # Mon-Fri
        total_minutes = (END_HOUR - START_HOUR) * 60
        self.rows = total_minutes // SLOT_MINUTES
        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.setLayout(self.grid)
        self.cell_occupancy = {}  # (col, row) -> widget

        # Build header labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for c, day in enumerate(days):
            lbl = QLabel(day)
            lbl.setStyleSheet("font-weight: bold; border-bottom: 1px solid #ccc;")
            lbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(lbl, 0, c + 1)

        # Time labels on left column
        for r in range(self.rows):
            minutes = START_HOUR * 60 + r * SLOT_MINUTES
            if minutes % 60 == 0:  # label every hour
                hh = minutes // 60
                time_label = QLabel(f"{hh:02d}:00")
                time_label.setFixedWidth(50)
                time_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
                self.grid.addWidget(time_label, r + 1, 0)
            else:
                spacer = QLabel("")
                spacer.setFixedWidth(50)
                self.grid.addWidget(spacer, r + 1, 0)

        # Create empty cells for layout alignment (we'll place class widgets spanning rows)
        for r in range(self.rows):
            for c in range(self.cols):
                placeholder = QLabel("")
                placeholder.setStyleSheet("border: 1px solid #eee; min-height:18px;")
                placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grid.addWidget(placeholder, r + 1, c + 1)

    def add_class_block(self, name, days, start_min, end_min, color="#B3E5FC"):
        """Add a class to the grid. Returns (True,None) or (False,conflicts)."""
        start_idx = minutes_to_slot_index(start_min)
        end_idx = minutes_to_slot_index(end_min)
        if start_idx is None or end_idx is None:
            raise ValueError("Class outside displayable hours")

        # Compute span (ceil if not exactly on slot)
        span = int((end_min - START_HOUR * 60 + SLOT_MINUTES - 1) // SLOT_MINUTES) - start_idx

        # Conflict detection
        conflicts = []
        for d in days:
            for r in range(start_idx, start_idx + span):
                if (d, r) in self.cell_occupancy:
                    conflicts.append((d, r))
        if conflicts:
            return False, conflicts

        # Place a widget spanning rows for each day
        for d in days:
            block = QLabel(name)
            block.setWordWrap(True)
            block.setStyleSheet(f"background:{color}; border:1px solid #0288D1; padding:4px; border-radius:4px;")
            block.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(block, start_idx + 1, d + 1, span, 1)
            for r in range(start_idx, start_idx + span):
                self.cell_occupancy[(d, r)] = block

        return True, None

    def check_conflict(self, days, start_min, end_min):
        """Return True if this class conflicts with existing classes."""
        start_idx = minutes_to_slot_index(start_min)
        if start_idx is None:
            return True
        span = int((end_min - START_HOUR * 60 + SLOT_MINUTES - 1) // SLOT_MINUTES) - start_idx
        for d in days:
            for r in range(start_idx, start_idx + span):
                if (d, r) in self.cell_occupancy:
                    return True
        return False
    
    def get_class_names(self):
        names = {w.text() for w in self.cell_occupancy.values()}
        return sorted(names)
    
    def remove_class(self, class_name):
        to_remove = set()

        # Find all cells occupied by this class
        for (col, row), widget in list(self.cell_occupancy.items()):
            if widget.text() == class_name:
                to_remove.add(widget)

        if not to_remove:
            return False

        for widget in to_remove:
            # Remove the widget from the layout
            self.grid.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        # Remove all entries from cell_occupancy that pointed to this widget
        self.cell_occupancy = {
            key: w for key, w in self.cell_occupancy.items() if w.text() != class_name
        }
        return True