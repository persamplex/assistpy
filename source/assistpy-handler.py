import os
import subprocess
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_user_preference():
    # بررسی آرگومان‌های خط فرمان
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['console', 'silent']:
        return sys.argv[1].lower() == 'console'
    
    # پیش‌فرض: silent
    return False

def find_and_run_script(filename, window=False):
    base_path = sys._MEIPASS
    for dirpath, dirnames, filenames in os.walk(base_path):
        if filename in filenames:
            script_path = os.path.join(base_path, filename)
            try:
                if window:
                    subprocess.run(['python', script_path])
                    print(f'{script_path} started')
                else:
                    subprocess.run(['python', script_path], creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f'{script_path} started in silent mode')

            except WindowsError as e:
                print(f"Error: {e}")
                if str(e) == "[WinError 2] The system cannot find the file specified":
                    message = f"Error on startup: Python not found! Please install Python or check your Python installation path.To ensure that the 'assistpy' script works correctly, you should be able to execute Python commands using the 'python' command in the command prompt.This program requires Python to run Python commands."

                else:
                    message = f"Error: {e}"
                command = f'echo {message} & pause'
                subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd.exe', '/k', command])
            return

if __name__ == '__main__':
    run_with_console = get_user_preference()
    find_and_run_script('assistpy-tk.py', window=run_with_console)
