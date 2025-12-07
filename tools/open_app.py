# open_app.py - Clean utility to open Windows apps

import os
import subprocess
import winreg
import pyautogui
from tools.search_web import search_and_open

# -----------------------------
# Registry-based installed apps
# -----------------------------
def get_installed_apps():
    app_map = {}
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]
    for root, path in reg_paths:
        try:
            reg_key = winreg.OpenKey(root, path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(reg_key, i)
                    subkey = winreg.OpenKey(reg_key, subkey_name)
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    values = [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])]
                    icon = winreg.QueryValueEx(subkey, "DisplayIcon")[0] if "DisplayIcon" in values else ""
                    app_map[name.lower()] = icon.strip('"')
                except Exception:
                    continue
        except Exception:
            continue
    return app_map

# -----------------------------
# Open app by name
# -----------------------------
def open_app_fun(app_name):
    app_name = app_name.lower().strip()
    apps = get_installed_apps()

    # Try registry-installed apps
    for name, path in apps.items():
        if app_name in name and path:
            try:
                exe_path = path.split(',')[0].strip('"')
                if not exe_path.lower().endswith('.exe'):
                    return f"⚠️ Found '{name}', but not an executable: {exe_path}"
                subprocess.Popen([exe_path])
                return f"✅ Opened '{name}' from registry ({exe_path})"
            except Exception as e:
                return f"❌ Failed to open '{name}': {e}"

    # Fallback: system apps and popular custom apps
    system_apps = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'wordpad': 'write.exe',
        'explorer': 'explorer.exe',
        'cmd': 'cmd.exe',
        'powershell': 'powershell.exe',
        'task manager': 'taskmgr.exe',
        'control panel': 'control.exe',
        'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        'vs code': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
        'visual studio code': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
    }
    uwp_apps = {'whatsapp': '5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App'}

    for key, exe in system_apps.items():
        if app_name in key:
            try:
                exe_path = os.path.expandvars(exe)
                subprocess.Popen([exe_path])
                return f"✅ Opened system/custom app '{key}' ({exe_path})"
            except Exception as e:
                return f"❌ Failed system/custom app '{key}': {e}"

    for key, app_id in uwp_apps.items():
        if app_name in key:
            try:
                subprocess.Popen(['explorer.exe', f'shell:appsFolder\\{app_id}'])
                return f"✅ Opened UWP app '{key}'"
            except Exception as e:
                return f"❌ Failed UWP app '{key}': {e}"

    # Fallback: web search
    search_and_open(f"search for {app_name}.com", 1)
    return f"⚠️ App '{app_name}' not found locally; performed web search."

# -----------------------------
# Switch between windows/tabs
# -----------------------------
def switch_tab_fun(direction='next'):
    try:
        pyautogui.keyDown('alt')
        if direction == 'next':
            pyautogui.press('tab')
        elif direction == 'prev':
            pyautogui.keyDown('shift')
            pyautogui.press('tab')
            pyautogui.keyUp('shift')
        else:
            return "⚠️ Unknown direction. Use 'next' or 'prev'."
        pyautogui.keyUp('alt')
        return f"✅ Switched to {direction} tab/window."
    except Exception as e:
        return f"❌ Failed to switch tab: {e}"
