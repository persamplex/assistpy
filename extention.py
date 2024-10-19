import random
import time 
import keyboard
import pyautogui
import pyttsx3
import pyperclip
import secrets
import string
import jdatetime
import datetime
import pytz
from plyer import notification


# Important: This code should be executed using the `exec` command in Python as part of your main program. 



def show_log(enable=True):
    global config
    config['showNotification'] = enable

def save_log(enable=True):
    global config
    config['writeLogFile'] = enable
    if enable is True:
        notification.notify(
            title="save_log notification",
            message=f'saving log on = {os.path.join(os.getcwd(), 'assistpy.log')}',
            timeout=5
        )

def copy_to_clipboard(text):
    pyperclip.copy(text)

def text_to_speach(text='okey',rate=-50,is_girl=True):
    engine = pyttsx3.init()
    ratee = engine.getProperty('rate')
    engine.setProperty('rate', ratee+rate)

    voices = engine.getProperty('voices')
    if is_girl:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def generate_password(length=12):
    characters = string.ascii_letters + string.digits 
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    copy_to_clipboard(password)


def show_date(time_zone='Asia/Tehran'):
    try:
        tz = pytz.timezone(time_zone)
    except pytz.UnknownTimeZoneError:
        notification.notify(
            title="404",
            message=f'Time zone "{time_zone}" not found',
            timeout=5
        )
        return
    
    current_time = datetime.datetime.now(tz)
    
    if time_zone in ['Asia/Tehran', 'Iran']:
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=current_time)
        formatted_date_time = shamsi_date.strftime("%Y/%m/%d %H:%M")
        calendar_type = 'Shamsi'
    else:
        formatted_date_time = current_time.strftime("%Y/%m/%d %H:%M")
        calendar_type = 'Gregorian'
    
    notification.notify(
        title=f"Date",
        message=f'{formatted_date_time} for {time_zone}',
        timeout=5
    )
    copy_to_clipboard(formatted_date_time)
    


def generate_tag(length=6):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    
    name = random.choice(consonants) if random.random() > 0.5 else random.choice(vowels)
    
    for i in range(length - 1):
        if name[-1] in vowels:
            name += random.choice(consonants)
        else:
            name += random.choice(vowels)
    
    copy_to_clipboard('#' + name.capitalize())

def generate_number():
    copy_to_clipboard(random.randint(10000,99999))

def generate_port():
    copy_to_clipboard(random.randint(49152,65535))


def type_like_human(command=None, speed=0.1):
    if command == None:
        command = pyperclip.paste()
    """
    Types the given text like a human with a specified typing speed using the keyboard.

    Args:
        text (str): The text to be typed.
        speed (float): The delay between typing each character.
    """
    text = rf'{command}'
    time.sleep(0.5)
    for char in text:
        # Check if Ctrl+C is pressed to stop the program
        if keyboard.is_pressed('ctrl+c'):
            print("\nProgram interrupted by user. Exiting...")
            return
        pyautogui.typewrite(char)
        time.sleep(speed)

def netplan(speed=0.04):
    text = f'''
network:
    version: 2
    renderer: networkd
    ethernets:
        enp1s0:
            addresses:
                - 192.168.43.254/24
            nameservers:
                addresses: [1.1.1.1, 8.8.8.8]
            routes:
                - to: default
                  via: 192.168.43.1

'''
    type_like_human(command=text,typing_speed=float(speed))



def printes(text='this is test'):
    print(text)
    