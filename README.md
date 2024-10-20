# assistpy README

## Overview
`assistpy` is a Python-based utility designed to automate task management and provide an interactive assistant window with hotkey controls. The program monitors workstation lock status, automatically launching and terminating a custom assistant window based on user activity. It features a lightweight GUI with command execution capabilities, controlled via keyboard shortcuts.

This script comes with an integrated tray icon and can be extended with user-defined Python functions via an `extension.py` file. The program also logs executed commands and offers optional desktop notifications.

## Key Features
- **Hotkey-Controlled Window:** Open the assistant window by pressing `Ctrl + .` and close it with `Ctrl + Alt + .`.
- **Customizable Commands:** You can extend the functionality by specifying custom commands in an `extension.py` file.
- **Automatic Process Monitoring:** The program monitors workstation lock status and starts/stops based on whether the user is active.
- **Notifications and Logging:** Notifications and logs help you track executed commands and any errors.
- **Cross-process Management:** The program spawns subprocesses for the GUI and tray icon.

## Dependencies
- Python 3.x (Version 3.13 or lower)
- External packages:
  - `AIP` (A library that helps install required packages for the program)
  - `Tkinter` (for the GUI)
  - `keyboard` (for hotkey management)
  - `multiprocessing` (for managing background processes)
  - `psutil` (for process monitoring)
  - `plyer` (for desktop notifications)
  - `pystray` (for tray icon)
  - `PIL` (for image handling in the tray icon)

## How to Run
The program is distributed as an `.exe` file, which can be executed with two modes:

1. **Console Mode:**  
   If you want the program to open with a console, run the `.exe` file with the `console` argument.  
   Example:
   ```
   assistpy.exe console
   ```

2. **Non-Console Mode:**  
   If you run the `.exe` file without any arguments, it will open without a console, running silently in the background.  
   Example:
   ```
   assistpy.exe
   ```

## Extensions
The program can integrate custom functions defined in an `extension.py` file. If the file is not found locally, the program will request a file path from the user.

## assistpy-handler.py
The program relies on an additional script named `assistpy-handler.py` for launching itself and managing other features.

## Installation
`assistpy` uses a built-in library called `AIP`, which is responsible for installing the required dependencies. This allows for smooth package management without manual intervention.

## Additional Notes
- The log file is stored as `assistpy.log` in the current directory, where all command executions and errors are recorded.
- The dump file for the `extension.py` path is located in the system's temporary folder.

