import os, time
import sys
import subprocess
import shutil



def _is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        try:
            __import__(package_name.lower())
            return True
        except:
            try:
                result = subprocess.run([sys.executable, '-m','pip', 'show', '--quiet', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                return True
            except subprocess.CalledProcessError:
                return False

def _run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{e.stderr.strip()}")
        time.sleep(10)
    except Exception as e:
        print(e.stderr.strip())
        time.sleep(10)

        # pass

if __name__ == "__main__":
    if not _is_package_installed("colorama"):
        print(f'Try to install necessary libraries with pip\nmake sure you have access to the internet\n[AIP] colorama installing ')
        _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'colorama'])

    from colorama import Fore, Style
    for x in range(1, len(sys.argv)):
            if sys.argv[x] == '--install':
                command = [sys.executable, '-m', 'pip', 'show', 'pip']
                try:
                    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if result.returncode == 0:
                        location_line = next(line for line in result.stdout.split('\n') if line.startswith('Location:'))
                        pip_location = location_line.split(':', 1)[1].strip()
                    else:
                        print(f"Error: {result.stderr.strip()}")
                        exit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    exit()
                current_executable = sys.argv[0]
                program_name_with_extension = os.path.basename(current_executable)
                program_name = os.path.splitext(program_name_with_extension)[0]
                package_folder_path = os.path.join(pip_location, program_name)

                try:
                    os.makedirs(package_folder_path, exist_ok=True)
                    target_file_path = os.path.join(package_folder_path, '__init__.py')
                    if os.path.exists(target_file_path):
                        os.remove(target_file_path)
                    shutil.copy(current_executable, package_folder_path)
                    new_file_path = os.path.join(package_folder_path, '__init__.py')
                    os.rename(os.path.join(package_folder_path, os.path.basename(current_executable)), new_file_path)
                    print(f"\n\nThe script is installed in your local-packages {package_folder_path}\n"
                        f"Use: {Fore.CYAN}{Style.BRIGHT}import AIP{Style.RESET_ALL}\n"
                        f"\n{Fore.BLACK}\"Note: This script cannot be used outside your local environment\"{Style.RESET_ALL}")
                except Exception as e:
                    print(f"Error on installing package on local-package:\n{e}")


def install(package_name):
    if not _is_package_installed("colorama"):
        _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'colorama'])

    from colorama import Fore, Style
    if _is_package_installed(package_name) != True:
        print(f"{Fore.BLACK}[AIP]{Style.RESET_ALL} {package_name} installing ")
        if _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]) == None:
            print(f"{Fore.RED}[AIP]{Style.RESET_ALL} {package_name} not installed")
            exit()
        else:
            print(f"{Fore.GREEN}[AIP]{Style.RESET_ALL} {package_name} installed")


     


              
def __custom_exception_handler(exception_type, exception, traceback):
    if exception_type == ModuleNotFoundError:
        package_name = exception.name  
        install(package_name)
        code = subprocess.call([sys.executable, sys.argv[0]]) 
    else:
        sys.__excepthook__(exception_type, exception, traceback)

sys.excepthook = __custom_exception_handler
    