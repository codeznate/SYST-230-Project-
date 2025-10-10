
"""
EXTERNAL/INTERNAL LIBRARIES
    ***
    tkinter = Interal python module for GUI interface, development, configuration, and design
    ttk = Internal python function from tkinter, upgraded tk widgets
    messagebox = Internal python function from tkinter, function for displaying message boxs with messages upon
    certain conditions. 
    descriptions = External python file for major descriptions for organization and cleanliness. 
"""
import tkinter as tk
from tkinter import ttk, messagebox
from descriptions import major_descriptions

"""
MajorPick GUI Interface project!

"""



class majorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Major Pick")
        self.geometry("800x600")

        # container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # pages holders
        self.frames = {}
        for F in (homePage, decidedPage, quizPage, resultPage, majorInfoPage, aboutPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(homePage)

        menu_bar = tk.Menu(self)
        self.config(menu = menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label = "Home", command = lambda: self.show_frame(homePage))
        file_menu.add_command(label = "Quiz", command= lambda: self.show_frame(quizPage))
        file_menu.add_command(label = "Decided", command = lambda: self.show_frame(decidedPage))
        file_menu.add_separator()
        file_menu.add_command(label = "Exit", command = self.destroy)
        menu_bar.add_cascade(label = "Navigation", menu = file_menu)

        help_menu = tk.Menu(menu_bar, tearoff = 0)
        help_menu.add_command(label = "About", command = lambda: self.show_frame(aboutPage))
        menu_bar.add_cascade(label = "Help", menu = help_menu)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class homePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="Welcome student! Are you currently decided or undecided?", font=("Helvetica", 16))
        label.pack(pady=40)

        # buttons
        decided_btn = ttk.Button(self, text="Decided", command=lambda: controller.show_frame(decidedPage))
        decided_btn.pack(pady=10)
        undecided_btn = ttk.Button(self, text="Undecided", command=lambda: controller.show_frame(quizPage))
        undecided_btn.pack(pady=10)

class decidedPage(ttk.Frame):  # page for drop down selection
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Select your major from the dropdown!", font=("Consolas", 14))
        label.pack(pady=25)

        # major dropbox
        majors = [
            "Business", "Engineering", "Computer Science", "Performing Arts",
            "Visual Arts", "Health Science", "Biology", "Psychology",
            "Music", "Economics"
        ]
        self.selectedMajor = tk.StringVar()
        major_dropdown = ttk.Combobox(self, textvariable=self.selectedMajor, values=majors, state="readonly")
        major_dropdown.pack(pady=10)

        # button
        submit_btn = ttk.Button(self, text="Submit", command=self.show_major)
        submit_btn.pack(pady=10)
        home_btn = ttk.Button(self, text="Home", command=lambda: controller.show_frame(homePage))
        home_btn.pack(pady=10)

    # show major when selected
    def show_major(self):
        if not self.selectedMajor.get():
            messagebox.showwarning("No selection", "Please select a major.")
        else:
            info_page = self.controller.frames[majorInfoPage]
            info_page.show_major_info(self.selectedMajor.get())
class quizPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.answers = []
        self.current_question = 0
        self.score = {"STEM": 0, "Arts": 0, "Business": 0}

        # questions
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

        self.question_label = tk.Label(self, text="", font=("Arial", 14), wraplength=500)
        self.question_label.pack(pady=30)
        self.answer_var = tk.StringVar()
        self.options = ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]

        self.radio_buttons = []
        for option in self.options:
            rb = ttk.Radiobutton(self, text=option, variable=self.answer_var, value=option)
            rb.pack(anchor="w", padx=60, pady=2)
            self.radio_buttons.append(rb)

        # progressing questions
        self.next_btn = tk.Button(self, text="Next question", command=self.next_question)
        self.next_btn.pack(pady=20)
        self.back_btn = tk.Button(self, text="Home", command=lambda: controller.show_frame(homePage))
        self.back_btn.pack(pady=20)

        self.load_question()

    def load_question(self):
        q_text = self.questions[self.current_question]
        self.question_label.config(
            text=f"Question {self.current_question + 1} of {len(self.questions)}:\n\n{q_text}"
        )
        self.answer_var.set("")

        if self.current_question == len(self.questions) -1:
            self.next_btn.config(text = "Submit!")
        else:
            self.next_btn.config(text = "Next Question")

    def next_question(self):
        answer = self.answer_var.get().strip()
        if answer == "":
            messagebox.showwarning("No selection", "Please select an answer.")
            return

        self.answers.append(answer)
        self.current_question += 1

        if self.current_question >= len(self.questions):
            result_page = self.controller.frames[resultPage]
            result_page.set_result(self.answers)
            self.controller.show_frame(resultPage)
        else:
            self.load_question()
    
    def reset_quiz(self): #reset the quiz
        self.answers.clear()
        self.current_question = 0
        self.answer_var.set("")

        self.load_question()

class resultPage(ttk.Frame):  # quiz result page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.result_label = ttk.Label(self, text="", font=("Arial", 16))
        self.result_label.pack(pady=50)

        # button
        home_btn = ttk.Button(self, text="Home", command = self.reset_and_home)
        home_btn.pack(pady=20)

        retake_btn = ttk.Button(self, text = "Retake quiz", command = self.retake_quiz)
        retake_btn.pack(pady = 5)

    def set_result(self, answers):
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

        for i, ans in enumerate(answers):
            value = value_map.get(ans, 0)
            for major in q_map[i]:
                scores[major] += value

        recommended = max(scores, key=scores.get)
        result_text = f"Recommended Major: {recommended}\n\nScores:\n"
        for major, score in scores.items():
            result_text += f"  • {major}: {score}\n"
        self.result_label.config(text=result_text)
    
    def retake_quiz(self):
        quiz_page = self.controller.frames[quizPage]
        quiz_page.reset_quiz()
        self.controller.show_frame(quizPage)
    
    def reset_and_home(self):
        quiz_page = self.controller.frames[quizPage]
        quiz_page.reset_quiz()

        self.controller.show_frame(homePage)

class majorInfoPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ttk.Label(self, text = "", font = ("Arial", 14), wraplength = 500)
        self.label.pack(pady = 20)

        self.home_btn = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(homePage))
        self.home_btn.pack(pady = 10)

    def show_major_info(self, major_name): #showing description of major 
        description = major_descriptions.get(major_name, "No description available.")
        self.label.configure(text = f"{major_name}\n\n{description}")
        self.tkraise()

class aboutPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text = "Major pick, your career deciding assistant!", font = ("Helvetica", 16, "bold"))
        label.pack(pady = 40)
        label = ttk.Label(self, text = """This is major pick, an application that helps students decide their major, provide descriptions 
and job examples of the major, and provides general information like tuition cost and other important information
at George Mason University.""", font = ("Helvetica", 14), wraplength = 500)
        label.pack(pady = 60)

        home_btn = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(homePage))
        home_btn.pack(pady = 80)

if __name__ == "__main__":  # mainloop
    app = majorApp()
    app.mainloop()
