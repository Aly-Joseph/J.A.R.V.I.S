import win32gui
import win32con
import time


def minimize_console():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    time.sleep(0.5)


def focus_window_by_title(keyword: str, timeout=5):
    end = time.time() + timeout

    while time.time() < end:
        def enum_handler(hwnd, _):
            title = win32gui.GetWindowText(hwnd).lower()
            if keyword.lower() in title:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)

        win32gui.EnumWindows(enum_handler, None)
        time.sleep(0.3)
