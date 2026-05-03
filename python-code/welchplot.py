import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================================================
# SETTINGS
# ======================================================
file_name = "strategy1rule1slots14.csv"
T = 1000
w = 100

# ======================================================
# LOAD DATA
# ======================================================
df = pd.read_csv(file_name)
df = df[df["Week"] <= T]

# ======================================================
# WEEKLY MEAN OVER REPLICATIONS
# ======================================================
weekly = (
    df.groupby("Week")
      .mean(numeric_only=True)
      .reindex(range(1, T + 1))
)

# Variables
elective = weekly["Elective_App_WT"]
urgent   = weekly["Urgent_Scan_WT"]

# ======================================================
# WELCH METHOD
# cumulative average + moving average
# ======================================================
elective_welch = (
    elective.expanding()
            .mean()
            .rolling(window=w, center=True, min_periods=1)
            .mean()
)

urgent_welch = (
    urgent.expanding()
          .mean()
          .rolling(window=w, center=True, min_periods=1)
          .mean()
)

# ======================================================
# PLOT
# ======================================================
plt.style.use("ggplot")
plt.figure(figsize=(14,7))

weeks = np.arange(1, T + 1)

plt.plot(
    weeks,
    elective_welch,
    linewidth=2.5,
    label="Elective Appointment WT"
)

plt.plot(
    weeks,
    urgent_welch,
    linewidth=2.5,
    label="Urgent Scan WT"
)

# ======================================================
# Vertical reference line at week 60
# ======================================================
plt.axvline(
    x=150,
    linestyle=":",
    linewidth=2,
    color="black"
)

plt.title(f"Welch Plot (Window Size = {w})", fontsize=18, fontweight="bold")
plt.xlabel("Week", fontsize=14)
plt.ylabel("Moving Average Waiting Time", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.4)

plt.tight_layout()
plt.show()