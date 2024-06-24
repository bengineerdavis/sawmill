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

import pandas as pd


# TODO: move functions below into this class in it's public instance methods
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

    def __init__(self):
        """
        Initializes the RestructuredData object with empty DataFrames for entries and data.
        """
        self.entry_pattern: LiteralString = "^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        self.column_patterns = (
            {
                "date": r"(\d{4}-\d{2}-\d{2})",  # Matches a date in the format YYYY-MM-DD
                "time": r"(\d{2}:\d{2}:\d{2})",  # Matches a time in the format HH:MM:SS
                "category": r"(?<=\d{2}:\d{2}:\d{2}\s)(\w+)",  # Matches any one word after a timestamp (see 'date' and 'time' patterns above)
                "message": r"(.+)",  # Matches one or more of any character
            },
        )
        self.file_path: Union[str, TextIO, os.PathLike]

       self._entries = "None"  # Placeholder for lazy loading

    @property
    def entries(self) -> pd.DataFrame:
        """
        Lazily loads and returns the entries DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing log entries and their line numbers.
        """
        if self._entries is None:
            self._entries = self._extract_entries(self.file_path, self.entry_pattern)
        return self._entries

    def _extract_entries(
        self,
        file_path: Union[str, TextIO, os.PathLike],
        entry_pattern: LiteralString = None,
    ) -> pd.DataFrame:
        r"""
        Reads in unstructured data and returns a DataFrame with all entries and their line numbers extracted into their own rows, via regex patterns.

        Args:
            file_path (str, bytes, os.PathLike): A valid pathlike file object or string
            entry_pattern (LiteralString): A valid regex pattern

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
            ...     records = restructured._entries.to_dict(orient="records")

            >>> records[0] == {'entry': '2024-03-20 23:12:33 platform > readFromDestination: start\n', 'line_numbers': [0]}
            >>> records[1] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release\n', 'line_numbers': [1]}
            >>> records[2] == {'entry': '2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS\n', 'line_numbers': [2]}
            >>> records[3] == {'entry': '2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:\n\tconverter.type = key\n\tdecimal.format = BASE64\n\treplace.null.with.default = true\n\tschemas.cache.size = 1000\n\tschemas.enable = false\n', 'line_numbers': [3, 4, 5, 6, 7, 8]}
            >>> records[4] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release', 'line_numbers': [9]}
        """

        # Initialize lists to hold log entries and their corresponding line numbers.
        entries = []
        line_indices = []


        # Compile the regex pattern for identifying the start of log entries.
        pattern = re.compile(entry_pattern, re.MULTILINE)

        # Open the file and read through it line by line.
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file):
                # Check if the line matches the entry pattern, indicating a new log entry.
                if pattern.match(line):
                    # If the current log entry list is not empty, it means the previous entry is complete.
                    if entry_lines:
                        # Save the collected lines and their indices.
                        entries.append("".join(entry_lines))
                        line_indices.append(indices)
                        # Reset the lists for the next log entry.
                        entry_lines = []
                        indices = []
                    # Add the current line to the new log entry.
                    entry_lines.append(line)
                    indices.append(line_number)
                else:
                    # If the line does not match the pattern, it continues the current log entry.
                    entry_lines.append(line)
                    indices.append(line_number)

            # After the last line is processed, check if there is an unfinished log entry to save.
            if entry_lines:
                entries.append("".join(entry_lines))
                line_indices.append(indices)

        # Create a DataFrame from the collected log entries and their line numbers.
        entries = pd.DataFrame({"entry": entries, "line_numbers": line_indices})

        return entries

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

    def read(self, extract_from="entry") -> pd.DataFrame:
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

        self._extracted_entries = self._extract_entries(
            file_path=self.file_path,
            entry_pattern=self.entry_pattern,
        )
        self._raw_entries = self._extracted_entries[extract_from]

        # Create an empty DataFrame to store the extracted metadata
        self.data = pd.DataFrame()

        # Iterate over the column patterns, create the new column, and extract the matching metadata
        for column_name, pattern in self.column_patterns.items():
            self.data[column_name] = self._extract_metadata_columns(
                self._raw_entries, pattern
            )

        return self.data
