<div align="center">

# ⚡ Cyber Monitor CLI

**High-Performance System Dashboard with a Cyberpunk Aesthetic**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Style](https://img.shields.io/badge/Style-Cyberpunk-ff00ff?style=for-the-badge)](https://github.com/Textualize/rich)
[![Author](https://img.shields.io/badge/Author-aliden1z-orange?style=for-the-badge)](https://github.com/aliden1z)

<p align="center">
  <img src="screenshot.png" alt="Cyber Monitor Dashboard Preview" width="800">
</p>

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-built-with)

</div>

---

## 📖 About

**Cyber Monitor CLI** is a terminal-based system monitor designed for those who want more than just data—they want *style*. Unlike standard tools like `top` or `htop`, this dashboard delivers critical system metrics wrapped in a responsive, neon-themed TUI (Text User Interface).

Built for speed and aesthetics, it features **instant startup**, sparkline historical graphs, and real-time process tracking without clogging your terminal history.

## 🚀 Features

### 📊 System Health Matrix
- **Real-Time Core Stats:** Monitors CPU Load, RAM Usage, Swap Memory, and Load Averages (1m, 5m, 15m).
- **Sparkline Graphs:** Visualizes CPU history with a mini-chart (` ▂▃▄▅▆▇█`) that reacts to load changes.
- **Hardware Info:** Displays Hostname, Kernel, Uptime, and **Battery Status** (with charging indicators).

### 📡 I/O Traffic Stream
- **Network Speedometer:** Live tracking of Download (`⬇`) and Upload (`⬆`) speeds.
- **Disk Activity:** Real-time Read/Write speeds for your primary disk.
- **Storage Health:** Visual progress bar for Root Disk usage.

### 🔥 Top Process Tracker
- **Smart Sorting:** Automatically lists the top 5 resource-hungry processes.
- **Dual Metrics:** Shows both CPU% and Memory% for each process.
- **Efficiency:** Updates process lists intelligently (cached cycles) to minimize the monitor's own CPU footprint.

### 🎨 Cyberpunk UX
- **Neon Palette:** Custom theme using Bright Cyan, Spring Green, and Neon Magenta.
- **Responsive Layout:** Automatically adjusts to your terminal window size.
- **Zero Lag:** Optimized rendering loop ensures the UI never freezes.

## 📥 Installation

You can install Cyber Monitor globally on your system. This method creates an isolated virtual environment in `/opt/`, keeping your main Python setup clean.

### Option 1: Global Install (Recommended)

This allows you to run `cyber-monitor` from anywhere in your terminal.

```bash
# 1. Clone the repository
git clone https://github.com/aliden1z/cyber-monitor-cli.git
cd cyber-monitor-cli

# 2. Install using Make (Requires sudo)
sudo make install
```

Once installed, simply run:
```bash
cyber-monitor
```

**To uninstall:**
```bash
sudo make uninstall
```

### Option 2: Local Run (No Install)

If you just want to test it without installing:

```bash
# Install dependencies locally
pip install -r requirements.txt

# Run the script
python monitor.py
```

## 💻 Usage

Whether installed globally or running locally, the controls are the same:

- **Launch:** `cyber-monitor` or `python monitor.py`
- **Exit:** Press `Ctrl + C`

## 🛠️ Built With

This project relies on robust Python libraries to deliver performance and beauty.

| Library | Purpose |
| :--- | :--- |
| **[Rich](https://github.com/Textualize/rich)** | The rendering engine behind the TUI, tables, and neon colors. |
| **[Psutil](https://github.com/giampaolo/psutil)** | Cross-platform library for retrieving information on running processes and system utilization. |

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐧 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <small>Developed with ❤️ by <a href="https://github.com/aliden1z">aliden1z</a></small>
</div>
