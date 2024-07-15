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


@app.command()
def parse(file_path: str):
    """
    Parse the file and convert it to a DataFrame.
    """
    # Ingest data from the file
    restructured_file = RestructuredData(file_path=file_path)
    return restructured_file.data


@app.command()
def query(dataframe, extract: str = None, filter: list = None):
    """
    Apply extraction, filtering, and transformation to the DataFrame.
    """
    df_query = DataFrameQuery(dataframe)

    if extract:
        dataframe = df_query.extract_data(extract)

    if filter:
        for f in filter:
            dataframe = df_query.filter_data(f)

    return dataframe


@app.command()
def view(dataframe, format: str):
    """
    Create views for the data.
    """
    df_viewer = DataFrameViewer(dataframe)
    return df_viewer.create_view(format)


@app.command()
def export(dataframe, format: str, as_type: str, to: str):
    """
    Export the view to the specified format.
    """
    df_exporter = DataFrameExporter(dataframe)

    if as_type == "file":
        if format == "csv":
            df_exporter.to_csv(to)
        elif format == "json":
            df_exporter.to_json(to)
        # Add more formats as needed
    elif as_type == "git":
        df_exporter.to_git(to)
    elif as_type == "web":
        df_exporter.to_web(to)
    elif as_type == "zip":
        df_exporter.to_zip(to)


def main():
    app()


if __name__ == "__main__":
    main()
