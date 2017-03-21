import os
from collections import OrderedDict

from ginger.elenco.documento.frontmatter import FrontMatter, FrontMatterException


class Documento:
    """
    Questa classe gestisce un singolo documento
    """

    def __init__(self, _id: str, _file: os.DirEntry, _basedir: str):
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
            if _basedir:
                # Se viene passata anche la cartella di partenza
                # Calcola il percorso relativo al file
                # attivandosi dalla cartella di partenza.
                self.file = os.path.relpath(_file, _basedir)
            else:
                # Se non viene passata la cartella di partenza
                # memorizza il percorso assoluto al file
                self.file = _file
            # Tenta di aprire il file e di leggere i meta-tags
            self.importa_tags(_basedir)
        else:
            self.file = ""

    def importa_tags(self, basedir):
        """
        Apre il file attualmente puntato da self.file e cerca 
        di leggerne i meta-tags
        
        :param basedir: Cartella di base per calcolare il percorso relativo al file   
        """
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

    def json(self) -> dict:
        """
        Esporta il documento in formato JSON
        
        :return: Le informazioni sul documento in formato JSON 
        """
        temp = dict()
        temp["id"] = self.id
        temp["file"] = self.file
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
