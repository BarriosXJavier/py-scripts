import subprocess
import platform

def check_status() -> bool:
    """
    Check if system is running on battery.

    Returns:
        bool: True if running on battery, False otherwise.
    """

    try:
        status = subprocess.check_output(["upower", "-i", "/org/freedesktop/Upower/devices/battery_BAT0"],
        universal_newlines=True,
        )
        return "state: discharging" in status.lower()
    except subprocess.CalledProcessError as e:
        print(f"Error checking power status: {e}")
        return False

def set_mode(mode: str) -> None:
    """
    Set power mode (Ubuntu)

    Args:
        mode(str): The desired power mode
    """
    try:
        if platform.system() == "Linux":
            subprocess.run(
                    ["gsettings", "set", "org.gnome.settings-daemon.plugins.power", "profile", mode],
                    check=True,
            )
            print(f"Power mode set to '{mode}")
        else:
            print("Your operating system is not supported")
    except subprocess.CalledProcessError as e:
        print(f"Error setting power mode: {e}")

if __name__ == "__main__":
    if check_status():
        set_mode("balanced")
    else:
        print("PC is plugged in. No action needed.")
