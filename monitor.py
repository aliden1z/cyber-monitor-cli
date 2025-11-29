import psutil
import time
import platform
from datetime import datetime
from collections import deque
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich import box
from rich.align import Align

# ⚡ Cyber Monitor CLI - Developed by aliden1z

class CyberMonitor:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # Prime CPU counter to avoid 0% on startup
        psutil.cpu_percent()

        # Configuration
        self.proc_refresh_rate = 2  # Update processes every 2 seconds
        self.tick = 0
        self.cached_procs = []
        self.cpu_history = deque([0]*40, maxlen=40)

        # I/O Cache for speed calculations
        self.last_net = psutil.net_io_counters()
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()

        # Static System Info
        self.boot_time = psutil.boot_time()
        self.sys_info = {
            "node": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
        }

        self._init_layout()

    def _init_layout(self):
        """Initializes the TUI layout structure."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=1)
        )
        self.layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=2)
        )
        self.layout["right"].split_column(
            Layout(name="procs", ratio=3),
            Layout(name="storage", ratio=2)
        )

    def get_size(self, bytes, suffix="B"):
        """Converts bytes to human readable format."""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.1f}{unit}{suffix}"
            bytes /= factor

    def make_bar(self, percent, color="bright_cyan"):
        """Generates a text-based progress bar."""
        width = 20
        filled = int(width * (percent / 100))
        bar = "━" * filled + " " * (width - filled)
        return f"[{color}]{bar}[/] [bold white]{percent:.1f}%[/]"

    def generate_sparkline(self, data):
        """Generates a mini text graph for CPU history."""
        bars = "  ▂▃▄▅▆▇█"
        if not data: return ""
        graph = ""
        for val in data:
            idx = int((val / 100) * (len(bars) - 1))
            idx = max(0, min(idx, len(bars) - 1))
            color = "spring_green1" if val < 50 else "gold1" if val < 80 else "deep_pink2"
            graph += f"[{color}]{bars[idx]}[/]"
        return graph

    def get_header(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        title = f"[bold bright_cyan]⚡ CYBER-MONITOR[/] [dim]v1.2[/]"
        clock = datetime.now().strftime("%H:%M:%S")
        info = f"[italic white]by aliden1z[/]  |  [bold spring_green1]{clock}[/]"

        grid.add_row(title, info)
        return Panel(grid, style="white on black", box=box.HEAVY_EDGE, padding=(0, 1))

    def get_system_panel(self):
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(style="bold bright_cyan")
        grid.add_column(justify="right")

        # Load Average
        try:
            l1, l5, l15 = psutil.getloadavg()
            grid.add_row("Load Avg", f"[spring_green1]{l1:.2f}[/] [gold1]{l5:.2f}[/] [deep_pink2]{l15:.2f}[/]")
        except:
            grid.add_row("Load Avg", "N/A")

        # Uptime
        uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.boot_time))
        grid.add_row("Uptime", f"[bold white]{uptime}[/]")

        # Battery
        if hasattr(psutil, "sensors_battery"):
            batt = psutil.sensors_battery()
            if batt:
                icon = "⚡" if batt.power_plugged else "🔋"
                color = "green" if batt.percent > 20 else "red"
                grid.add_row("Battery", f"[{color}]{icon} {batt.percent}%[/]")

        grid.add_row(" ", " ")

        # CPU
        cpu = psutil.cpu_percent()
        self.cpu_history.append(cpu)
        grid.add_row("[bold white]CPU Load[/]", f"[bold white]{cpu}%[/]")
        grid.add_row(self.generate_sparkline(self.cpu_history), "")

        # RAM
        mem = psutil.virtual_memory()
        grid.add_row(" ", " ")
        grid.add_row("RAM Usage", self.make_bar(mem.percent, "bright_magenta"))
        grid.add_row(" ", f"[dim]{self.get_size(mem.used)} / {self.get_size(mem.total)}[/dim]")

        # Swap
        swap = psutil.swap_memory()
        if swap.total > 0:
            grid.add_row("Swap", self.make_bar(swap.percent, "deep_sky_blue1"))

        return Panel(grid, title="[bold bright_cyan]SYSTEM HEALTH[/]", border_style="bright_cyan", box=box.ROUNDED)

    def get_process_panel(self, force=False):
        # Update processes only every N seconds to save resources
        if force or (self.tick % self.proc_refresh_rate == 0):
            try:
                self.cached_procs = sorted(
                    [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])],
                    key=lambda p: p['cpu_percent'] or 0, reverse=True
                )[:5]
            except: pass

        table = Table(box=box.SIMPLE_HEAD, expand=True, show_edge=False, padding=(0,0))
        table.add_column("PID", style="dim", width=6)
        table.add_column("TASK", style="bold white", ratio=1)
        table.add_column("CPU%", justify="right", style="spring_green1", width=6)
        table.add_column("MEM%", justify="right", style="gold1", width=6)

        if not self.cached_procs:
            table.add_row("-", "Scanning...", "-", "-")
        else:
            for p in self.cached_procs:
                name = p['name'] or "?"
                table.add_row(str(p['pid']), name[:15], f"{p['cpu_percent']:.1f}", f"{p['memory_percent']:.1f}")

        return Panel(table, title="[bold bright_magenta]TOP PROCESSES[/]", border_style="bright_magenta", box=box.ROUNDED)

    def get_storage_net_panel(self):
        t = time.time()
        dt = t - self.last_time
        dt = 1 if dt <= 0 else dt

        net = psutil.net_io_counters()
        disk = psutil.disk_io_counters()

        # Calculate Speeds
        net_in = (net.bytes_recv - self.last_net.bytes_recv) / dt
        net_out = (net.bytes_sent - self.last_net.bytes_sent) / dt
        disk_r = (disk.read_bytes - self.last_disk.read_bytes) / dt
        disk_w = (disk.write_bytes - self.last_disk.write_bytes) / dt

        self.last_net, self.last_disk, self.last_time = net, disk, t

        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column("SOURCE", style="bold gold1")
        grid.add_column("IN / READ", justify="right", style="spring_green1")
        grid.add_column("OUT / WRITE", justify="right", style="deep_sky_blue1")

        grid.add_row("NETWORK", f"⬇ {self.get_size(net_in)}/s", f"⬆ {self.get_size(net_out)}/s")
        grid.add_row("DISK I/O", f"R: {self.get_size(disk_r)}/s", f"W: {self.get_size(disk_w)}/s")

        # Disk Usage
        du = psutil.disk_usage('/')
        usage_color = "spring_green1" if du.percent < 80 else "deep_pink2"

        wrapper = Table.grid(expand=True)
        wrapper.add_row(grid)
        wrapper.add_row(" ")
        wrapper.add_row(f"[bold white]Root Disk:[/] [dim]{self.get_size(du.free)} Free[/]")
        wrapper.add_row(self.make_bar(du.percent, usage_color))

        return Panel(wrapper, title="[bold spring_green1]STORAGE & NET[/]", border_style="spring_green1", box=box.ROUNDED)

    def update(self, init=False):
        self.layout["header"].update(self.get_header())
        self.layout["left"].update(self.get_system_panel())
        self.layout["procs"].update(self.get_process_panel(force=init))
        self.layout["storage"].update(self.get_storage_net_panel())

        if not init:
            self.layout["footer"].update(Align.center(f"[dim italic]System: {self.sys_info['node']} | Press Ctrl+C to Exit[/]"))

    def run(self):
        self.update(init=True) # Immediate render

        with Live(self.layout, refresh_per_second=4, screen=True) as live:
            try:
                while True:
                    self.tick += 1
                    self.update()
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    try:
        CyberMonitor().run()
    except Exception as e:
        print(f"Error: {e}")
