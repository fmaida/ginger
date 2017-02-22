from os import DirEntry
from collections import OrderedDict


class Documento:

    def __init__(self, _id: str, _file: DirEntry):
        self.id = _id
        self.file = _file
        self.meta = OrderedDict()

    def __repr__(self):
        return "<Documento: {}>".format(self.id)