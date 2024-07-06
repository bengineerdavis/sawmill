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

# build_dict = {
#     "session": {
#         "date": r"(\d{4}-\d{2}-\d{2})",  # Matches a date in the format YYYY-MM-DD
#         "time": r"(\d{2}:\d{2}:\d{2})",  # Matches a time in the format HH:MM:SS
#         "category": r"(?<=\d{2}:\d{2}:\d{2}\s)(\w+)",  # Matches any one word after a timestamp (see 'date' and 'time' patterns above)
#         "entry": r"(.+)",  # Matches one or more of any character
#     },
#     "table2": {
#         "date": r"(\d{4}-\d{2}-\d{2})",  # Matches a date in the format YYYY-MM-DD
#         "time": r"(\d{2}:\d{2}:\d{2})",  # Matches a time in the format HH:MM:SS
#         "category": r"(?<=\d{2}:\d{2}:\d{2}\s)(\w+)",  # Matches any one word after a timestamp (see 'date' and 'time' patterns above)
#         "entry": r"(.+)",  # Matches one or more of any character
#     },
# }
