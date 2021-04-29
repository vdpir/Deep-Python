import tempfile
import os
import random


class File:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            f = open(self.file_path, 'w')
            f.close()
        self.f = open(self.file_path, 'r')

    def read(self):
        try:
            with open(self.file_path) as f:
                return f.read()
        except IOError:
            return ""

    def write(self, string_to_write):
        try:
            with open(self.file_path, 'w') as f:
                return f.write(string_to_write)
        except IOError:
            return ""

    def __add__(self, obj):
        string_from_file_obj = obj.read()
        string_from_this_file = self.read()
        target_path = os.path.join(tempfile.gettempdir(), str(random.randint(10000,100000)))
        new_file = File(target_path)
        new_file.write(string_from_file_obj+string_from_this_file)
        return new_file

    def __str__(self):
        return '{}'.format(self.file_path)

    def __iter__(self):
        self.ff = open(self.file_path, 'r')
        return self

    def __next__(self):
        returned_string = self.ff.readline()
        if returned_string == '':
            self.ff.close()
            raise StopIteration

        return returned_string

    def __enter__(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
