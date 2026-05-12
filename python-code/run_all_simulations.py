"""
run_all_simulations.py
----------------------
Draait automatisch alle combinaties:
  - Strategieën: S1, S2, S3
  - Urgente slots: 10 t/m 20
  - Rules: 1, 2, 3, 4

Resultaten → FinalOutput.csv  (te openen in Excel)

Gebruik:
  python run_all_simulations.py
"""

import csv
import os
import random
import time

from simulation import Simulation

# ══════════════════════════════════════════════════════════════════
# INSTELLINGEN
# ══════════════════════════════════════════════════════════════════
W      = 100          # weken per simulatie (verhoog naar 500 voor finale run)
R      = 10           # replicaties
RULES  = [1, 2, 3, 4]
STRATEGIES   = [1, 2, 3]
URGENT_SLOTS = list(range(10, 21))  # 10, 11, ..., 20
OUTPUT_FILE  = "FinalOutput.csv"

def get_filename(strategy: int, n_urgent: int) -> str:
    return f"input-S{strategy}-{n_urgent}.txt"

# ══════════════════════════════════════════════════════════════════
# CSV HEADER
# ══════════════════════════════════════════════════════════════════
FIELDNAMES = ['Filename', 'Strategy', 'UrgentSlots', 'Rule',
              'ElAppWT', 'ElScanWT', 'UrScanWT', 'OT', 'OV']

write_header = not os.path.exists(OUTPUT_FILE)
with open(OUTPUT_FILE, mode='a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter=';')
    if write_header:
        writer.writeheader()

# ══════════════════════════════════════════════════════════════════
# HOOFD-LOOP
# ══════════════════════════════════════════════════════════════════
total = len(STRATEGIES) * len(URGENT_SLOTS) * len(RULES)
done  = 0
overall_start = time.time()

print(f"{'='*65}")
print(f"  Totaal: {total} combinaties  (W={W}, R={R})")
print(f"{'='*65}\n")

results_summary = []

for strategy in STRATEGIES:
    for n_urgent in URGENT_SLOTS:
        filename = get_filename(strategy, n_urgent)

        if not os.path.exists(filename):
            print(f"  [SKIP] Niet gevonden: {filename}")
            continue

        for rule in RULES:
            done += 1
            label = f"S{strategy}-{n_urgent}slots-Rule{rule}"
            print(f"[{done}/{total}] {label} ...", end=' ', flush=True)
            t0 = time.time()

            try:
                sim = Simulation(filename, W, R, rule)
                sim.setWeekSchedule()

                el_app_list  = []
                el_scan_list = []
                ur_scan_list = []
                ot_list      = []
                ov_list      = []

                for r in range(R):
                    sim.resetSystem()
                    random.seed(r)
                    sim.runOneSimulation()

                    ov = sim.avgElectiveAppWT * sim.weightEl + sim.avgUrgentScanWt * sim.weightUr
                    el_app_list.append(sim.avgElectiveAppWT)
                    el_scan_list.append(sim.avgElectiveScanWT)
                    ur_scan_list.append(sim.avgUrgentScanWt)
                    ot_list.append(sim.avgOT)
                    ov_list.append(ov)

                avg_el_app  = sum(el_app_list)  / R
                avg_el_scan = sum(el_scan_list) / R
                avg_ur_scan = sum(ur_scan_list) / R
                avg_ot      = sum(ot_list)      / R
                avg_ov      = sum(ov_list)      / R

                with open(OUTPUT_FILE, mode='a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter=';')
                    writer.writerow({
                        'Filename':    filename[:-4],
                        'Strategy':    strategy,
                        'UrgentSlots': n_urgent,
                        'Rule':        rule,
                        'ElAppWT':     round(avg_el_app,  4),
                        'ElScanWT':    round(avg_el_scan, 4),
                        'UrScanWT':    round(avg_ur_scan, 4),
                        'OT':          round(avg_ot,      4),
                        'OV':          round(avg_ov,      4),
                    })

                elapsed = time.time() - t0
                print(f"OK  OV={avg_ov:.4f}  ({elapsed:.1f}s)")
                results_summary.append((label, avg_ov))

            except Exception as e:
                print(f"FOUT: {e}")

# ══════════════════════════════════════════════════════════════════
# EINDOVERZICHT
# ══════════════════════════════════════════════════════════════════
total_elapsed = time.time() - overall_start
print(f"\n{'='*65}")
print(f"  Klaar!  Tijd: {total_elapsed/60:.1f} minuten")
print(f"  Output: {OUTPUT_FILE}")
print(f"{'='*65}\n")

if results_summary:
    results_summary.sort(key=lambda x: x[1])
    print("Top 5 beste configuraties (laagste OV):")
    for rank, (lbl, ov) in enumerate(results_summary[:5], 1):
        print(f"  {rank}. {lbl:35s}  OV = {ov:.4f}")