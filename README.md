# Real-Time Phyphox Acceleration Dashboard

This project collects real-time acceleration data from an Android smartphone using the Phyphox mobile application and its HTTP API. The collected X, Y, and Z acceleration values are processed using Python to calculate acceleration magnitude, detect walking steps, and generate visualizations for analysis.

## What I did

- Connected an Android smartphone to Python through the Phyphox HTTP API.
- Used the **Acceleration with g** experiment in Phyphox.
- Collected timestamped X, Y, and Z acceleration values.
- Recorded accelerometer data for approximately **3 minutes**.
- Saved the collected sensor readings into a CSV file.
- Calculated acceleration magnitude using:

  `A = sqrt(X^2 + Y^2 + Z^2)`

- Implemented step detection using local acceleration peaks.
- Used an acceleration threshold to identify possible walking steps.
- Added a minimum time interval between detected steps to reduce duplicate detections.
- Calculated:
  - Total detected steps
  - Steps per minute
  - Average steps per minute
  - Maximum acceleration
- Generated graphs for:
  - X, Y, and Z acceleration over time
  - Acceleration magnitude over time
  - Detected steps
  - Steps per minute
  - Maximum acceleration by minute
- Created a combined acceleration dashboard for visualization and analysis.
- Tested the visualization functions to ensure that the graphs are generated correctly.

## Files

- `main.py` - connects to Phyphox, collects acceleration data, performs step detection, and saves the CSV.
- `visualize.py` - contains functions for generating acceleration and step-analysis graphs.
- `test_visualize.py` - tests whether the graphs and dashboard are generated successfully.
- `accelerometer_3min.csv` - collected accelerometer dataset.
- `acceleration_dashboard.png` - combined dashboard containing the analysis graphs.
- `requirements.txt` - contains the required Python libraries.

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txtREADME.md
