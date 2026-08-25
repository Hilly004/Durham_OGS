import time
import os
import sys

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from Hardware.Dome.Dome_Commands import AstroHavenDome
from Hardware.Connections.Dome_Connection import DomeConnection
from Utilities.Config import dome_host, dome_port

# =========================================================
# Setup
# =========================================================

connection = DomeConnection(
    dome_host=dome_host,
    dome_port=dome_port
)

dome = AstroHavenDome(connection)


# =========================================================
# Helpers
# =========================================================

def print_header(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f'Dome host: {dome_host}')
    print(f'Dome port: {dome_port}')

def run_command(name, command):
    """
    Run a dome command and display whether it succeeded.
    """

    print(f"\nRunning: {name}")

    try:
        result = command()

        print("Command completed successfully.")

        if result is not None:
            print(f"Response: {result}")

    except Exception as e:
        print(f"ERROR: {e}")


def read_value(name, command):
    """
    Read a value from the dome and display it.
    """

    try:
        value = command()
        print(f"{name:<35}: {value}")
        return value

    except Exception as e:
        print(f"{name:<35}: ERROR - {e}")
        return None


# =========================================================
# Connection
# =========================================================

def connect():
    print_header("CONNECT TO DOME")

    try:
        result = dome.connect()

        if result:
            print(
                f"Connected to dome at "
                f"{dome_host}:{dome_port}"
            )
        else:
            print("Connection failed.")

    except Exception as e:
        print(f"Connection error: {e}")


def disconnect():
    print_header("DISCONNECT DOME")

    try:
        dome.disconnect()
        print("Disconnected.")

    except Exception as e:
        print(f"Disconnect error: {e}")


# =========================================================
# Status
# =========================================================

def show_status():

    print_header("DOME STATUS")

    if not dome.is_connected():
        print("Dome is not connected.")
        return

    print("\nGeneral status")
    print("-" * 60)

    read_value(
        "All open",
        dome.all_open
    )

    read_value(
        "All closed",
        dome.all_closed
    )

    read_value(
        "Open all indicator",
        dome.open_all_indicator
    )

    read_value(
        "Close all indicator",
        dome.close_all_indicator
    )

    read_value(
        "Either motor running",
        dome.either_motor_running
    )

    read_value(
        "Both motors running",
        dome.both_motors_running
    )

    read_value(
        "Auto close enabled",
        dome.auto_close_enabled
    )

    read_value(
        "Fault",
        dome.fault
    )


    print("\nLeft shutter")
    print("-" * 60)

    read_value(
        "Left open",
        dome.left_open
    )

    read_value(
        "Left closed",
        dome.left_closed
    )

    read_value(
        "Left up limit",
        dome.left_up_limit
    )

    read_value(
        "Left down limit",
        dome.left_down_limit
    )

    read_value(
        "Left forward running",
        dome.left_forward_running
    )

    read_value(
        "Left reverse running",
        dome.left_reverse_running
    )

    read_value(
        "Left jog up indicator",
        dome.left_jog_up_indicator
    )

    read_value(
        "Left jog down indicator",
        dome.left_jog_down_indicator
    )


    print("\nRight shutter")
    print("-" * 60)

    read_value(
        "Right open",
        dome.right_open
    )

    read_value(
        "Right closed",
        dome.right_closed
    )

    read_value(
        "Right up limit",
        dome.right_up_limit
    )

    read_value(
        "Right down limit",
        dome.right_down_limit
    )

    read_value(
        "Right forward running",
        dome.right_forward_running
    )

    read_value(
        "Right reverse running",
        dome.right_reverse_running
    )

    read_value(
        "Right jog up indicator",
        dome.right_jog_up_indicator
    )

    read_value(
        "Right jog down indicator",
        dome.right_jog_down_indicator
    )


    print("\nRegisters")
    print("-" * 60)

    read_value(
        "Left shutter angle",
        dome.get_left_angle
    )

    read_value(
        "Right shutter angle",
        dome.get_right_angle
    )

    read_value(
        "Aperture",
        dome.get_aperture
    )

    read_value(
        "Shutter width",
        dome.get_shutter_width
    )

    read_value(
        "Full travel time",
        dome.get_full_travel_time
    )

    read_value(
        "Full travel",
        dome.get_full_travel
    )


# =========================================================
# Jog Testing
# =========================================================

def jog_test(name, jog_function):

    print_header(f"JOG TEST: {name}")

    if not dome.is_connected():
        print("Dome is not connected.")
        return

    print(
        "The shutter will jog while this test is active."
    )

    try:
        duration = float(
            input(
                "Jog duration in seconds "
                "(recommended 0.5-2.0): "
            )
        )

    except ValueError:
        print("Invalid duration.")
        return

    if duration <= 0:
        print("Duration must be greater than zero.")
        return

    if duration > 5:
        print(
            "For safety, this test limits jogs "
            "to 5 seconds."
        )
        duration = 5

    confirm = input(
        f"Jog {name} for {duration:.1f} seconds? "
        "[y/N]: "
    )

    if confirm.lower() != "y":
        print("Cancelled.")
        return

    try:

        print("Starting jog...")

        jog_function(True)

        time.sleep(duration)

    except Exception as e:

        print(f"Jog error: {e}")

    finally:

        # Very important:
        # always attempt to clear the jog bit.
        try:
            jog_function(False)
            print("Jog stopped.")

        except Exception as e:
            print(
                "WARNING: failed to clear jog command: "
                f"{e}"
            )

            try:
                dome.stop_all()
                print(
                    "STOP ALL command sent as fallback."
                )

            except Exception as stop_error:
                print(
                    "CRITICAL: STOP ALL also failed: "
                    f"{stop_error}"
                )


