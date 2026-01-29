#!/usr/bin/env python3
"""
gpu_agi_guard.py
Initial Autonomous Gear Inhibitor — starter script with dry-run support, CSV logging, safe shutdown.
Single dependency: psutil
"""
import argparse
import csv
import os
import subprocess
import sys
import time
from datetime import datetime

try:
    import psutil
except Exception:
    print("Missing dependency: psutil. Install with `pip install psutil` (inside venv).")
    raise SystemExit(1)

def parse_args():
    p = argparse.ArgumentParser(description="GPU-AGI-Guard — Autonomous Gear Inhibitor")
    p.add_argument('--targets', default="blender,python,firefox,steam",
                   help="Comma-separated process names to watch (case-insensitive, substring match)")
    p.add_argument('--poll-interval', type=int, default=5, help="Seconds between checks")
    p.add_argument('--eco-power', type=int, default=60, help="Eco power limit (W)")
    p.add_argument('--perf-power', type=int, default=300, help="Perf power limit (W)")
    p.add_argument('--dry-run', action='store_true', help="Monitor/log only; do not change power")
    p.add_argument('--log-file', default="gpu_agi_guard_log.csv", help="CSV log path")
    return p.parse_args()

def detect_nvidia():
    try:
        out = subprocess.check_output(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                                      stderr=subprocess.STDOUT).decode().strip()
        return bool(out)
    except Exception:
        return False

def ensure_log(path):
    exists = os.path.exists(path)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if not exists:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "mode", "active_targets", "note"])

def set_power_limit(watts, dry_run, has_nvidia):
    if dry_run or not has_nvidia:
        return f"[DRY RUN] Would set power limit to {watts}W"
    try:
        subprocess.run(['nvidia-smi', '-pl', str(int(watts))], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f"Power limit set to {watts}W"
    except Exception as e:
        return f"Power set failed: {e}"

def main():
    args = parse_args()
    targets = [t.strip().lower() for t in args.targets.split(',') if t.strip()]
    has_nvidia = detect_nvidia()
    if has_nvidia:
        print("NVIDIA GPU detected (nvidia-smi available).")
    else:
        print("No NVIDIA GPU detected or nvidia-smi failed — running in monitor/dry-run mode by default.")
    ensure_log(args.log_file)
    mode = "ECO"
    print(f"Starting GPU-AGI-Guard (mode={{mode}}). Ctrl+C to stop.")
    try:
        while True:
            try:
                active = [p.info.get('name', '') or '' for p in psutil.process_iter(['name'])]
                active = [a.lower() for a in active if a]
            except Exception as e:
                print(f"Failed to enumerate processes: {e}")
                active = []
            found = any(t in proc for proc in active for t in targets)
            new_mode = "PERF" if found else "ECO"
            if new_mode != mode:
                mode = new_mode
                power = args.perf_power if mode == "PERF" else args.eco_power
                note = set_power_limit(power, args.dry_run or not has_nvidia, has_nvidia)
                active_list = ",".join(sorted({t for t in targets if any(t in proc for proc in active)}))
                ts = datetime.utcnow().isoformat()
                print(f"{{ts}} | Mode={{mode}} | Active=[{{active_list}}] | {{note}}")
                try:
                    with open(args.log_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([ts, mode, active_list, note])
                except Exception as e:
                    print(f"Failed to write log: {e}")
            time.sleep(max(1, args.poll_interval))
    except KeyboardInterrupt:
        print("Received interrupt — attempting safe shutdown (reset to ECO if possible).")
        try:
            if not (args.dry_run or not has_nvidia):
                subprocess.run(['nvidia-smi', '-pl', str(int(args.eco_power))], check=False)
        except Exception:
            pass
        print("Exited cleanly.")
    except Exception as e:
        print(f"Unhandled error in main loop: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()