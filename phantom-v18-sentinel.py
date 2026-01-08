# ==============================================================================
# PHANTOM-IG CORE: v18.6 SENTINEL
# Developed by: cappiavi
# 
# REQUIRED PIP PACKAGES:
# pip install instaloader rich requests
#
# PURPOSE: High-resilience, future-proof Instagram media extraction with 
# persistent manifest tracking and neural activity monitoring.
# ==============================================================================

import instaloader
import sys, os, time, random, sqlite3, collections, socket
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, MofNCompleteColumn, TimeRemainingColumn
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from rich.align import Align

console = Console()

class SentinelEngine:
    def __init__(self):
        self.dev = "cappiavi"
        self.version = "v18.6 SENTINEL"
        self.start_time = datetime.now()
        self.db_path = "citadel_manifest.db"
        self.db_conn = sqlite3.connect(self.db_path)
        self.activity_log = collections.deque(maxlen=10)
        self.stats = {"downloaded": 0, "skipped": 0, "errors": 0, "latency": 0}
        self._init_db()

    def _init_db(self):
        self.db_conn.execute("CREATE TABLE IF NOT EXISTS downloads (shortcode TEXT PRIMARY KEY)")
        self.db_conn.commit()

    def is_downloaded(self, shortcode):
        cur = self.db_conn.execute("SELECT 1 FROM downloads WHERE shortcode = ?", (shortcode,))
        return cur.fetchone() is not None

    def mark_done(self, shortcode):
        self.db_conn.execute("INSERT OR IGNORE INTO downloads VALUES (?)", (shortcode,))
        self.db_conn.commit()
        self.stats["downloaded"] += 1

    def log(self, message, style="white"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.append(f"[dim]{timestamp}[/] [{style}]{message}[/]")

    def close_db(self):
        self.db_conn.close()

engine = SentinelEngine()

def get_net_health():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=1.5)
        return "[bold green]ONLINE[/]"
    except: return "[bold red]OFFLINE[/]"

def clean_exit():
    engine.close_db()
    os.system('cls' if os.name == 'nt' else 'clear')
    msg = Align.center(f"\n[bold red]PHANTOM CORE: SENTINEL TERMINATED[/]\n[white]Manifest Secured. Session Logged.\n[magenta]By {engine.dev}[/]")
    console.print(msg)
    sys.exit(0)

def make_layout(progress_bar, target="NONE"):
    layout = Layout()
    layout.split_row(
        Layout(name="main", ratio=2),
        Layout(name="side", size=42)
    )
    
    # --- MAIN VIEWPORT ---
    log_content = "\n".join(engine.activity_log)
    layout["main"].split_column(
        Layout(Panel(Align.left(log_content), title="[bold]NEURAL ACTIVITY FEED[/]", border_style="bright_magenta"), ratio=1),
        Layout(Panel(progress_bar, title=f"TARGET: @{target}", border_style="cyan"), size=5)
    )
    
    # --- ENHANCED SIDE PANEL ---
    side_table = Table.grid(padding=1)
    total_ops = engine.stats['downloaded'] + engine.stats['errors']
    success_rate = (engine.stats['downloaded'] / total_ops * 100) if total_ops > 0 else 100
    
    side_table.add_row(f"[bold cyan]ENGINE:[/] {engine.version}")
    side_table.add_row(f"[bold cyan]UPTIME:[/] {str(datetime.now()-engine.start_time).split('.')[0]}")
    side_table.add_row(f"[bold cyan]NET HEALTH:[/] {get_net_health()}")
    side_table.add_row("-" * 25)
    side_table.add_row("[bold yellow]THROUGHPUT STATS[/]")
    side_table.add_row(f" • [white]Saved Media:[/] [green]{engine.stats['downloaded']}[/]")
    side_table.add_row(f" • [white]Deduplicated:[/] [blue]{engine.stats['skipped']}[/]")
    side_table.add_row(f" • [white]Success Rate:[/] [bold {'green' if success_rate > 90 else 'yellow'}]{success_rate:.1f}%[/]")
    side_table.add_row("-" * 25)
    side_table.add_row("[bold red]NETWORK DIAGNOSTICS[/]")
    side_table.add_row(f" • [white]Server Latency:[/] [blue]{engine.stats['latency']}ms[/]")
    risk_color = "green" if engine.stats['latency'] < 400 else "red"
    side_table.add_row(f" • [white]Throttle Risk:[/] [{risk_color}]LOW[/]" if risk_color == "green" else f" • [white]Throttle Risk:[/] [{risk_color}]HIGH[/]")
    
    layout["side"].update(Panel(side_table, title="CORE MONITOR", border_style="blue"))
    return layout

def citadel_loop(loader, profile):
    progress = Progress(SpinnerColumn("dots"), TextColumn("[bold white]{task.fields[status]}"), BarColumn(complete_style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), expand=True)
    task_id = progress.add_task("dl", total=profile.mediacount, status="SCANNING")
    
    with Live(None, refresh_per_second=4, screen=True, transient=True) as live:
        try:
            for post in profile.get_posts():
                while "[bold red]" in get_net_health():
                    engine.log("CONNECTION INTERRUPTED - WAITING...", style="bold red")
                    live.update(make_layout(progress, target=profile.username))
                    time.sleep(5)
                
                if engine.is_downloaded(post.shortcode):
                    engine.stats["skipped"] += 1
                    progress.update(task_id, advance=1)
                    continue
                
                success = False
                backoff = 30
                while not success:
                    try:
                        t1 = time.time()
                        progress.update(task_id, status=f"PULLING: {post.shortcode}")
                        live.update(make_layout(progress, target=profile.username))
                        
                        loader.download_post(post, target=profile.username)
                        engine.stats["latency"] = int((time.time() - t1) * 1000)
                        
                        # JPG/MP4 Only Purge
                        base_path = os.path.join(profile.username, f"{post.date_utc:%Y-%m-%d_%H-%M-%S}_UTC")
                        for ext in [".txt", ".json.xz", ".json"]:
                            if os.path.exists(base_path + ext): os.remove(base_path + ext)
                        
                        engine.mark_done(post.shortcode)
                        engine.log(f"FILE SYNCED: {post.shortcode}", style="bright_green")
                        success = True
                    except Exception as e:
                        if "429" in str(e):
                            engine.log("LIMIT REACHED. BACKING OFF...", style="bold yellow")
                            time.sleep(backoff)
                            backoff *= 2
                        else:
                            engine.stats["errors"] += 1
                            success = True 
                
                time.sleep(abs(random.gauss(4, 1.2)))
                progress.update(task_id, advance=1)
                live.update(make_layout(progress, target=profile.username))

        except KeyboardInterrupt:
            live.stop()
            clean_exit()

if __name__ == "__main__":
    L = instaloader.Instaloader(quiet=True, save_metadata=False, post_metadata_txt_pattern="")
    L.context._session.headers.update({"X-IG-App-ID": "936619743392459"})
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        target = console.input("[bold yellow]CITADEL[/] [white]»[/] [b]TARGET USER:[/b] ")
        prof = instaloader.Profile.from_username(L.context, target)
        citadel_loop(L, prof)
    except KeyboardInterrupt: clean_exit()
    except Exception as e:
        console.print(f"[red]Fatal Error: {e}[/]")
        engine.close_db()