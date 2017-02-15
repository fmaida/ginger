import os
from .modello import Elemento
from .frontmatter import FrontMatter


class Ginger:

    def __init__(self, *args):
        self.estensione = ".md"
        self.cartelle = args
        self.collezione = []
        self.allegati = []
        self.allegati_controllabili = []

    def registra_allegati(self, tag, estensioni):
        self.allegati_controllabili.append(estensioni)

    def scansiona(self):
        """
        Scansiona tutte le cartelle alla ricerca di file in formato .md 
        e di possibili allegati
        """

        for cartella in self.cartelle:
            self.analizza_cartella(cartella)
        print("DOCUMENTI:")
        print("=" * 16)
        for indice, elemento in enumerate(self.collezione):
            print(f"{indice+1}. {elemento}")
        print()
        print("ALLEGATI:")
        print("=" * 16)
        for indice, elemento in enumerate(self.allegati):
            print(f"{indice+1}. {elemento}")

    def analizza_cartella(self, cartella):
        """
        Analizza una singola cartella
        
        Args:
            cartella: La cartella da analizzare 
        """
        risultati = os.scandir(cartella)
        for elemento in risultati:
            _id, estensione = os.path.splitext(elemento.name)
            if elemento.name.endswith(self.estensione) and elemento.is_file():
                self.aggiungi_o_modifica(_id, elemento, "")
            elif estensione in self.allegati_controllabili[0]:
                self.aggiungi_o_modifica(_id, elemento, "Images")
            elif estensione in self.allegati_controllabili[1]:
                self.aggiungi_o_modifica(_id, elemento, "Files")
            elif elemento.is_dir():
                self.analizza_cartella(os.path.join(cartella, elemento))

    def aggiungi_o_modifica(self, _id, documento, tag):
        """
        Se è un documento (tag == ""):
            Crea l'elemento se _id non esiste
            Modifica l'elemento se _id esiste
        Se è un allegato (tag != ""):
            Crea un elemento vuoto e aggiunge agli allegati se _id non esiste
            Aggiunge in coda agli allegati se _id esiste
        Args:
            _id: 
            documento: 
            tag: 
        """
        try:
            indice = next(indice for indice, elemento in enumerate(self.collezione) if elemento["id"] == _id)
            # L'elemento esiste
            if tag == "":
                self.collezione[indice]["id"] = _id
                self.collezione[indice]["documento"] = documento.name
            else:
                if tag not in self.collezione[indice]:
                    self.collezione[indice][tag] = []
                self.collezione[indice][tag].append(documento.name)
        except StopIteration:
            # L'elemento non esiste
            n = len(self.collezione)
            self.collezione.append({"index": n, "id": _id, "documento": ""})
            if tag == "":
                self.collezione[n]["documento"] = documento.name
            else:
                self.collezione[n][tag] = [documento.name]
