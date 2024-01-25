#!/usr/bin/python3

import platform
import subprocess
from datetime import datetime

def check_status() -> bool:
    try:
        with open("/sys/class/power_supply/BAT0/status", "r") as status_file:
            battery_status = status_file.read().strip().lower()
        print(f"{datetime.now()} - Battery Status: {battery_status}")
        return battery_status == "discharging"
    except FileNotFoundError as e:
        print(f"{datetime.now()} - Error checking power status: {e}")
        return False

def set_power_saving_mode() -> None:
    try:
        if platform.system() == "Linux":
            result = subprocess.run(
                ["sudo", "tlp", "start"],
                check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                print(f"{datetime.now()} - Power-saving mode activated.")
            else:
                print(f"{datetime.now()} - Failed to start TLP. Error: {result.stderr.decode('utf-8')}")
        else:
            print("Your operating system is not supported")
    except subprocess.CalledProcessError as e:
        print(f"{datetime.now()} - Error setting power-saving mode: {e}")
        print(f"{datetime.now()} - Command that failed: {e.cmd}")
        print(f"{datetime.now()} - Error output: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    log_file_path = "~/power-saver-log.txt"
    try:
        log_file_path = log_file_path.replace("~", "/home/barrios")  #Use your username
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{datetime.now()} - Script started\n")
            if check_status():
                set_power_saving_mode()
            else:
                log_file.write(f"{datetime.now()} - PC is plugged in. No action needed.\n")
            log_file.write(f"{datetime.now()} - Script completed successfully\n")
    except Exception as e:
        print(f"{datetime.now()} - Error: {e}")

