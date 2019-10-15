import subprocess, os
from enum import Enum

class GnomeNotificationTypes(Enum):
    CRITICAL="critical"
    NORMAL="normal"
    LOW="low"

def notify(type, title, message):
    userID = subprocess.run(['id', '-u', os.environ['SUDO_USER']],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True).stdout.decode("utf-8").replace('\n', '')
    subprocess.run(['sudo', '-u', os.environ['SUDO_USER'], 'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{}/bus'.format(userID), 
                    'notify-send', '-u', type, '-t', '5000', '-i', 'nm-device-wireless', title, message],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True)