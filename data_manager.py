import json
import os

STUDENTS_FILE = 'students.data' # Refer to this from now on. STUDENTS_FILE. If you type in something else I will break your goddamn legs.

def read_data(filename=STUDENTS_FILE):

    if not os.path.exists(filename):
        # Create an empty list in the file if it's new
        with open(filename, 'w') as f:
            json.dump([], f)
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle case where file is empty or corrupted
        return []

def write_data(data, filename=STUDENTS_FILE):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)