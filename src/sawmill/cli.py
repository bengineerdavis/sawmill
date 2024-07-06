import typer

from .restructured import RestructuredData

# from io import TextIO
import logging
from pathlib import Path

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


def main():
    app()
    

if __name__ == "__main__":
    main()