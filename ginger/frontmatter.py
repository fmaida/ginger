import os
import re

import yaml
import markdown2

basedir = os.path.dirname(__file__)


class FrontMatterException(Exception):
    pass


class FrontMatter:
    """
    Questa classe gestisce una pagina markdown 
    che contenga una parte iniziale in front-matter YAML
    """

    def __init__(self, p_file):
        """
        Costruttore della classe
        
        Args:
            p_file: Il file da aprire 
        """

        self.meta = {}
        self.contenuto = ""
        self.importa(p_file)

    def importa(self, p_file):
        """
        Importa un file
        
        Args:
            p_file: Il file da aprire 

        Returns:
            None
        """

        with open(p_file, "r") as f:
            testo = f.read()
        frontmatter, contenuto = self.separa_frontmatter(testo)
        self.meta = yaml.load(frontmatter)
        self.contenuto = markdown2.markdown(contenuto)

    def esporta(self):
        """
        Esporta il contenuto dell'istanza della classe 
        in un dizionario
        
        Returns:
            dict
        """
        temp = self.meta
        temp["_content"] = self.contenuto
        return temp

    def separa_frontmatter(self, p_testo):
        """
        Prende il file di testo e cerca di separare la parte 
        iniziale in front-matter YAML dal resto in markdown
        
        Args:
            p_testo: Testo da analizzare 

        Returns:
            Una tupla con la parte YAML e con il resto in markdown
        """

        trovato = re.search(r"(?:-{4,})([\w\W\D]*)(?:-{4,})([\w\W\D\s]*)", p_testo, re.VERBOSE | re.MULTILINE)
        return trovato.group(1), trovato.group(2)


def apri(game_id):
    try:
        elemento = os.path.join(basedir, "content", game_id + ".md")
        out = FrontMatter(elemento).esporta()
    except IOError:
        out = {}
    return out
