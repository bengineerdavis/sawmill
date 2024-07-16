# src/sawmill/tui.py
from typing import Dict

import pandas as pd
from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


class LogViewer:
    def __init__(self, logs: pd.DataFrame, table_kwargs, columns=None):
        self.logs = logs.astype(str)
        self.table_kwargs: Dict = table_kwargs
        # TODO: Purge any unnecessary commented-out lines from this file and class
        # self.title = "Log_Results" if table_kwargs["title"] is None else table_kwargs["title"]
        self.columns = (
            [col for col in self.logs.columns.tolist()] if columns is None else columns
        )

    def display_logs(self):

        table = Table(**self.table_kwargs)

        # make sure all columns are included by default
        for col in self.columns:
            table.add_column(col.capitalize())

        log_level_column_name = "log_status"
        for _, row in self.logs.iterrows():
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

columns = [
    "date",
    "time",
    "entry",
    "line_numbers",
    "log_status",
    "component",
]
table_kwargs = dict(
    # title="Logs",
    show_header=True,
    header_style="bold magenta",
    box=box.MINIMAL,
)


def live_logs(logs: pd.DataFrame, columns=columns, table_kwargs=table_kwargs):
    viewer = LogViewer(logs, table_kwargs=table_kwargs, columns=columns)
    table = viewer.display_logs()
    with Live(console=console, refresh_per_second=4) as live:
        live.update(
            Panel(Align.center(table), title="Sawmill Log Viewer", border_style="green")
        )
