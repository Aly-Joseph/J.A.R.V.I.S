import os

def shutdown():
    os.system("shutdown /s /t 0")

def restart():
    os.system("shutdown /r /t 0")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def open_app(app):
    if app == "calc": os.system("calc")
    if app == "notepad": os.system("notepad")
    if app == "chrome": os.system("start chrome")
