import logging
from pathlib import Path

# from io import TextIO
from typing import Union

import typer

from .restructured import RestructuredData
from .tui import live_logs

logging.basicConfig(level=logging.INFO)
root = logging.getLogger()
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def find(file_path: str, query: str):
    """Convert an unstructured text file into csv-like (columns, rows) output

    Example:
        pass"""

    # ingest data from the file
    restructured_file = RestructuredData(file_path=file_path)

    # print to the terminal the results for the user
    if Path(query).is_file():
        with open(query, "r") as f:
            query_from_file = f.read()
            restructured_file.search(query_from_file)
    else:
        restructured_file.search(query)


@app.command()
def view(file_path: str, query: Union[str, None] = None):
    # ingest data from the file
    restructured_file = RestructuredData(file_path=file_path)
    logs = restructured_file.search(query)

    live_logs(logs=logs)


def main():
    app()


if __name__ == "__main__":
    main()
