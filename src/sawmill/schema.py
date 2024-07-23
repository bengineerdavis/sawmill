import os
from typing import (
    Dict,
    List,
    TextIO,
    Union,
)

import pandas as pd


# TODO: use the schema to build and manage the different dataframes that will become the
# tables representing the file
class Schema(object):
    """
    This class provides a structured representation of unstructured text (file, string, or stream). It uses regex
    patterns to serialize text data into entries and their corresponding line numbers, and stores them in a
    Pandas DataFrame. The class allows for easy searching and filtering of text data using DataFrame methods
    or SQL-like queries.

    Attributes:
        build_dict (Dict[str, Union[Dict, str, None]]): A dictionary containing the schema for the file
        file_path (Union[str, TextIO, os.PathLike]): A valid pathlike file object or string
        template (Dict): A dictionary containing the schema for the file

    Example:
        schema_template = {
            "session": {
                "pk": "int",
                "file_fk": "int",
                "timestamp": "datetime",
                "command_success": "bool",
                "command_error": "str",
            },
            "file": {
                "pk": "int",
                "file_path": "str",
                "raw_data": "text",
            },
            "entry": {
                "pk": "int",
                "contents": "text",
                "file_fk": "int",
            },
            "line": {
                "pk": "int",
                "contents": "text",
                "entry_fk": "int",
                "file_fk": "int",
            },
        }

        build_dict = {
            # first, add file to table (this can be done automatically by the class)
            # any other columns are for additional data that can be extracted from the
            file
            "file" {
                "metadata": r"(\{.*\})",  # Matches a JSON object
            },
            # second, go through the file again and extract entries
            "entry": {
                "contents": "text",
            },
            # third, go through the file another time and extract lines
            "line": {
                "pk": "int",
                "contents": "text",
                "entry_fk": "int",
                "file_fk": "int",
            },
            # work on this table later?
            "session": {
                "pk": "int",
                "file_fk": "int",
                "timestamp": "datetime",
                "command_success": "bool",
                "command_error": "str",
            },
        }

        my_schema = Schema(file_path, template)



    """

    def __init__(self, file_path, template, build_dict) -> Dict:
        """
        Initializes the RestructuredData object with empty DataFrames for entries and
        data.
        """
        self.build_dict: Dict[str, Union[Dict, str, None]] = build_dict
        self.file_path: Union[str, TextIO, os.PathLike] = file_path
        self.template: Dict = template
        self.tables = []

    @property
    def schema(self) -> pd.DataFrame:
        """
        Lazily loads and returns the entries DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing log entries and their line numbers.
        """
        if self.self._data is None:
            self._schema_dict = self._create_schema(self.file_path, self.entry_pattern)
        return self._data

    def _build(self) -> List[pd.DataFrame]:
        """pass"""

        for table in self.build_dict:
            self._create_table(table)

        return

        # self.file_path: Union[str, TextIO, os.PathLike]

    def _create_table(
        self,
        table_definitions: Dict[str, str],
        file_path: Union[str, TextIO, os.PathLike],
    ) -> pd.DataFrame:
        """Define each dataframe that will represent a table

        Args:
            entries (pd.DataFrame): The DataFrame containing the entries."""
