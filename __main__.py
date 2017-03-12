import os
import datetime
import json
from collections import OrderedDict

from ruamel import yaml
from ginger import Ginger


basedir = os.path.join(os.path.expanduser("~"), "Documents",
                       "Progetti", "HTML-CSS", "ginger-output")
cartelle = []
cartelle.append(os.path.join(basedir, "_content"))
cartelle.append(os.path.join(basedir, "_files"))
cartelle.append(os.path.join(basedir, "_images"))

ginger = Ginger(*cartelle)
ginger.registra_allegati(tag="Images", estensioni=[".jpg", ".jpeg", ".png", ".gif"])
ginger.registra_allegati(tag="Files", estensioni=[".zip", ".rar", ".7z"])

t1 = datetime.datetime.now()
ginger.scansiona()


"""
Per ogni elemento trovato apre il corrispondente file .md con il frontmatter
e poi aggiorna le informazioni nella parte front-matter con quelle che ha trovato
"""


def file_representer(dumper, data: os.DirEntry):
    percorso = str(data.path)
    return dumper.represent_str(percorso)

# 'register' it
yaml.add_representer(os.DirEntry, file_representer)


print("DOCUMENTI TROVATI:")
print("=" * 20)
for indice, elemento in enumerate(ginger.documenti):
    print(elemento)

t2 = datetime.datetime.now()

print()
print(ginger.json())
print()
print(str((t2 - t1)/datetime.timedelta(seconds=1)))

# import test

"""
a = FrontMatter(elemento["documento"])
for tipo in ginger.allegati:
    try:
        # a.meta[tipo["tag"]] = elemento[tipo["tag"]]
        pass
    except KeyError:
        pass
b = OrderedDict(a.meta)
print(b)
b.move_to_end("title", last=False)
# b[b.keys()["Title"]] = 0
"""

# print("----\n" + yaml.dump(b) + "----\n\n" + a.contenuto)
