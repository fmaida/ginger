import os
from ginger import Ginger


basedir = "/Users/Cesco/Documents/Progetti/HTML-CSS/ginger-output"
cartelle = []
cartelle.append(os.path.join(basedir, "_content"))
cartelle.append(os.path.join(basedir, "_files"))
cartelle.append(os.path.join(basedir, "_images"))

ginger = Ginger(*cartelle)
ginger.registra_allegati(tag="Images", estensioni=[".jpg", ".jpeg", ".png", ".gif"])
ginger.registra_allegati(tag="Files", estensioni=[".zip", ".rar", ".7z"])
ginger.scansiona()
