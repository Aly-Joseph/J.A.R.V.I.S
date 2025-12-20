from tools import *
from memory import *

def system_agent(task):
    if "shutdown" in task: shutdown()
    if "restart" in task: restart()
    if "sleep" in task: sleep()

def app_agent(task):
    if "calculator" in task: open_app("calc")
    if "notepad" in task: open_app("notepad")
    if "chrome" in task: open_app("chrome")

def memory_agent(task):
    if "my name is" in task:
        name = task.split("my name is")[-1].strip()
        remember("name", name)
        return f"I will remember your name, {name}."
