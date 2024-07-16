from dataclasses import dataclass
from typing import Any


@dataclass
class Table:
    """A class to represent a table and help assemble tabkles in an in-memory
    database."""

    db_path: str
    schema: dict[str, Any] = {}
    table: dict[str, list[Any]] = {}

    def __post_init__(self):
        self.columns = [key for key in self.schema.keys()]
        self._build_attrs(self.columns)

    def build(self):
        """Build the a dictionary representing the table, using the attributes
        representing column names and their accompanying list of values as each key:
        value pair.

        From the schema, also recast the values in the table to the appropriate type, as
        defined in the values of self.schema.

        Returns:
            dict: The dictionary , with all list values appropriately recasted to the
            schema-declared types, to be used as an object assemble a dataframe
        """

        for column in self.columns:
            type_caster = self.schema[column]
            values = [type_caster(value) for value in getattr(self, column)]
            self.table[column] = values

    def _build_attrs(self, attr_names: list[str]):
        """Insert all column names from the schema as attributes to the class instance"""
        for attr in attr_names:
            setattr(self, attr, [])
