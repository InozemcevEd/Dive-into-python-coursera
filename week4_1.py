import os
import tempfile


class File:
    def __init__(self, path):
        self.path = path
        self.current_position = 0

        if not os.path.exists(self.path):
            open(self.path, 'w+')

    def write(self, line):
        with open(self.path, 'w+') as f:
            return f.write(line)

    def read(self):
        with open(self.path, 'r+') as f:
            return f.read()

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), 'new_file.txt')
        new_file = File(new_path)
        new_file.write(self.read() + other.read())
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)

            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration('EOF')

            self.current_position = f.tell()
            return line

    def __str__(self):
        return '{}'.format(self.path)

