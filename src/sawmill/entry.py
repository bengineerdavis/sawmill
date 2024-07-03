from typing import Dict, List
import logging


logger = logging.getLogger(__name__)


class Line:
    def __init__(self, file_id):
        self.file_id: int = file_id

    def update(
        self,
        id: int,
        content: str,
        entry_id: int,
        lines: Dict[str, List[str]],
    ) -> Dict[str, str]:
        lines["id"].append(id)
        lines["line"].append(content)
        lines["entry_id"].append(entry_id)
        lines["file_id"].append(self.file_id)

        return lines


class Entry:
    """An entry in a log file.

    Attributes:
        id: The id of the entry.
        file_id: The id of the file the entry belongs to.
    """

    def __init__(self, file_id):
        self.id: int = 0
        self.lines: List[str] = []
        self._line_numbers: List[int] = []
        self.file_id: int = file_id

    def add(self, line: str, line_number: int) -> None:
        self._line_numbers.append(line_number)
        self.lines.append(line)

    def update(self, entries: Dict[str, str]) -> Dict[str, str]:
        entries["id"].append(self.id)
        
        self._entry = "".join(self.lines)
        entries["entry"].append(self._entry)

        entries["line_numbers"].append(self._line_numbers)

        entries["file_id"].append(self.file_id)

        self.id += 1
        return entries

    def flush(self) -> None:
        self.lines = []
        self._line_numbers = []
        self._entry = ""
