# src/sawmill/tui.py
import pandas as pd
from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

console = Console()


class ScrollableLogViewer:
    def __init__(self, logs: pd.DataFrame):
        self.logs = logs.astype(str)
        self.current_start = 0
        self.page_size = 100
        self.total_lines = len(logs)

    def display_logs(self):
        # pre-cast into a string type to use with rich's Table API
        # self.logs["id"] = self.logs["id"].astype(str)
        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL)
        columns = [
            "date",
            "time",
            "entry",
            "line_numbers",
            "log_status",
            "component",
        ]
        # table.add_column("Timestamp", style="dim", width=20)

        # make sure all columns are included by default
        for col in columns:
            table.add_column(col.capitalize())

        # table.add_column("Level")
        # table.add_column("Message")

        end = min(self.current_start + self.page_size, self.total_lines)
        log_level_column_name = "log_status"
        for _, row in self.logs.iloc[self.current_start : end].iterrows():
            level_style = "green" if row[log_level_column_name] == "INFO" else "red"
            table.add_row(
                row["date"],
                row["time"],
                row["entry"],
                row["line_numbers"],
                Text(row[log_level_column_name], style=level_style),
                row["component"],
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
    viewer = ScrollableLogViewer(logs)
    table = viewer.display_logs()
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            live.update(table)
            key = console.input()
            if key == "q":
                False
            elif key == "j":
                viewer.scroll_down()
            elif key == "k":
                viewer.scroll_up()
