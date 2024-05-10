


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

import re
import pandas as pd
from pandas import DataFrame
import tempfile
import pathlib
import os

from typing import (
    Dict,
    Union,
    LiteralString,
    TextIO,
    List,
)


# TODO: move functions below into this class in it's public instance methods
class RestructuredData(object):
    """
    This class provides a structured representation of unstructured text (file, string, or stream). It uses regex
    patterns to serialize text data into entries and their corresponding line numbers, and stores them in a 
    Pandas DataFrame. The class allows for easy searching and filtering of text data using DataFrame methods
    or SQL-like queries.

    Attributes:
        entries (pd.DataFrame): DataFrame that stores raw entries and their line numbers.
        data (pd.DataFrame): DataFrame that stores extracted metadata from each entry, along with related raw entry.
    """

    def __init__(self):
        """
        Initializes the RestructuredData object with empty DataFrames for entries and data.
        """
        self.entries = pd.DataFrame()
        self.data = pd.DataFrame()

    def _extract_entries(self):
        """
        A helper method to extract entries and their line numbers from unstructured data. 
        This method populates the 'entries' DataFrame.

        Returns:
            None: This method does not return any value but modifies the 'entries' attribute.
        """
        pass
    
    def read_unstructured(self):
        """
        Reads in unstructured data and returns a DataFrame with all entries and their line numbers extracted into their own rows.

        Returns:
            pd.DataFrame: A DataFrame containing entries and their line numbers.
        """
        return self.entries

    def extract_columns(self, entries: pd.DataFrame = None):
        """
        Extracts metadata from each row's complex string in the 'entries' DataFrame and creates a new DataFrame with the
        extracted metadata inserted into each related row in the new DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing extracted metadata related to each entry.
        """
        return self.data


def read_unstructured(file_path: Union[str, TextIO, os.PathLike], entry_pattern: LiteralString = "^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})") -> pd.DataFrame:
    r"""
    Serializes unstructured text-based data files into a Pandas DataFrame (columns, rows) using regex patterns

    Args:
        file_path (str, bytes, os.PathLike): A valid pathlike file object or string
        entry_pattern (LiteralString): A valid regex pattern

    Returns:
        A Pandas DataFrame (spreadsheet-like, 2d data object)

    Raises:

    Examples:
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
        >>> results = read_unstructured(
        ...    file_path = unstructure_data.name,
        ...    )

        >>> records = results.to_dict(orient="records")

        >>> records[0] == {'entry': '2024-03-20 23:12:33 platform > readFromDestination: start\n', 'line_numbers': [0]}
        >>> records[1] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release\n', 'line_numbers': [1]}
        >>> records[2] == {'entry': '2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS\n', 'line_numbers': [2]}
        >>> records[3] == {'entry': '2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:\n\tconverter.type = key\n\tdecimal.format = BASE64\n\treplace.null.with.default = true\n\tschemas.cache.size = 1000\n\tschemas.enable = false\n', 'line_numbers': [3, 4, 5, 6, 7, 8]}
        >>> records[4] == {'entry': '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release', 'line_numbers': [9]}

    """
    # Initialize lists to hold log entries and their corresponding line numbers.
    entries = []
    line_indices = []

    # Temporary lists to accumulate lines and indices for the current log entry.
    entry_lines = []
    indices = []

    # Compile the regex pattern for identifying the start of log entries.
    pattern = re.compile(entry_pattern, re.MULTILINE)

    # Open the file and read through it line by line.
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file):
            # Check if the line matches the entry pattern, indicating a new log entry.
            if pattern.match(line):
                # If the current log entry list is not empty, it means the previous entry is complete.
                if entry_lines:
                    # Save the collected lines and their indices.
                    entries.append(''.join(entry_lines))
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
            entries.append(''.join(entry_lines))
            line_indices.append(indices)

    # Create a DataFrame from the collected log entries and their line numbers.
    structured_data = {"entry": entries, "line_numbers": line_indices}
    return pd.DataFrame(structured_data)


