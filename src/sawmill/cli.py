import typer

from .restructured import RestructuredData

# from io import TextIO
import os
from typing import Union, TextIO

app = typer.Typer()

@app.command()
def read(file_path: str):
    """Convert an unstructured text file into csv-like (columns, rows) output
    
    Example:
        pass"""

    restructured_file = RestructuredData(file_path=file_path)
    data = restructured_file.read()

    print(data)


def main():
    app()
    

if __name__ == "__main__":
    main()