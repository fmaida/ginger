import os
import datetime
from collections import OrderedDict

from ginger.elenco.documento.frontmatter import FrontMatter, FrontMatterException
from ginger.elenco.documento.relfile import RelFile


class Documento:
    """
    Questa classe gestisce un singolo documento
    """

    @classmethod
    def set_basedir(cls, _basedir):
        RelFile.set_basedir(_basedir)

    def __init__(self, _id: str, _file: os.DirEntry):
        """
        Inizializzazione della classe
        
        :param _id:     ID del documento da registrare 
        :param _file:   Percorso (assoluto) al file
        :param basedir: Cartella di partenza dal quale ricavare 
                        il percorso relativo
        """
        self.id = _id
        self.meta = OrderedDict()
        if _file != "":
            # Se viene passato il percorso assoluto ad un file..
            self.file = RelFile(_file)
            # Tenta di aprire il file e di leggere i meta-tags
            self.importa_tags()
        else:
            self.file = RelFile()

    def importa_tags(self):
        """
        Apre il file attualmente puntato da self.file e cerca 
        di leggerne i meta-tags
        
        :param basedir: Cartella di base per calcolare il percorso relativo al file   
        """
        try:
            file_md = self.file.absolute_path
            if os.path.exists(file_md):
                f = FrontMatter(file_md)
                # Se il documento non ha meta-tags,
                # crea un dizionario vuoto per cominciare
                if f.meta is None:
                    f.meta = dict()
                try:
                    for chiave in f.meta:
                        self.meta[chiave.lower()] = f.meta[chiave]

                    # Se il titolo non è nei meta-tags se lo inventa lui
                    if "title" not in self.meta.keys():
                        self.meta["title"] = self.file.name
                    # Se la data non è nei meta-tags se lo inventa lui
                    if "date" not in self.meta.keys():
                        self.meta["date"] = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        if type(self.meta["date"]) == datetime:
                            self.meta["date"] = self.meta["date"].strftime("%Y-%m-%d %H:%M:%S")
                except TypeError:
                    # Si vede che non ha nessun meta-tag da copiare
                    pass
        except FrontMatterException:
            pass
        pass

    def json(self) -> dict:
        """
        Esporta il documento in formato JSON
        
        :return: Le informazioni sul documento in formato JSON 
        """
        temp = dict()
        temp["id"] = self.id
        temp["file"] = self.file.relative_path
        temp["rel"] = {}
        for chiave in self.meta:
            temp["rel"][chiave] = self.meta[chiave]
        return temp

    def __repr__(self):
        """
        Rappresenta visivamente la classe
        :return: 
        """
        return "<Documento: {}>".format(self.id)
