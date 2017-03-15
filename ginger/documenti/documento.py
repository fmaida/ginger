import os
from collections import OrderedDict

from .frontmatter import FrontMatter, FrontMatterException


class Documento:

    def __init__(self, _id: str, _file: os.DirEntry, basedir):
        self.id = _id
        self.meta = OrderedDict()
        if _file != "":
            if basedir:
                self.file = os.path.relpath(_file, basedir)
            else:
                self.file = _file
            self.importa_tags(basedir)
        else:
            self.file = ""

    def importa_tags(self, basedir):
        try:
            percorso = os.path.join(basedir, self.file)
            if os.path.exists(percorso):
                f = FrontMatter(percorso)
                try:
                    for chiave in f.meta:
                        self.meta[chiave.lower()] = f.meta[chiave]
                except TypeError:
                    # Si vede che non ha nessun meta-tag da copiare
                    self.meta = []
                    pass
        except FrontMatterException:
            pass

    def json(self):
        temp = dict()
        temp["id"] = self.id
        temp["file"] = self.file
        temp["rel"] = {}
        for chiave in self.meta:
            temp["rel"][chiave] = self.meta[chiave]
        return temp

    def __repr__(self):
        return "<Documento: {}>".format(self.id)
