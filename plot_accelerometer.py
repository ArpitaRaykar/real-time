import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_INPUT = "accelerometer_3min.csv"
DEFAULT_OUTPUT = "accelerometer_chart.png"


def load_data(csv_path):
    """Load numeric accelerometer columns from a CSV file."""
    time_values = []
    x_values = []
    y_values = []
    z_values = []

    with csv_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required_columns = {"Time_s", "X", "Y", "Z"}
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {missing}")

        for row in reader:
            try:
                time_values.append(float(row["Time_s"]))
                x_values.append(float(row["X"]))
                y_values.append(float(row["Y"]))
                z_values.append(float(row["Z"]))
            except (TypeError, ValueError):
                continue

    if not time_values:
        raise ValueError("No valid accelerometer rows were found.")

    return time_values, x_values, y_values, z_values


def create_chart(input_path, output_path):
    time_values, x_values, y_values, z_values = load_data(input_path)

    figure, axes = plt.subplots(
        2,
        1,
        figsize=(12, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )
    figure.suptitle("Accelerometer Motion", fontsize=16, fontweight="bold")

    axes[0].plot(time_values, x_values, label="X", linewidth=1.2)
    axes[0].plot(time_values, y_values, label="Y", linewidth=1.2)
    axes[0].plot(time_values, z_values, label="Z", linewidth=1.2)
    axes[0].set_ylabel("Acceleration")
    axes[0].set_title("Acceleration by axis")
    axes[0].legend(loc="upper right")
    axes[0].grid(alpha=0.25)

    magnitude = [
        (x * x + y * y + z * z) ** 0.5
        for x, y, z in zip(x_values, y_values, z_values)
    ]
    axes[1].plot(time_values, magnitude, color="#d95f02", linewidth=1.2)
    axes[1].set_xlabel("Time (seconds)")
    axes[1].set_ylabel("Magnitude")
    axes[1].set_title("Acceleration magnitude")
    axes[1].grid(alpha=0.25)

    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    print(f"Chart saved to: {output_path}")
    print(f"Rows plotted: {len(time_values)}")


if __name__ == "__main__":
    input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_INPUT)
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(DEFAULT_OUTPUT)

    try:
        create_chart(input_file, output_file)
    except (OSError, ValueError) as error:
        print(f"Could not create chart: {error}", file=sys.stderr)
        raise SystemExit(1)
