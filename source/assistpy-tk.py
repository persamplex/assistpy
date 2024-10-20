import sys

if sys.version_info >= (3, 13):
    print("This script requires Python version lower than 3.13.")
    sys.exit(1)

import AIP
import tkinter as tk
from tkinter import filedialog,messagebox
import os,sys
import keyboard
import threading
import time
import logging
from multiprocessing import Process, Queue
import psutil
from plyer import notification
import tempfile

import pystray
from PIL import Image
from pystray import MenuItem, Menu

config = {
    'showNotification': False,
    'writeLogFile': True
}

logging.basicConfig(filename="assistpy.log", level=logging.INFO, format='%(asctime)s - %(message)s')

DUMP_FILE_PATH = os.path.join(tempfile.gettempdir(), "extension_path_dump.txt")


def find_or_request_extension_file():
    """Check if extention.py exists in the current directory or in the dump file, otherwise ask the user to select the file."""
    
    if os.path.exists("extention.py"):
        print(os.path.abspath("extention.py"))
        print('on local found ')
        return "extention.py"
    
    if os.path.exists(DUMP_FILE_PATH):
        with open(DUMP_FILE_PATH, 'r') as dump_file:
            saved_path = dump_file.read().strip()
            if os.path.exists(saved_path):
                print('on dump found ')
                return saved_path

            
    
    print("File 'extention.py' not found. Please select the file.")
    
    root = tk.Tk()
    root.withdraw() 
    root.title("Select Extension File") 

    messagebox.showinfo("Do You Have Extensions?", "If you want to add your custom functions, please select your 'extension.py' file.")

    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    
    if not file_path:
        print("No file selected. Continuing without it...")
        return None 

    with open(DUMP_FILE_PATH, 'w') as dump_file:
        dump_file.write(file_path)
    
    return file_path

def try_open_extension_file(file_path):
    """Try to open the extension file. If it fails, request a new file path."""
    try:
        with open(file_path, 'r') as file:
            exec(file.read())
    except (FileNotFoundError, IOError) as e:
        print(f"Error opening file '{file_path}': {e}")


extension_file_path = find_or_request_extension_file()
try:
    with open(extension_file_path, 'r') as file:
        exec(file.read())
except (FileNotFoundError, IOError) as e:
    print(f"Error opening file '{extension_file_path}': {e}")



