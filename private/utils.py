import re
import os

class InputValidator:
    def __init__(self):
        self.assignment_pattern = re.compile(r'^[a-zA-Z0-9+\-*/** ]+$')

    def is_valid_assignment(self, assignment_string):
        if not assignment_string:
            print("Assignment cannot be empty")
            return False
        elif not self.assignment_pattern.match(assignment_string):
            print("Invalid assignment")
            return False
        else:
            return True
        
    def is_valid_filename(self, filename):
        if not filename:
            print("Filename cannot be empty")
            return False

        if not os.path.basename(filename) == filename:
            print("File cannot be fun")
            return False

        if '.' not in filename:
            filename += '.txt'

        return True