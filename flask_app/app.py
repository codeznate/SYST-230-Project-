import subprocess 
import os
import signal

from flask import Flask
from Routes.quiz import quiz_bp
from Routes.majorSelect import majorSelect_bp 

C_SERVER_PATH = os.path.abspath("../CServer/server") #path to c compile

c_server_process = None #close it later
def start_c_server():
    global c_server_process 
    if not os.path.exists(C_SERVER_PATH):
        print(f"Error: C server executable not found.")
        return
    print("C server launching...")
    try:
        c_server_process = subprocess.Popen([C_SERVER_PATH], cwd=os.path.dirname(C_SERVER_PATH),  
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("C server successfully booted.")
    except Exception:
        print(f"Failed to start server {Exception}")

def stop_c_server():
    global c_server_process
    if c_server_process and c_server_process.poll() is None:
        print("Stopping C server...")
        c_server_process.send_signal(signal.SIGINT)
        c_server_process.wait()
        print("C server stopped.")


def create_app():  #create flask app
    app = Flask(__name__)
    app.register_blueprint(quiz_bp, url_prefix="/quiz")  #blueprint for quiz page
    app.register_blueprint(majorSelect_bp, url_prefix="/decided") #blueprint for decided page 
    return app

if __name__ == "__main__":   #running file directly 
    start_c_server()
    app = create_app()
    
    try:
        app.run(debug = True, port= 5000)
    finally:
        stop_c_server()



