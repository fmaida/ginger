import json
import os
import re

from .documenti import ListaDocumenti, Documento


class TipoAllegato:

    def __init__(self, tag, estensioni):
        self.tag = tag
        self.estensioni = estensioni


class Ginger:
    """
    Ginger scandaglia una o più cartelle alla ricerca di
    file di testo che contengano un front-matter YAML con 
    i meta-dati ed una parte di testo formattata in markdown.
    Inoltre cerca gli allegati (audio, video, files) correlati
    a questi file di testo. Riesce a riconoscerli perchè hanno 
    lo stesso nome ("zanac.md", "zanac.jpg", "zanac.mp3", ...)
    oppure perchè hanno nomi simili fra di loro
    ("zanac.md", "zanac--1.jpg", "zanac--2.jpg", ...)
    """

    def __init__(self, *args):
        """
        Costruttore della classe, a cui passo una serie
        di cartelle da scansionare
        
        Args:
            *args: Percorsi alle cartelle da analizzare 
        """

        # Imposta le cartelle da scandagliare
        self.cartelle = args
        # Imposta la cartella base
        self.basedir = self.cartelle[0]
        # Estensione dei file di testo da ricercare
        self.estensione = ".md"
        # Azzera alcuni parametri
        self.totale_documenti = 0
        self.documenti = ListaDocumenti()
        self.allegati = []

    def registra_allegati(self, tag, estensioni):
        """
        Con questo metodo indico una o più estensioni 
        da tenere sotto controllo durante la scansione, 
        ed eventualmente aggiungere alla lista.
        (es: "Immagini", [".jpg", ".png", ".gif"])
        
        Args:
            tag: Il tag con cui catalogare i files trovati 
            estensioni: Una lista delle estensioni da ricercare

        Returns:
            None
        """
        self.allegati.append(TipoAllegato(tag=tag.lower(), estensioni=estensioni))

    def scansiona(self):
        """
        Scansiona tutte le cartelle alla ricerca di file in formato .md 
        e di possibili allegati
        """

        self.documenti = ListaDocumenti()

        for cartella in self.cartelle:
            self.analizza_cartella(cartella)

        # Una volta finito di scansionare le cartelle, riordina gli allegati
        for elemento in self.documenti:
            for tipo in self.allegati:
                try:
                    elemento.meta[tipo.tag].sort()
                except:
                    pass

    def analizza_cartella(self, cartella):
        """
        Analizza una singola cartella
        
        Args:
            cartella: La cartella da analizzare 
        """
        risultati = os.scandir(cartella)
        for elemento in risultati:
            _id, estensione = os.path.splitext(elemento.name)
            if elemento.is_dir():
                # E' una sottocartella
                self.analizza_cartella(os.path.join(cartella, elemento))
            elif elemento.name.endswith(self.estensione) and elemento.is_file():
                # E' un file .md
                self.aggiungi_o_modifica(_id, elemento)
            else:
                # E' un file con un'altra estensione
                for tipo in self.allegati:
                    if estensione in tipo.estensioni:
                        self.aggiungi_o_modifica(_id, elemento, tag=tipo.tag)

    def aggiungi_o_modifica(self, _id, documento, tag=""):
        """
        Se è un documento (tag == ""):
            Crea l'elemento se _id non esiste
            Modifica l'elemento se _id esiste
        Se è un allegato (tag != ""):
            Crea un elemento vuoto e aggiunge agli allegati se _id non esiste
            Aggiunge in coda agli allegati se _id esiste
        Args:
            _id: L'id dell'elemento
            documento: Il documento da aggiungere
            tag: Il tag sotto cui catalogarlo (se è vuoto è un file .md)
        """
        try:

            # Prima di iniziare cerca di capire se il nome dell'elemento
            # finisce con un "--n" dove n è un numero da 0 in poi
            # Es: file: "zanac--1" --> id: "zanac"
            #     file: "pippols--14" --> id: "pippols"

            valori = re.split(r"[-]{2,}[0-9]+$", _id)
            _id = valori[0].lower()

            # Cerca l'ID per vedere se è già stato catalogato
            indice = self.documenti.cerca(_id)

            # L'elemento con l'ID esiste già,
            # altrimenti si verificherebbe un'eccezione
            if tag == "":
                self.documenti[indice].id = _id
                self.documenti[indice].file = os.path.relpath(documento, self.basedir)
                self.documenti[indice].importa_tags(self.basedir)
            else:
                if tag not in self.documenti[indice].meta:
                    self.documenti[indice].meta[tag] = []
                self.documenti[indice].meta[tag].append(os.path.relpath(documento, self.basedir))
        except StopIteration:
            # Se siamo qui vuol dire che non ha trovato un'altro
            # elemento con lo stesso ID ricercato... pazienza, vuol
            # dire che lo aggiungiamo ai nostri documenti
            self.documenti.aggiungi(Documento(_id=_id, _file="", basedir=self.basedir))
            if tag == "":
                self.documenti.ultimo().file = os.path.relpath(documento, self.basedir)
                self.documenti.ultimo().importa_tags(self.basedir)
            else:
                self.documenti.ultimo().meta[tag] = [os.path.relpath(documento, self.basedir)]

    def find(self, _id):
        temp = [elemento for elemento in self.documenti if elemento.id == _id]
        if len(temp) > 0:
            return temp[0]
        else:
            return None

    def json(self, indent=4):
        temp = []
        for documento in self.documenti:
            temp.append(documento.json())
        return json.dumps(temp, indent=indent)

    def __iter__(self):
        for elemento in self.documenti:
            yield elemento

    def __len__(self):
        return len(self.documenti)
