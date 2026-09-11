import requests
import csv
import time
from datetime import datetime

# =========================================================
# PHYPOX CONNECTION
# =========================================================

PHYPOX_URL = "http://192.168.203.152:8080"

API_URL = (
    PHYPOX_URL
    + "/get?accX&accY&accZ&acc_time"
)

# =========================================================
# RECORDING SETTINGS
# =========================================================
# 180 seconds = 3 minutes
DURATION = 180

CSV_FILE = "accelerometer_3min.csv"

# =========================================================
# CHECK CONNECTION
# =========================================================

print("=" * 60)
print("REAL-TIME ACCELEROMETER DATA COLLECTION")
print("=" * 60)

print("\nChecking Phyphox connection...")

try:
    response = requests.get(API_URL, timeout=5)

    if response.status_code == 200:
        print(" Phyphox connection successful")

    else:
        print("✗ Phyphox returned status:", response.status_code)
        exit()

except Exception as e:
    print("✗ Cannot connect to Phyphox")
    print("Error:", e)
    exit()

# =========================================================
# START RECORDING
# =========================================================

print("\nStarting 3-minute recording...")
print("Put the phone in your pocket.")
print("Walk normally for 3 minutes.")
print("Do not close Phyphox.\n")

start_time = time.time()
row_count = 0
last_sensor_time = None

# =========================================================
# CREATE CSV
# =========================================================

with open(
    CSV_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # Header
    writer.writerow([
        "Timestamp",
        "Time_s",
        "X",
        "Y",
        "Z"
    ])

    # =====================================================
    # CONTINUOUS COLLECTION
    # =====================================================

    while time.time() - start_time < DURATION:

        try:

            response = requests.get(
                API_URL,
                timeout=5
            )

            data = response.json()

            # -------------------------------------------------
            # Extract buffers
            # -------------------------------------------------

            x_buffer = data["buffer"]["accX"]["buffer"]
            y_buffer = data["buffer"]["accY"]["buffer"]
            z_buffer = data["buffer"]["accZ"]["buffer"]
            time_buffer = data["buffer"]["acc_time"]["buffer"]

            # -------------------------------------------------
            # Process available readings
            # -------------------------------------------------

            for x, y, z, sensor_time in zip(
                x_buffer,
                y_buffer,
                z_buffer,
                time_buffer
            ):

                # Skip missing X/Y/Z values
                if x is None or y is None or z is None:
                    continue

                # -------------------------------------------------
                # Sensor time may sometimes be None.
                # If it is valid, use it.
                # Otherwise use elapsed computer time.
                # -------------------------------------------------

                if sensor_time is not None:

                    try:
                        sensor_time = float(sensor_time)

                        if last_sensor_time is not None:
                            if sensor_time <= last_sensor_time:
                                continue

                        last_sensor_time = sensor_time

                    except (TypeError, ValueError):
                        sensor_time = None

                # -------------------------------------------------
                # Elapsed time from Python
                # -------------------------------------------------

                elapsed = time.time() - start_time

                # -------------------------------------------------
                # Actual timestamp
                # -------------------------------------------------

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )[:-3]

                # -------------------------------------------------
                # Write CSV
                # -------------------------------------------------

                writer.writerow([
                    timestamp,
                    round(elapsed, 4),
                    x,
                    y,
                    z
                ])

                row_count += 1

            # Immediately save data
            file.flush()

            # -------------------------------------------------
            # Progress
            # -------------------------------------------------

            elapsed_total = time.time() - start_time
            remaining = max(
                0,
                DURATION - elapsed_total
            )

            print(
                f"\rTime: {elapsed_total:6.1f}/"
                f"{DURATION} sec | "
                f"Rows: {row_count:5d} | "
                f"Remaining: {remaining:5.1f} sec",
                end=""
            )

        except requests.exceptions.RequestException as e:

            print(
                "\nConnection problem:",
                e
            )

        except (KeyError, TypeError, ValueError) as e:

            print(
                "\nData problem:",
                e
            )

        except Exception as e:

            print(
                "\nUnexpected problem:",
                e
            )

        # Small delay
        time.sleep(0.1)

# =========================================================
# FINISHED
# =========================================================

print("\n\n" + "=" * 60)
print("RECORDING COMPLETED")
print("=" * 60)

print("Rows collected :", row_count)
print("CSV file       :", CSV_FILE)

if row_count == 0:
    print("\nWARNING: No data was collected.")
else:
    print("\n✓ Data successfully saved!")
    print("✓ Timestamp + X + Y + Z are available.")

print("=" * 60)