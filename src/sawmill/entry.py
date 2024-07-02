from typing import Dict, List

"""
"""


class Line:
    def __init__(self, content, entry_id, file_id):
        self.content: str = content
        self.entry_id: int = entry_id
        self.file_id: int = file_id

    def update(
        self,
        id: int,
        lines: Dict[str : List[str]],
    ) -> Dict[str:str]:
        lines["id"].append(id)
        lines["content"].append(content)
        lines["entry_id"].append(self.entry_id)
        lines["file_id"].append(self.file_id)

        return lines


class Entry:
    """An entry in a log file.

    Attributes:
        entry (str): The name of the entry.
        lines (Dict[int:str]): A dictionary of line numbers and their contents.
        index (Dict[str:int]): A dictionary of line contents and their line numbers.

    Example:
        entry = Entry()
        entry.entry.insert("line1, line1_index")
        entry.lines = {1: "line1", 2: "line2"}
    """

    def __init__(self, file_id):
        self.id: int = 0
        self._lines: List[str] = []
        self._line_numbers: List[int] = []
        self.file_id: int = file_id

    def add(self, line: str, line_number: int) -> None:
        self.line_numbers.append(line_number)
        self._lines.append(line)

    def update(self, entries: Dict[str:str]) -> Dict[str:str]:
        entries["id"].append(self.id)

        entry = "".join(self._lines)
        entries["entry"].append(entry)

        entries["line_numbers"].append(self.line_numbers)

        entries["file_id"].append(self.file_id)

        self.id += 1
        return entries

    def flush(self) -> None:
        self._lines.clear()
        self.line_numbers.clear()


# TODO: Add a RawFile class that will handle the raw log file and entries.
# class RawFile:
#     def __init__(self):
#         self.id: int = {}

#     def add(self, entry: str, line: str) -> None:
#         if entry not in self.entries:
#             self.entries[entry] = Entry()
#         self.entries[entry].add(line)

#     def flush(self) -> None:
#         for entry in self.entries.values():
#             entry.flush()
