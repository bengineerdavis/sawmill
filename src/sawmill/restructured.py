"""
This module provides a function to serialize unstructured text-based data files into a Pandas DataFrame using regex patterns.

Example usage:
    from pathlib import Path

    # file contents: '2024-03-20 23:12:33 platform > readFromDestination: start'
    file_data = Path('.') / 'file_data.txt'

    results = restructure_data(
        file_path=file_data,
    )

    results

    # contents should now be organized into a Pandas DataFrame
    '''entry	line_numbers
    0	2024-03-20 23:12:33 platform > readFromDestina...	[0]'''
"""

import os
import re
from typing import (
    Dict,
    List,
    LiteralString,
    TextIO,
    Union,
)
from pathlib import Path
import json
import textwrap

import pandas as pd

from .entry import Entry, Line

import logging
import duckdb


logger = logging.getLogger(__name__)


class RestructuredData(object):
    """
    This class provides a structured representation of unstructured text (file, string, or stream). It uses regex
    patterns to serialize text data into entries and their corresponding line numbers, and stores them in a
    Pandas DataFrame. The class allows for easy searching and filtering of text data using DataFrame methods
    or SQL-like queries.

    Attributes:
        entry_pattern (LiteralString): A valid regex pattern to identify the start of a new log entry.
        file_path (Union[str, TextIO, os.PathLike]): A valid pathlike file object or string
        column_patterns (Dict[str,str]): A dictionary of key-value pairs representing 'column_name': 'regex pattern'
        _entries (pd.DataFrame): DataFrame that stores raw entries and their line numbers.
        data (pd.DataFrame): DataFrame that stores extracted metadata from each entry, along with related raw entry.
    """

    def __init__(self, file_path, file_id=0):
        """
        Initializes the RestructuredData object with empty DataFrames for entries and data.
        """
        self.entry_pattern: LiteralString = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        self.column_patterns = {
                "date": r"(\d{4}-\d{2}-\d{2})",  # Matches a date in the format YYYY-MM-DD
                "time": r"(\d{2}:\d{2}:\d{2})",  # Matches a time in the format HH:MM:SS
                "log_status": r"\b(INFO|WARN|ERROR|DEBUG|TRACE|NOTICE)\b", # Matches on INFO|WARN|ERROR|DEBUG|TRACE|NOTICE messages
                "component": r"(?<=\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s)(?!INFO|WARN|ERROR|DEBUG\b)(\w+)(?=\s*>)",  # Matches any one word after a timestamp that is not INFO, WARN, ERROR, DEBUG
                # "message": r"(.+)",  # Matches one or more of any character
        }
        self.file_path: Union[str, TextIO, os.PathLike] = Path(file_path)
        self.file_id = file_id
        self._data: List[pd.DataFrame] | None = None
        self.entries = {
            "id": [],
            "entry": [],
            "line_numbers": [],
            "file_id": [],
        }
        self.lines = {
            "id": [],
            "line": [],
            "entry_id": [],
            "file_id": [],
        }
        self.file = {
            "id": [self.file_id],  # List[int]
            "path": [self.file_path],
            "name": [self.file_path.name],
            "contents": [self._write_contents()],
        }

    def _extract(self) -> pd.DataFrame:
        r"""
        Reads in unstructured data and returns a DataFrame with all entries and their line numbers extracted into their own rows, via regex patterns.

        Returns:
            pd.DataFrame: A DataFrame (spreadsheet-like, 2d data object) containing entries and their line numbers.

        Raises:

        Examples:
            >>> import tempfile
            >>> from pathlib import Path

            >>> file_contents = '''2024-03-20 23:12:33 platform > readFromDestination: start
            ... 2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release
            ... 2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS
            ... 2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:
            ... \tconverter.type = key
            ... \tdecimal.format = BASE64
            ... \treplace.null.with.default = true
            ... \tschemas.cache.size = 1000
            ... \tschemas.enable = false
            ... 2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release'''

            >>> # now we're ready to simulate data in a tempfile
            >>> unstructure_data = tempfile.NamedTemporaryFile()
            >>> with open(unstructure_data.name, "w") as ud:
            ...     # prepare text to be written to the temporary file
            ...     split_marker = "<split>"
            ...     insert_whitespace = file_contents.replace("\n", f"\n{split_marker}")
            ...     lines = insert_whitespace.split(split_marker)
            ...
            ...     # write lines to the temporary file
            ...     ud.writelines(lines)

            ...     restructured = RestructuredFileData(file_path = Path(ud))
            ...     records = restructured.data.to_dict(orient="records")

            ...      records[0] == {'entry': '2024-03-20 23:12:33 platform > readFromDestination: start\n', 'line_numbers': [0]}
            ...      records[1] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release\n', 'line_numbers': [1]}
            ...      records[2] == {'entry': '2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS\n', 'line_numbers': [2]}
            ...      records[3] == {'entry': '2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:\n\tconverter.type = key\n\tdecimal.format = BASE64\n\treplace.null.with.default = true\n\tschemas.cache.size = 1000\n\tschemas.enable = false\n', 'line_numbers': [3, 4, 5, 6, 7, 8]}
            ...      records[4] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release', 'line_numbers': [9]}
        """

        # Compile the regex pattern for identifying the start of log entries.
        pattern = re.compile(self.entry_pattern, re.MULTILINE)

        # Open the file and read through it line by line.
        with open(self.file_path, "r") as file:
            entry = Entry(file_id=self.file_id)
            lines = Line(file_id=self.file_id)
            for index, line in enumerate(file):
                logger.debug(f"Processing line {index}: {line}")
                logger.debug(f"Processing entries dict:\n\n{self.entries}\n\n")
                
                self.lines = lines.update(id=index, content=line, entry_id=entry.id, lines=self.lines)
                # Check if the line matches the entry pattern, indicating a new log entry.
                if pattern.match(line):
                    # If the current log entry list is not empty, it means the previous entry is complete.
                    if entry.lines:
                        # Save the collected lines and their indices.
                        self.entries = entry.update(entries=self.entries)
                        # Reset the lists for the next log entry.
                        entry.flush()
                    # Add the current line to the new log entry.
                    entry.add(line=line, line_number=index)
                else:
                    # If the line does not match the pattern, it continues the current log entry.
                    entry.add(line=line, line_number=index)
                    # breakpoint()

            # After the last line is processed, check if there is an unfinished log entry to save.
            if len(entry.lines) > 0:
                self.lines = lines.update(id=index, content=line, entry_id=entry.id, lines=self.lines)
                self.entries = entry.update(entries=self.entries)
            
    def _write_contents(self) -> str:

        with open(self.file_path, "r") as file:
            contents = file.read()

        return contents

    # helper function
    def _extract_metadata_columns(
        self, entries: pd.DataFrame, data_pattern: str
    ) -> List[Dict]:
        """
        Helper function Extracts column data from a DataFrame based on a given data pattern.

        Args:
            entries (pd.DataFrame): The DataFrame containing the entries.
            data_pattern (str): The regex pattern used to extract the value for the current column.

        Returns:
            List: A list of extracted values for the current column. If no match is found, None is appended.
        """

        # Create an empty list to store the extracted values for the current column
        extracted_values = []

        # Iterate over the entries in the DataFrame
        for entry in entries:
            # Use regex pattern to extract the value for the current column
            match = re.search(data_pattern, entry)
            if match:
                extracted_values.append(match.group(1))
            else:
                extracted_values.append(None)

        return extracted_values

    def read(self, extract_from="entry"):
        r"""
        Extracts metadata from each row's complex string in an 'entries' DataFrame and creates a new DataFrame with the extracted metadata
        inserted into each related row in the new DataFrame.

        Returns:
            A new Pandas DataFrame with the extracted metadata as separate rows

        Raises:

        Examples:
            >>> import tempfile
            >>> from pathlib import Path

            >>> file_contents = '''2024-03-20 23:12:33 platform > readFromDestination: start
            ... 2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release
            ... 2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS
            ... 2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:
            ... \tconverter.type = key
            ... \tdecimal.format = BASE64
            ... \treplace.null.with.default = true
            ... \tschemas.cache.size = 1000
            ... \tschemas.enable = false
            ... 2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release'''

            >>> # now we're ready to simulate data in a tempfile
            >>> unstructure_data = tempfile.NamedTemporaryFile()

            >>> with open(unstructure_data.name, "w") as ud:
            ...     # prepare text to be written to the temporary file
            ...     split_marker = "<split>"
            ...     insert_whitespace = file_contents.replace("\n", f"\n{split_marker}")
            ...     lines = insert_whitespace.split(split_marker)
            ...
            ...     # write lines to the temporary file
            ...     ud.writelines(lines)

            ...     restructured = RestructuredFileData(file_path = Path(ud))
            ...     result = restructured.read()

            ...     # update DataFrame display settings for better readability
            ...     pd.set_option('display.max_columns', 5)
            ...     pd.set_option('display.width', 100)
            ...     result
                    date	    time	    category	                                      message
            0	2024-03-20	23:12:33	platform	2024-03-20 23:12:33 platform > readFromDestina...
            1	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > WARN StatusC...
            2	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > 2024-03-20 2...
            3	2024-03-09	11:03:43	source	2024-03-09 11:03:43 source > INFO main o.a.k.c...
            4	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > WARN StatusC...
        """
       
        # Extract the raw entries from the unstructured data
        self._extract()

        # Isolate the the raw text column for each extracted entry
        self._raw_entries = self.entries[extract_from]

        # Create an empty DataFrame to store the extracted metadata
        self.data = {}
        self.data["entries"] = pd.DataFrame(self.entries)
        self.data["lines"] = pd.DataFrame(self.lines)
        self.data["file"] = pd.DataFrame(self.file)
        
        # Iterate over the column patterns, create the new column, and extract the matching metadata
        for column_name, pattern in self.column_patterns.items():
            self.data["entries"][column_name] = self._extract_metadata_columns(
            self._raw_entries, pattern
            )
        
        # TODO refactor things like local data caching to the user directory
        # TODO: add rules about purging old data
        # TODO: move app-level config to a separate config file and corresponding config object 
        local_data_root_dir = Path(__name__).parent.parent.parent / "data"
        cache_dir = local_data_root_dir / Path(self.file_path).name
        cache_dir.mkdir(exist_ok=True, parents=True)
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H:%M:%S")
        for tablename, records in self.data.items():
            logger.debug(f"Table: {tablename}")
            logger.debug(f"Records: {records}")
            records.to_json(
                f"{cache_dir / tablename}_{timestamp}.json", 
                orient="records", 
                date_format="iso",
                default_handler=str,
                index=False,
                )
        
        return self.data


    def search(self, query) -> str:
        # grab data from the tables
        schema = self.read()
        tables = [tablename for tablename in schema.keys()]

        # import the tables
        df_entries, df_lines, df_file = [df for df in schema.values()]
        
        # try improve the table formatting output for the user
        df_entries['entry'].str.wrap(100)
        pd.set_option('display.max_colwidth', 400)
        pd.set_option('display.width', 800)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        # Print the query result
        results = duckdb.query(query).to_df()
    
        print(results)
        
        
