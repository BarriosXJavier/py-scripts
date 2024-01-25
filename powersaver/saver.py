#!/usr/bin/python3

import platform
import subprocess

def check_status() -> bool:
    try:
        with open("/sys/class/power_supply/BAT0/status", "r") as status_file:
            battery_status = status_file.read().strip().lower()
        print(f"Battery Status: {battery_status}")
        return battery_status == "discharging"
    except FileNotFoundError as e:
        print(f"Error checking power status: {e}")
        return False

def set_power_saving_mode() -> None:
    try:
        if platform.system() == "Linux":
            subprocess.run(
                ["sudo", "tlp", "start"],
                check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            print("Power-saving mode activated.")
        else:
            print("Your operating system is not supported")
    except subprocess.CalledProcessError as e:
        print(f"Error setting power-saving mode: {e}")
        print(f"Command that failed: {e.cmd}")
        print(f"Error output: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    if check_status():
        set_power_saving_mode()
    else:
        print("PC is plugged in. No action needed.")

