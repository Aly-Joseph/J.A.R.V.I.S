import psutil, platform, datetime

def get_system_info():
    return {
        "os": platform.system(),
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A",
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    }
