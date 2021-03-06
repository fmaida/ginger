import os
import re
from collections import OrderedDict

from ruamel import yaml
import markdown2

basedir = os.path.dirname(__file__)


class FrontMatterException(Exception):
    pass


class FrontMatter:
    """
    Questa classe gestisce la lettura e la scrittura 
    di un documento di testo che contenga una parte 
    iniziale in front-matter YAML ed il resto con la
    formattazione Markdown
    """

    def __init__(self, p_file):
        """
        Costruttore della classe
        
        Args:
            p_file: Il file da aprire 
        """

        self.meta = OrderedDict()
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
        try:
            self.meta = yaml.load(frontmatter, Loader=yaml.BaseLoader)
            self.contenuto = markdown2.markdown(contenuto)
        except yaml.parser.ParserError:
            pass

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

        trovato = re.search(r"(?:-{4,})\n([\w\W\D]*)\n(?:-{4,})([\w\W\D\s]*)", p_testo, re.VERBOSE | re.MULTILINE)
        try:
            return trovato.group(1), trovato.group(2)
        except AttributeError:
            return "", p_testo


def apri(game_id):
    try:
        elemento = os.path.join(basedir, "content", game_id + ".md")
        out = FrontMatter(elemento).esporta()
    except IOError:
        out = {}
    return out
