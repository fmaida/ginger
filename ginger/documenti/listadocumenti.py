class ListaDocumenti:

    def __init__(self):
        self.totale = 0
        self.elenco = []

    def aggiungi(self, documento):
        self.elenco.append(documento)
        self.totale += 1

    def rimuovi(self, indice):
        del self.elenco[indice]
        self.totale -= 1

    def cerca(self, _id):
        return next(indice for indice, elemento in enumerate(self.elenco) if elemento.id == _id)

    def ultimo(self):
        return self.elenco[-1]

    def __getitem__(self, indice):
        return self.elenco[indice]