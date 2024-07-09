# src/sawmill/tui.py
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

console = Console()

class ScrollableLogViewer:
    def __init__(self, logs: pd.DataFrame):
        self.logs = logs
        self.current_start = 0
        self.page_size = 10
        self.total_lines = len(logs)

    def display_logs(self):
        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL)
        table.add_column("Timestamp", style="dim", width=20)
        
        # make sure all columns are included by default
        for col in self.logs.columns.tolist():
            if col != "timestamp":
                table.add_column(col.capitalize())
        
        # table.add_column("Level")
        # table.add_column("Message")

        end = min(self.current_start + self.page_size, self.total_lines)
        log_level_column_name = "log_status"
        for _, row in self.logs.iloc[self.current_start:end].iterrows():
            level_style = "green" if row[log_level_column_name] == "INFO" else "red"
            table.add_row(
                row['id'],
                row['timestamp'],
                row['entry'], 
                row['line_numbers'],
                Text(row[log_level_column_name], 
                style=level_style), 
                row['component'],
            )
        
        return table

    def scroll_up(self):
        if self.current_start > 0:
            self.current_start -= self.page_size

    def scroll_down(self):
        if self.current_start + self.page_size < self.total_lines:
            self.current_start += self.page_size

# def load_logs() -> pd.DataFrame:
#     # Placeholder log data, replace with actual log loading
#     logs = pd.DataFrame({
#         "timestamp": ["2023-07-08 12:34:56", "2023-07-08 12:35:56", "2023-07-08 12:36:56", "2023-07-08 12:37:56",
#                       "2023-07-08 12:38:56", "2023-07-08 12:39:56", "2023-07-08 12:40:56", "2023-07-08 12:41:56",
#                       "2023-07-08 12:42:56", "2023-07-08 12:43:56", "2023-07-08 12:44:56", "2023-07-08 12:45:56"],
#         "level": ["INFO", "ERROR", "INFO", "ERROR", "INFO", "ERROR", "INFO", "ERROR", "INFO", "ERROR", "INFO", "ERROR"],
#         "message": ["Log message 1", "Log message 2", "Log message 3", "Log message 4", "Log message 5",
#                     "Log message 6", "Log message 7", "Log message 8", "Log message 9", "Log message 10",
#                     "Log message 11", "Log message 12"]
#     })
#     return logs

def live_logs(logs: pd.DataFrame):
    # logs = load_logs()
    viewer = ScrollableLogViewer(logs)
    with Live(console=console, refresh_per_second=4, screen=True) as live:
        while True:
            table = viewer.display_logs()
            live.update(Panel(Align.center(table), title="Sawmill Log Viewer", border_style="green"))
            key = console.input()
            if key == "q":
                break
            elif key == "j":
                viewer.scroll_down()
            elif key == "k":
                viewer.scroll_up()