class AssistApp:
    def __init__(self, queue):
        self.queue = queue
        self.root = tk.Tk()
        self.root.withdraw()
        self.assist_window = None

        threading.Thread(target=self.ctrl_dot_listener, daemon=True).start()
        threading.Thread(target=self.ctrl_alt_dot_listener, daemon=True).start()

    def ctrl_dot_listener(self):
        keyboard.add_hotkey('ctrl+.', self.toggle_assist_window)
    
    def ctrl_alt_dot_listener(self):
        keyboard.add_hotkey('ctrl+alt+.', lambda: self.queue.put('exit_app'))

    def toggle_assist_window(self):
        if self.assist_window and self.assist_window.winfo_exists():  # Check if the window exists
            self.assist_window.deiconify()
            self.assist_window.lift()
        else:
            x, y = self.root.winfo_pointerxy()
            self.create_assist_window(x, y)

    def create_assist_window(self, x, y):
        self.assist_window = tk.Toplevel(self.root)
        self.assist_window.attributes('-alpha', 0.8)
        self.assist_window.attributes('-topmost', True)
        self.assist_window.overrideredirect(True)
        self.assist_window.focus_force()

        self.entry = tk.Entry(self.assist_window, highlightthickness=0, bd=0, bg=None)
        self.entry.pack(padx=0, pady=0)

        self.entry.bind('<Return>', self.handle_return_pressed)
        self.assist_window.bind('<Escape>', self.on_closing)
        self.entry.bind('<Tab>', self.handle_tab_press)
        self.entry.bind('<BackSpace>', self.handle_backspace_press)

        self.assist_window.geometry(f"{self.entry.winfo_reqwidth()}x{self.entry.winfo_reqheight()}+{x + 10}+{y + 10}")
        self.entry.focus_set()
    
    def handle_backspace_press(self, event):
        self.entry.config(fg="black")

    def handle_tab_press(self, event):
        current_text = self.entry.get()
        function_names = [name for name in globals() if callable(globals()[name])]
        self.suggestions = [name for name in function_names if name.startswith(current_text)]

        if self.suggestions:
            if len(self.suggestions) == 1:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.suggestions[0])
            else:
                self.update_completion_text()

        return 'break'

    def update_completion_text(self):
        common_prefix = self.find_longest_common_prefix(self.suggestions)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, common_prefix)
        self.entry.icursor(len(common_prefix))

    def find_longest_common_prefix(self, strings):
        if not strings:
            return ""
        prefix = strings[0]
        for string in strings[1:]:
            while not string.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

    def handle_return_pressed(self, event):
        command = self.entry.get()
        
        try:
            self.entry.config(bg="white")

            self.assist_window.withdraw()  # Option to hide the window instead of destroying
            
            result = eval(command)
            if callable(result):
                result()
                self.notify_and_log(f"{command} executed with no arguments", result)
            else:
                self.notify_and_log(f"{command} executed with result", result)
            self.assist_window.destroy()

        except Exception as e:
            self.entry.config(fg="red")
            self.assist_window.deiconify()  # Show the window again if there's an error
            self.notify_and_log(f"Error executing '{command}': {e}", is_error=True)
        
    def notify_and_log(self, message, result=None, is_error=False):
        title = "Command Executed" if not is_error else "Execution Error"
        if config['showNotification']:
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
        if config['writeLogFile']:
            if is_error:
                logging.error(message)
            else:
                logging.info(message)
            
    def on_closing(self, event=None):
        if self.assist_window:
            self.assist_window.destroy()
            self.assist_window = None

    def run(self):
        self.root.mainloop()


def is_workstation_locked():
    """Check if the workstation is locked by looking for LogonUI.exe process."""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'LogonUI.exe':
                return True
        return False
    except Exception as e:
        print(f'Error on is_workstation_locked: {e}')

def icon_run(queue):
    menu = Menu(
        MenuItem('Reload', lambda _: queue.put('reload_app')),
        MenuItem('Exit', lambda _: queue.put('exit_app'))
    )
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    image = Image.open(os.path.join(current_directory,'icon.ico'))
    icon = pystray.Icon("assistpy", image, "assistpy", menu)
    icon.run()



def launch_program(queue):
    """Launch the AssistApp."""
    app_process = Process(target=_app, args=(queue,))
    app_process.start()
    icon_process = Process(target=icon_run, args=(queue,))
    icon_process.start()

    return app_process.pid,icon_process.pid


def terminate_process(pid):
    """Terminate the process with the given PID."""
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait()
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} does not exist.")
    except psutil.AccessDenied:
        print(f"Access denied to terminate process with PID {pid}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def monitor_workstation(queue):
    """Monitor workstation lock state and manage the AssistApp process."""
    last_state = None
    app_pid = None
    icon_pid = None
    while True:
        if not queue.empty():
            msg = queue.get()
            if msg == 'exit_app':
                print('Exit requested, stopping program...')
                if app_pid and icon_pid:
                    terminate_process(app_pid)
                    terminate_process(icon_pid)
                break
            elif msg == 'reload_app':
                print('reload requested, stopping program...')
                terminate_process(app_pid)
                terminate_process(icon_pid)
                print('reload requested, starting program...')
                app_pid,icon_pid = launch_program(queue)
                

        current_state = is_workstation_locked()
        if current_state != last_state:
            if current_state:
                print('Stopping program...')
                if app_pid and icon_pid:
                    terminate_process(app_pid)
                    terminate_process(icon_pid)
                    app_pid = None
                    icon_pid = None
            else:
                print('Starting program...')
                app_pid,icon_pid = launch_program(queue)

        last_state = current_state
        time.sleep(1)


def _app(queue):
    assist_app = AssistApp(queue)
    assist_app.run()


if __name__ == "__main__":
    queue = Queue()
    monitor_workstation(queue)
