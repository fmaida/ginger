import os


class RelFile:

    @property
    def file(self):
        return self.absolute_path

    @property
    def name(self):
        return os.path.basename(self.absolute_path)

    @file.setter
    def file(self, _file):
        if _file != "":
            self.relative_path = os.path.relpath(_file, self.BASEDIR)
            self.absolute_path = os.path.join(self.BASEDIR, self.relative_path)
        else:
            raise ValueError("File path cannot be empty")

    @classmethod
    def set_basedir(cls, _basedir):
        cls.BASEDIR = _basedir

    def __init__(self, _file=""):
        self.absolute_path = ""
        self.relative_path = ""
        if _file != "":
            self.file = _file