# =========================================================
# Tracking Test
# =========================================================

def tracking_test():

    print_header("TRACKING TEST")

    if not dome.is_connected():
        print("Dome is not connected.")
        return

    print(
        "This writes target altitude and azimuth "
        "registers and enables dome tracking."
    )

    try:
        azimuth = int(
            input("Target azimuth value: ")
        )

        altitude = int(
            input("Target altitude value: ")
        )

    except ValueError:
        print("Values must be integers.")
        return

    print()
    print(f"Azimuth : {azimuth}")
    print(f"Altitude: {altitude}")

    confirm = input(
        "Write these values and enable tracking? [y/N]: "
    )

    if confirm.lower() != "y":
        print("Cancelled.")
        return

    try:

        dome.set_target_azimuth(azimuth)
        print("Target azimuth written.")

        dome.set_target_altitude(altitude)
        print("Target altitude written.")

        dome.enable_tracking()
        print("Tracking enabled.")

    except Exception as e:
        print(f"Tracking test failed: {e}")


# =========================================================
# Menu
# =========================================================

def show_menu():

    print()
    print("=" * 60)
    print("DASH1 DOME HARDWARE TEST")
    print("=" * 60)

    print()
    print("Connection")
    print("  1  - Connect")
    print("  2  - Disconnect")

    print()
    print("Status")
    print("  3  - Read all status values")
    print(" 3.5  - Read all coils")

    print()
    print("Whole dome")
    print("  4  - Open all")
    print("  5  - Close all")
    print("  6  - Progressive close")
    print("  7  - Stop all")

    print()
    print("Left shutter")
    print("  8  - Open left")
    print("  9  - Close left")
    print(" 10  - Stop left")
    print(" 11  - Jog left up")
    print(" 12  - Jog left down")

    print()
    print("Right shutter")
    print(" 13  - Open right")
    print(" 14  - Close right")
    print(" 15  - Stop right")
    print(" 16  - Jog right up")
    print(" 17  - Jog right down")

    print()
    print("Reset")
    print(" 18  - Fault reset")
    print(" 19  - BG reset")

    print()
    print("Tracking")
    print(" 20  - Enable tracking")
    print(" 21  - Disable tracking")
    print(" 22  - Set targets + enable tracking")

    print()
    print("Other")
    print("  0  - Exit")

    print()


def dump_coils():

    print("\nDOME COILS")
    print("-" * 40)

    for address in range(0, 41):

        try:

            value = connection.read_coil(
                address
            )

            print(
                f"{address:02d}: {value}"
            )

        except Exception as e:

            print(
                f"{address:02d}: ERROR - {e}"
            )


# =========================================================
# Main Program
# =========================================================

def main():

    while True:

        show_menu()

        choice = input("Select command: ").strip()

        if choice == "1":
            connect()

        elif choice == "2":
            disconnect()

        elif choice == "3":
            show_status()

        elif choice == "3.5":
            dump_coils()

        elif choice == "4":
            run_command(
                "Open all",
                dome.open_dome
            )

        elif choice == "5":
            run_command(
                "Close all",
                dome.close_dome
            )

        elif choice == "6":
            run_command(
                "Progressive close",
                dome.progressive_close
            )

        elif choice == "7":
            run_command(
                "STOP ALL",
                dome.stop_all
            )

        elif choice == "8":
            run_command(
                "Open left",
                dome.open_left
            )

        elif choice == "9":
            run_command(
                "Close left",
                dome.close_left
            )

        elif choice == "10":
            run_command(
                "Stop left",
                dome.stop_left
            )

        elif choice == "11":
            jog_test(
                "LEFT UP",
                dome.left_jog_up
            )

        elif choice == "12":
            jog_test(
                "LEFT DOWN",
                dome.left_jog_down
            )

        elif choice == "13":
            run_command(
                "Open right",
                dome.open_right
            )

        elif choice == "14":
            run_command(
                "Close right",
                dome.close_right
            )

        elif choice == "15":
            run_command(
                "Stop right",
                dome.stop_right
            )

        elif choice == "16":
            jog_test(
                "RIGHT UP",
                dome.right_jog_up
            )

        elif choice == "17":
            jog_test(
                "RIGHT DOWN",
                dome.right_jog_down
            )

        elif choice == "18":
            run_command(
                "Fault reset",
                dome.fault_reset
            )

        elif choice == "19":
            run_command(
                "BG reset",
                dome.bg_reset
            )

        elif choice == "20":
            run_command(
                "Enable tracking",
                dome.enable_tracking
            )

        elif choice == "21":
            run_command(
                "Disable tracking",
                dome.disable_tracking
            )

        elif choice == "22":
            tracking_test()

        elif choice == "0":

            print("\nExiting dome test.")

            if dome.is_connected():

                try:
                    dome.stop_all()
                except Exception:
                    pass

                try:
                    dome.disable_tracking()
                except Exception:
                    pass

                dome.disconnect()

            break

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()