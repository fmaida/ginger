from rosie import DocumentNotFound, NoDocuments
from .documento import Documento


class Elenco:
    """
    Gestisce un elenco di documenti
    """
    BASEDIR = ""  # La cartella di base

    @classmethod
    def set_basedir(cls, _basedir):
        cls.BASEDIR = _basedir
        Documento.set_basedir(_basedir)

    def __init__(self):
        self.elenco = []

    def aggiungi(self, _id: str, _file: str):
        """
        Aggiunge un nuovo documento
        
        :param _id:     L'ID del documento da aggiungere 
        :param _file:   Il percorso assoluto al file        
        """
        self.elenco.append(Documento(_id=_id, _file=_file))

    def rimuovi(self, indice):
        """
        Rimuove un documento dall'elenco in base al suo indice
        
        :param indice:  Indice del documento da rimuovere         
        """
        del self.elenco[indice]

    def cerca(self, _id):
        """
        Cerca un documento
        :param _id: L'ID da ricercare
        :return:    Un'istanza del documento trovato, 
                    altrimenti solleva un'eccezione DocumentNotFound
        """
        try:
            return self.elenco[next(indice for indice, elemento in enumerate(self.elenco) if elemento.id == _id)]
        except StopIteration:
            raise DocumentNotFound("The requested document '{}' wasn't found".format(_id))

    def ultimo(self):
        """
        Restituisce l'ultimo documento memorizzato nell'elenco
        Altrimenti solleva un'eccezione        
        """
        try:
            return self.elenco[-1]
        except IndexError:
            raise NoDocuments("There are no documents available")

    def __iter__(self):
        for elemento in self.elenco:
            yield elemento

    def __len__(self):
        return len(self.elenco)
