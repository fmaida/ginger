from .documento import Documento


class DocumentNotFoundException(Exception):
    pass


class Elenco:

    def __init__(self):
        self.elenco = []

    def aggiungi(self, documento: Documento):
        self.elenco.append(documento)

    def rimuovi(self, indice):
        del self.elenco[indice]

    def cerca(self, _id):
        try:
            return next(indice for indice, elemento in enumerate(self.elenco) if elemento.id == _id)
        except StopIteration:
            raise DocumentNotFoundException("The requested document index wasn't found")

    def ultimo(self):
        return self.elenco[-1]

    def __iter__(self):
        for elemento in self.elenco:
            yield elemento

    def __len__(self):
        return len(self.elenco)