def _extract_column_data(entries: pd.DataFrame, data_pattern: str) -> List:
    """
    Extracts column data from a DataFrame based on a given data pattern.

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

def extract_columns(entries_df: pd.DataFrame, extract_from_column: str, column_patterns: Dict[str, str]) -> pd.DataFrame:
    r"""
    Extracts metadata from each row's complex string in an 'entries' DataFrame and creates a new DataFrame with the extracted metadata
    inserted into each related row in the new DataFrame.

    Args:
        entries_df (pd.DataFrame): The DataFrame containing the entries with complex strings
        extract_from_column: name of the column from which to extract the metadata for each new column defined in 'column_patterns'
        column_patterns (Dict[str, str]): A dictionary of key-value pairs representing 'column_name': 'regex pattern'

    Returns:
        A new Pandas DataFrame with the extracted metadata as separate rows

    Raises:

    Examples:
        >>> column_patterns = {
        ...     'date': r'(\d{4}-\d{2}-\d{2})',  # Matches a date in the format YYYY-MM-DD
        ...     'time': r'(\d{2}:\d{2}:\d{2})',  # Matches a time in the format HH:MM:SS
        ...     'category': r'(?<=\d{2}:\d{2}:\d{2}\s)(\w+)',  # Matches any one word after a timestamp (see 'date' and 'time' patterns above)
        ...     'message': r'(.+)',  # Matches one or more of any character
        ... }
        >>> entries = {
        ...     'entry': [
        ...         '2024-03-20 23:12:33 platform > readFromDestination: start',
        ...         '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release',
        ...         '2024-03-20 23:12:36 destination > 2024-03-20 23:12:36 INFO i.a.c.i.b.a.AdaptiveDestinationRunner$Runner(getDestination):75 - Running destination under deployment mode: OSS',
        ...         '2024-03-09 11:03:43 source > INFO main o.a.k.c.c.AbstractConfig(logAll):369 JsonConverterConfig values:\n\tconverter.type = key\n\tdecimal.format = BASE64\n\treplace.null.with.default = true\n\tschemas.cache.size = 1000\n\tschemas.enable = false',
        ...         '2024-03-20 23:12:36 destination > WARN StatusConsoleListener The use of package scanning to locate plugins is deprecated and will be removed in a future release'
        ...     ],
        ...     'line_numbers': [
        ...         [0],
        ...         [1],
        ...         [2],
        ...         [3, 4, 5, 6, 7, 8],
        ...         [9]
        ...     ]
        ... }

        >>> # create example DataFrame and then extract the metadata using the column patterns
        >>> entries_df = pd.DataFrame(entries)
        >>> extract_from = 'entry'
        >>> result = extract_columns(entries_df, extract_from, column_patterns)
    
        >>> # update DataFrame display settings for better readability
        >>> pd.set_option('display.max_columns', 5)
        >>> pd.set_option('display.width', 100)
        >>> result
                  date	    time	    category	                                      message
        0	2024-03-20	23:12:33	platform	2024-03-20 23:12:33 platform > readFromDestina...
        1	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > WARN StatusC...
        2	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > 2024-03-20 2...
        3	2024-03-09	11:03:43	source	2024-03-09 11:03:43 source > INFO main o.a.k.c...
        4	2024-03-20	23:12:36	destination	2024-03-20 23:12:36 destination > WARN StatusC...
    """
    # Create an empty DataFrame to store the extracted metadata
    extracted_df = pd.DataFrame()
    
    # Iterate over the column patterns, create the new column, and extract the matching metadata
    entries = entries_df[extract_from_column]
    for column_name, pattern in column_patterns.items():
        extracted_values = _extract_column_data(entries, pattern)
        extracted_df[column_name] = extracted_values
    
    return extracted_df

