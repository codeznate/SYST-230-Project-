"""
-> Quiz dialog popup, generating quizzes and fetching results.
"""

from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QRadioButton, QButtonGroup,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

class QuizDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Undecided Student Quiz")
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout(self)

        self.questions = [
            "I prefer to be a leader and not a follower.",
            "I prefer to work for myself and not others.",
            "I work best with a structured schedule.",
            "I enjoy working with people.",
            "I like it when my actions make a difference.",
            "I can comprehend and synthesize large chunks of text very well.",
            "I am good at articulating myself verbally or in writing.",
            "I prefer to be creative than to have constraints.",
            "I like being active and moving around.",
            "I like traveling and experiencing new cultures",
        ]
        self.current_question = 0
        self.answers = []

        #quiz label
        self.quiz_label = QLabel("")
        self.quiz_label.setWordWrap(True)
        self.quiz_label.setStyleSheet("font-weight:bold; font-size:14px;")
        self.layout.addWidget(self.quiz_label)

        #answer buttons
        self.answer_group = QButtonGroup(self)
        self.answer_radios = []
        for text in ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]:
            rb = QRadioButton(text)
            self.answer_group.addButton(rb)
            self.layout.addWidget(rb)
            self.answer_radios.append(rb)

        #next button
        self.next_btn = QPushButton("Next Question")
        self.next_btn.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_btn)

        # Load first question
        self.load_question()

    def load_question(self):
        if self.current_question >= len(self.questions):
            return
        q = self.questions[self.current_question]
        self.quiz_label.setText(f"Question {self.current_question + 1} of {len(self.questions)}:\n{q}")
        #clear previous selections
        for rb in self.answer_radios:
            rb.setAutoExclusive(False)
            rb.setChecked(False)
            rb.setAutoExclusive(True)

    def next_question(self):
        selected = self.answer_group.checkedButton()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select an answer.")
            return

        self.answers.append(selected.text())
        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.compute_result()
        else:
            self.load_question()

    def compute_result(self):
        majors = [
            "Business", "Engineering", "Computer Science", "Performing Arts",
            "Visual Arts", "Health Science", "Biology", "Psychology",
            "Music", "Economics"
        ]
        scores = {m: 0 for m in majors}

        value_map = {
            "Strongly agree": 3,
            "Agree": 2,
            "Disagree": 0,
            "Strongly disagree": -1
        }

        q_map = [
            ["Business", "Economics"],
            ["Business", "Computer Science"],
            ["Engineering", "Health Science"],
            ["Psychology", "Health Science"],
            ["Health Science", "Biology"],
            ["Psychology", "Economics"],
            ["Performing Arts", "Psychology"],
            ["Visual Arts", "Music", "Performing Arts"],
            ["Health Science", "Performing Arts"],
            ["Business", "Economics"]
        ]

        for i, ans in enumerate(self.answers):
            value = value_map.get(ans, 0)
            for m in q_map[i]:
                if m in scores:
                    scores[m] += value

        recommended = max(scores, key=scores.get)
        result_text = f"Recommended Major: {recommended}\n\nScores:\n"
        for m, s in scores.items():
            result_text += f"{m}: {s}\n"

        QMessageBox.information(self, "Quiz Result", result_text)
        self.accept()