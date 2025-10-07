

import tkinter as tk
from tkinter import ttk, messagebox

class majorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Major Pick")
        self.geometry("600x400")

        #container
        container = ttk.Frame(self)
        container.pack(fill = "both", expand = True)
        container.rowconfigure(0, weight = 1)
        container.columnconfigure(0, weight = 1)

        #pages holders
        self.frames = {}
        for F in(homePage, decidedPage, quizPage, resultPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(homePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class homePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text = "Welcome student! Are you currently decided or undecided?", font = ("Consolas", 16))
        label.pack(pady = 40)

        #buttons
        decided_btn = ttk.Button(self, text = "Decided", command = lambda: controller.show_frame(decidedPage))
        decided_btn.pack(pady = 10)
        undecided_btn = ttk.Button(self, text = "Undecided", command = lambda: controller.show_frame(quizPage))
        undecided_btn.pack(pady = 10)


class decidedPage(ttk.Frame): #page for drop down selection 
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text = "Select your major from the dropdown!", font = ("Consolas", 14))
        label.pack(pady = 25)

        #major dropbox 
        majors = ["Business", "Engineering", "Computer science", "Performing Arts", "Visual Arts", "Health Science", "Biology", "Pyschology", "Music", "Economics"]
        self.selectedMajor = tk.StringVar()
        major_dropdown = ttk.Combobox(self, textvariable = self.selectedMajor, values = majors, state = "readonly")
        major_dropdown.pack(pady = 10)
                            
        #button
        submit_btn = ttk.Button(self, text = "Submit", command = self.show_major)
        submit_btn.pack(pady = 10)
        home_btn = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(homePage))
        home_btn.pack(pady = 10)

        #show major when selected
        def show_major(self):
            if not self.selectedMajor.get():
                messagebox.showwarning("No selection, please select a major.")
            else:
                messagebox.showinfo(f"Major selected!\n You selected: {self.selectedMajor.get()}")

class quizPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.question_index = 0
        self.score = {}

class resultPage(ttk.Frame): #quiz result page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.result_label = ttk.Label(self, text = "", font = ("Arial", 16))
        self.result_label.pack(pady = 50)

        #button
        home_btn = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(homePage))
        home_btn.pack(pady = 20)

        def set_result(self, score):
            recommended = max(score, key = score.get)
            self.result_label.config(text = f"Recommended Major: {recommended}")




if __name__ == "__main__": #mainloop 
    app = majorApp()
    app.mainloop()
