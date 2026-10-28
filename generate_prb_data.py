"""
generate_prb_data.py
Creates one week of synthetic hourly PRB utilization for cells in a shopping mall.
All data is made up - no real operator data.
"""

import random
import csv

random.seed(42)  # same "random" numbers every run, so results are repeatable

# The cells in our imaginary mall.
# base_peak = how busy the cell gets at its busiest hour (in % PRB)
cells = [
    {"cell": "MALL_L1800_S1", "layer": "coverage", "base_peak": 75},
    {"cell": "MALL_L2100_S1", "layer": "capacity", "base_peak": 60},
    {"cell": "MALL_L2600_S1", "layer": "capacity", "base_peak": 45},
]

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def mall_traffic_shape(hour, day):
    """Returns how busy the mall is (0.0 to 1.0) at a given hour and day."""
    if hour < 6:
        shape = 0.03                     # night: mall closed, almost empty
    elif hour < 10:
        shape = 0.10                     # morning: staff and cleaners only
    elif hour < 17:
        shape = 0.50                     # daytime shoppers
    elif hour < 22:
        shape = 1.00                     # evening peak
    else:
        shape = 0.25                     # closing time

    if day in ["Sat", "Sun"]:
        shape = shape * 1.2              # weekends are busier
    return min(shape, 1.0)


rows = []
for day in days:
    for hour in range(24):
        for c in cells:
            prb = c["base_peak"] * mall_traffic_shape(hour, day)
            prb = prb * random.uniform(0.9, 1.1)   # +/-10% random variation
            prb = prb + random.uniform(0.5, 2.0)   # signalling never lets PRB hit 0
            prb = max(0, min(100, round(prb, 1)))  # keep between 0 and 100
            rows.append({
                "day": day,
                "hour": hour,
                "cell": c["cell"],
                "layer": c["layer"],
                "prb_util_pct": prb,
            })

with open("prb_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created prb_data.csv with {len(rows)} rows")
print("First 5 rows:")
for r in rows[:5]:
    print(r)