# SYST-230 Project

A web application to assist college students in exploring and selecting majors, including resources for both undecided and decided students.

## Features

- Browse majors and view example career paths
- Select your major and see related job opportunities
- In-progress: Improved formatting and integration with a C-based web server

## Prerequisites

- Python 3.x
- Flask web framework

## Installation

1. Install Flask:
    ```bash
    pip install flask
    ```
2. If you encounter a "directory not in PATH" error, copy the directory, add it to your system PATH, then restart your terminal and code editor.

## Usage

1. Open a command terminal.
2. Navigate to the `flask_app` directory:
    ```bash
    cd flask_app
    ```
3. Start the app python code, also boots C server:
    ```bash
    python3 app.py
    ```
4. If successful, you should see:
    ```
    *Running on http://127.0.0.1:5000
    C server launching...
    C server successfully booted. 
        *Debugger is active!
    ```
5. Open your browser and go to [127.0.0.1:2728]
    ```
    2728 is the port that the C server runs on and handles the static pages, right now it runs the home page.
    5000 is the port that flask uses, which runs dynamic pages such as the quiz and decided page. 

## Notes

- `127.0.0.1` is a loopback address; the server runs locally on your computer.
- Any computer with Python and Flask installed can run this application.

---

George Mason University  
Updated: 9/30/2025
Author(s): 
    *Nathaniel Crick
