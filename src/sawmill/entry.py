from typing import Dict, List


class Line:
    def __init__(self, content, entry_id, file_id):
        self.content: str = content
        self.entry_id: int = entry_id
        self.file_id: int = file_id

    def update(
        self,
        id: int,
        lines: Dict[str, List[str]],
    ) -> Dict[str, str]:
        lines["id"].append(id)
        lines["content"].append(self.content)
        lines["entry_id"].append(self.entry_id)
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
        self._lines: List[str] = []
        self._line_numbers: List[int] = []
        self.file_id: int = file_id

    def add(self, line: str, line_number: int) -> None:
        self.line_numbers.append(line_number)
        self._lines.append(line)

    def update(self, entries: Dict[str, str]) -> Dict[str, str]:
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
