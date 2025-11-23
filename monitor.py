import psutil
import time
import platform
import os
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich import box

# Global variables to calculate network speed
last_net_io = psutil.net_io_counters()
last_time = time.time()

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format e.g:
    1253656 => '1.20 MB'
    1253656678 => '1.17 GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def get_progress_bar(percent, width=20):
    """
    Generates a colorful progress bar based on percentage.
    Green (<50%) -> Yellow (<80%) -> Red (>80%)
    """
    if percent < 50:
        color = "[green]"
    elif percent < 80:
        color = "[yellow]"
    else:
        color = "[bold red]"
        
    filled = int(width * percent // 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"{color}{bar}[/] {percent:.1f}%"

def get_system_info():
    """
    Fetches static system information (OS, Kernel, Hostname).
    """
    uname = platform.uname()
    grid = Table.grid(expand=True)
    grid.add_column(style="bold cyan")
    grid.add_column(style="white")
    
    grid.add_row("System:", f"{uname.system} {uname.release}")
    grid.add_row("Node Name:", uname.node)
    grid.add_row("Architecture:", uname.machine)
    
    # Try to get CPU frequency if available
    try:
        freq = psutil.cpu_freq()
        if freq:
            grid.add_row("CPU Freq:", f"{freq.current:.0f} Mhz")
    except:
        pass

    return Panel(
        grid, 
        title="[bold blue]SYSTEM INFO[/bold blue]",
        border_style="blue",
        box=box.ROUNDED
    )

def get_metrics_table():
    """
    Generates the main metrics table with real-time data.
    """
    global last_net_io, last_time

    table = Table(box=box.SIMPLE, expand=True, show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Visual", ratio=1)
    table.add_column("Value", justify="right", style="bold white")

    # --- CPU ---
    cpu_pct = psutil.cpu_percent()
    table.add_row("CPU Load", get_progress_bar(cpu_pct), f"{cpu_pct}%")

    # --- RAM ---
    mem = psutil.virtual_memory()
    mem_str = f"{get_size(mem.used)} / {get_size(mem.total)}"
    table.add_row("RAM Usage", get_progress_bar(mem.percent), mem_str)

    # --- SWAP ---
    swap = psutil.swap_memory()
    table.add_row("SWAP Memory", get_progress_bar(swap.percent), f"{get_size(swap.used)}")

    # --- DISK ---
    disk = psutil.disk_usage('/')
    disk_str = f"{get_size(disk.free)} Free"
    table.add_row("Disk (Root)", get_progress_bar(disk.percent), disk_str)

    # --- NETWORK SPEED CALCULATION ---
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    
    # Calculate difference
    time_delta = current_time - last_time
    # Avoid division by zero
    if time_delta == 0: time_delta = 1 

    bytes_sent = current_net_io.bytes_sent - last_net_io.bytes_sent
    bytes_recv = current_net_io.bytes_recv - last_net_io.bytes_recv
    
    speed_sent = bytes_sent / time_delta
    speed_recv = bytes_recv / time_delta
    
    # Update globals for next loop
    last_net_io = current_net_io
    last_time = current_time

    net_visual = f"[green]⬇ {get_size(speed_recv)}/s[/green]  [blue]⬆ {get_size(speed_sent)}/s[/blue]"
    net_total = f"Tot: {get_size(current_net_io.bytes_recv)}"
    table.add_row("Network Speed", net_visual, net_total)

    return Panel(
        table,
        title="[bold magenta]REAL-TIME METRICS[/bold magenta]",
        border_style="magenta",
        box=box.ROUNDED
    )

def make_layout():
    """
    Defines the layout structure: Header, Main (Split into Info & Metrics), Footer.
    """
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    
    return layout

def get_header():
    """Renders the top header."""
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right")
    
    grid.add_row(
        "[bold cyan]⚡ CYBER-MONITOR CLI[/bold cyan] [dim]v1.0 Beta by aliden1z[/dim]",
        datetime.now().strftime("[bold yellow]%Y-%m-%d %H:%M:%S[/bold yellow]")
    )
    return Panel(grid, style="white on black", box=box.HEAVY_EDGE)

def get_footer():
    """Renders the footer with uptime info."""
    uptime_s = time.time() - psutil.boot_time()
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    
    text = Text(f"System Uptime: {uptime_str} | Active User: {os.getlogin()} | Press Ctrl+C to Exit", justify="center", style="italic dim")
    return Panel(text, style="white on black", box=box.HEAVY_EDGE)

if __name__ == "__main__":
    layout = make_layout()
    
    # Using 'screen=True' for full-screen application mode
    with Live(layout, refresh_per_second=1, screen=True) as live:
        try:
            while True:
                layout["header"].update(get_header())
                layout["left"].update(get_system_info())
                layout["right"].update(get_metrics_table())
                layout["footer"].update(get_footer())
                time.sleep(1) # 1 second update rate for accurate network speed
        except KeyboardInterrupt:
            pass
