
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

Helps students who are undecided and looking to pursue secondary education on what major is best fit for them. Provides detailed results based off a quiz with
selected questions to provide the student with a recommended major. Detailed information and examples of jobs for each major will be provided, as well as
information about the major from GMU such as cost of tuition range, credits expected, different classes and content expected.

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
        home_label = ttk.Label(self, text="Welcome student! Are you currently decided or undecided?", font=("Consolas", 16))
        home_label.pack(pady=40)

        # buttons
        decided_btn = ttk.Button(self, text="Decided", command=lambda: controller.show_frame(decidedPage))
        decided_btn.pack(pady=10)
        undecided_btn = ttk.Button(self, text="Undecided", command=lambda: controller.show_frame(quizPage))
        undecided_btn.pack(pady=10)

class decidedPage(ttk.Frame): # page for drop down selection

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        decided_label = ttk.Label(self, text="Select your major from the dropdown!", font=("Consolas", 14))
        decided_label.pack(pady=25)

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
        self.next_btn = tk.Button(self, text="Next question", font = ("Consolas"), command=self.next_question)
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
            self.next_btn.config(text = "Submit!", font = ("Consolas"))
        else:
            self.next_btn.config(text = "Next Question", font = ("Consolas"))

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
        """Resets quiz state so the student can retake it.

        :returns: None
        :tests:
        >>> app = majorApp()
        >>> quiz_page = app.frames[quizPage]
        >>> quiz_page.answers = ["Agree"]
        >>> quiz_page.current_question = 5
        >>> quiz_page.reset_quiz()
        >>> (quiz_page.answers == [], quiz_page.current_question == 0)
        (True, True)
        """

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
        """Sets and displays the recommended major based on quiz answers.

        :param answers: List of answer strings ("Strongly agree", "Agree", etc.)
        :type answers: list[str]

        :returns: None, updates label text in the result page

        :tests:
        >>> app = majorApp()
        >>> result_page = app.frames[resultPage]
        >>> answers = ["Strongly agree"] * 10
        >>> result_page.set_result(answers)
        >>> "Recommended Major:" in result_page.result_label.cget("text")
        True
        """

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
        """Displays information about the selected major.

        :param major_name: Name of the major
        :type major_name: str

        :returns: None, updates label text with the description.

        :tests:
        >>> app = majorApp()
        >>> info_page = app.frames[majorInfoPage]
        >>> info_page.show_major_info("Business")
        >>> "Business" in info_page.label.cget("text")
        True
        """
        
        description = major_descriptions.get(major_name, "No description available.")
        self.label.configure(text = f"{major_name}\n\n{description}", font = ("Consolas", 14))
        self.tkraise()

class aboutPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        about_title_label = ttk.Label(self, text = "Major pick, your career deciding assistant!", font = ("Consolas", 16, "bold"))
        about_title_label.pack(pady = 40)
        about_desc_label = ttk.Label(self, text = """This is major pick, an application that helps students decide their major, provide descriptions 
and job examples of the major, and provides general information like tuition cost and other important information
at George Mason University.""", font = ("Consolas", 14), wraplength = 500)
        about_desc_label.pack(pady = 60)

        home_btn = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(homePage))
        home_btn.pack(pady = 80)

if __name__ == "__main__":  # mainloop
    
    """
    **TEST DECLARATIONS*
    Remove '#' to run doctest from tests in a few functions. 
    """
    #import doctest
    #doctest.testmod(verbose = True)

    app = majorApp()
    app.mainloop()
