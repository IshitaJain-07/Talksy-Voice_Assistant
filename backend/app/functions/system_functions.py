import os
import subprocess
import psutil
import datetime
import pyautogui
import platform
import webbrowser

def open_application(app_name):
    """
    Open an application
    """
    app_name = app_name.lower()
    
    # Dictionary of common apps
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "control panel": "control.exe",
        "task manager": "taskmgr.exe",
        "file explorer": "explorer.exe",
    }
    
    try:
        if app_name in app_paths:
            os.startfile(app_paths[app_name])
            return f"Opening {app_name}"
        else:
            # Try to open directly if not in the dictionary
            os.startfile(app_name)
            return f"Attempting to open {app_name}"
    except Exception as e:
        return f"I couldn't open {app_name}: {str(e)}"

def close_application(app_name):
    """
    Close an application
    """
    app_name = app_name.lower()
    
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # Check if process name contains the app name
            if app_name in proc.info['name'].lower():
                pid = proc.info['pid']
                process = psutil.Process(pid)
                process.terminate()
                return f"Closed {app_name}"
        
        return f"Could not find {app_name} running"
    
    except Exception as e:
        return f"Error closing {app_name}: {str(e)}"

def take_screenshot():
    """
    Take a screenshot and save it to the desktop
    """
    try:
        # Get desktop path
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(desktop, f"screenshot_{timestamp}.png")
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        return f"Screenshot saved to {filepath}"
    
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

def get_system_info():
    """
    Get system information
    """
    try:
        system = platform.system()
        processor = platform.processor()
        version = platform.version()
        
        # Get memory information
        memory = psutil.virtual_memory()
        total_ram = round(memory.total / (1024 ** 3), 2)  # Convert to GB
        available_ram = round(memory.available / (1024 ** 3), 2)
        
        # Get disk information
        disk = psutil.disk_usage('/')
        total_disk = round(disk.total / (1024 ** 3), 2)
        free_disk = round(disk.free / (1024 ** 3), 2)
        
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        return (
            f"System: {system} {version}\n"
            f"Processor: {processor}\n"
            f"RAM: {available_ram}GB free of {total_ram}GB\n"
            f"Disk: {free_disk}GB free of {total_disk}GB\n"
            f"CPU Usage: {cpu_usage}%"
        )
    
    except Exception as e:
        return f"Error getting system information: {str(e)}"

def open_website(url):
    """
    Open a website in the default browser
    """
    try:
        # Add http prefix if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        webbrowser.open(url)
        return f"Opening {url}"
    
    except Exception as e:
        return f"Error opening website: {str(e)}"

def create_reminder(reminder_text, time_str=None):
    """
    Create a reminder (simplified version)
    """
    try:
        if time_str:
            return f"I'll remind you: '{reminder_text}' at {time_str}"
        else:
            return f"I've noted your reminder: '{reminder_text}'"
    except Exception as e:
        return f"Error creating reminder: {str(e)}" 