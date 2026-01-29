# GPU-AGI-Guard

**Autonomous Gear Inhibitor** – A lightweight Python daemon that intelligently toggles your NVIDIA GPU between full-performance mode and ultra-low-power eco mode based on active workloads (games, renderers, AI inference, etc.). Uses only native `nvidia-smi`, logs metrics to CSV, and works in dry-run/monitor mode without a GPU.

Your local mini-AGI that guards power: beast mode when needed, eco-sleep when idle. No cloud, no bloat—just sovereign, energy-aware compute.

## 🚀 Quick Start (Linux – Ubuntu / Lubuntu recommended)

Requires Python 3.8+ and NVIDIA drivers (for real power changes; dry-run works without GPU).

```bash
# 1. Create project folder and navigate
mkdir -p ~/gpu-agi-guard && cd ~/gpu-agi-guard

# 2. Set up isolated virtual environment (safest)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependency
pip install psutil

# 4. Run in dry-run mode (monitors processes, no power changes)
python gpu_agi_guard.py --targets "blender,python,firefox,steam" --poll-interval 5 --dry-run --eco-power 60 --perf-power 300
```

- Deactivate venv when done: `deactivate`
- For real power control: Remove `--dry-run` and run with `sudo` if needed (nvidia-smi permissions).
- Windows: Use `py -3` instead of `python`, run as Administrator.

## Features
- Process-aware switching via psutil (detects target apps)
- Eco mode (low power limit) when idle; Perf mode (high limit) when targets active
- Up to 70% idle power savings (hardware-dependent, e.g., RTX 40/50-series)
- CSV logging (timestamp, mode, active targets, notes)
- Dry-run / monitor-only mode for dev/testing (no GPU required)
- Safe shutdown: Auto-resets to eco on exit
- Single dependency (psutil)

## CLI Options
- `--targets`: Comma-separated process names (e.g., "blender,python")
- `--poll-interval`: Check frequency in seconds (default 5)
- `--eco-power`: Idle power limit in watts (default 60)
- `--perf-power`: Active power limit in watts (default 300)
- `--dry-run`: Monitor/log only (default if no GPU detected)
- `--log-file`: CSV log path (default gpu_agi_guard_log.csv)

## Implementation Notes
- Relies on `nvidia-smi` for GPU control (query/set power limits).
- Monitoring works without elevation; power changes need admin/sudo.
- Extendable to AMD/Intel or Linux-native backends later.
- Battle-tested on constrained hardware — sovereign AI style.

## Troubleshooting
- `nvidia-smi` not found → Install NVIDIA drivers (`sudo ubuntu-drivers install` on Ubuntu).
- Permission errors → Run with `sudo` or enable unrestricted power control (`nvidia-smi -acp UNRESTRICTED` as root once).
- No mode switches → Verify target process names match exactly (case-insensitive).

## Contributing
PRs/issues welcome! Add profiles, AMD support, UI, or better prediction.

MIT License (see LICENSE file or standard text below).

*© 2026 Ghost Sigma Technologies LLC*  
*Built by Mr. Velasquez – AI Ecosystems Architect @ Ghost Sigma Technologies LLC*  
Sovereign agent swarms • RTX optimization • Linux/CUDA • GGUF quantization  
"Centralized AI extracts value. Sovereign AI creates it."