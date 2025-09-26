import os
import subprocess
import platform

def open_notepad():
    """Open Notepad application"""
    if platform.system() == 'Windows':
        os.system('start notepad')
        return "Opening Notepad"
    else:
        return "Notepad is only available on Windows"

def open_discord():
    """Open Discord application"""
    if platform.system() == 'Windows':
        try:
            # Try different possible paths
            discord_paths = [
                os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'app-1.0.9003', 'Discord.exe'), 
                os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Update.exe'),
                os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Discord.exe')
            ]
            
            for path in discord_paths:
                if os.path.exists(path):
                    os.startfile(path)
                    return "Opening Discord"
            
            # If no path exists, try to open Discord using the start command
            os.system('start discord:')
            return "Attempting to open Discord"
        except Exception as e:
            return f"Error opening Discord: {str(e)}"
    else:
        return "Discord automatic opening is only configured for Windows"

def open_cmd():
    """Open Command Prompt"""
    if platform.system() == 'Windows':
        os.system('start cmd')
        return "Opening Command Prompt"
    else:
        os.system('gnome-terminal')
        return "Opening Terminal"

def open_camera():
    """Open Camera application"""
    if platform.system() == 'Windows':
        # Try to open the camera app on Windows
        try:
            os.system('start microsoft.windows.camera:')
            return "Opening Camera"
        except Exception:
            return "Could not open camera"
    else:
        return "Camera app is only configured for Windows"

def open_calculator():
    """Open Calculator application"""
    if platform.system() == 'Windows':
        os.system('start calc')
        return "Opening Calculator"
    else:
        os.system('gnome-calculator')
        return "Opening Calculator" 