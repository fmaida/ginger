class ListaDocumenti:

    def __init__(self):
        self.elenco = []

    def aggiungi(self, documento):
        self.elenco.append(documento)

    def rimuovi(self, indice):
        del self.elenco[indice]

    def cerca(self, _id):
        return next(indice for indice, elemento in enumerate(self.elenco) if elemento.id == _id)

    def ultimo(self):
        return self.elenco[-1]

    def __getitem__(self, indice):
        return self.elenco[indice]

    def __iter__(self):
        for elemento in self.elenco:
            yield elemento

    def __len__(self):
        return len(self.elenco)
