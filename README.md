# ⚡ Cyber Monitor CLI

This is a terminal-based system monitor dashboard I built using Python. 

I wanted something that looks cooler than the standard `top` command and gives me a "cyberpunk" vibe while monitoring my Linux system. It runs completely in the terminal but features a responsive, panel-based UI.

## 📸 Dashboard Preview

![Cyber Monitor Screenshot](screenshot.png)

## 🚀 Features

- **Real-Time Monitoring:** Updates CPU, RAM, Swap, and Disk usage every second.
- **Network Speedometer:** Shows live Download and Upload speeds (KB/s or MB/s).
- **System Info Panel:** Displays your OS, Kernel version, Hostname, and CPU frequency.
- **Visual Indicators:** Progress bars change color based on load (Green → Yellow → Red).
- **Full Screen:** Runs in a dedicated screen buffer (doesn't clutter your terminal history).

## 🛠️ Built With

- **Python 3**
- **Rich** (For the TUI and layout)
- **Psutil** (For fetching system metrics)

## 📥 Installation

You can install Cyber Monitor globally with a single command. It will automatically set up an isolated environment for dependencies.

```bash
git clone https://github.com/aliden1z/cyber-monitor-cli.git
cd cyber-monitor-cli
sudo make install
```

To run the dashboard:
```bash
cyber-monitor
```

To uninstall:
```bash
sudo make uninstall
```

## 💻 Usage

Just run the script:

```bash
python monitor.py
```

*Press `Ctrl + C` to exit the dashboard safely.*

## 🐧 License

MIT License. Feel free to modify and use it!
