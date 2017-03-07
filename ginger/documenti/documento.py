import os
from collections import OrderedDict

from .frontmatter import FrontMatter, FrontMatterException


class Documento:

    def __init__(self, _id: str, _file: os.DirEntry):
        self.id = _id
        self.file = _file
        self.meta = OrderedDict()
        self.importa_tags()

    def importa_tags(self):
        try:
            if os.path.exists(self.file):
                f = FrontMatter(self.file)
                for chiave in f.meta:
                    self.meta[chiave.lower()] = f.meta[chiave]
        except FrontMatterException:
            pass

    def json(self):
        temp = dict()
        temp["id"] = self.id
        temp["file"] = self.file
        temp["rel"] = {}
        for chiave in self.meta:
            temp["rel"][chiave.lower()] = self.meta[chiave]
        return temp

    def __repr__(self):
        return "<Documento: {}>".format(self.id)
