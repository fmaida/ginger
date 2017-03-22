import os
import unittest

from ginger import Ginger

# import mytests
# mytests.create(100)


class GingerTest(unittest.TestCase):

    def setUp(self):
        basedir = os.path.join(os.path.expanduser("~"), "Documents",
                               "Progetti", "HTML-CSS", "ginger-output")
        cartelle = []
        cartelle.append(os.path.join(basedir, "_content"))
        # cartelle.append(os.path.join(basedir, "_files"))
        cartelle.append(os.path.join(basedir, "_images"))

        self.ginger = Ginger(*cartelle)
        self.ginger.registra_allegati(tag="Images",
                                      estensioni=[".jpg", ".jpeg", ".png", ".gif"])
        self.ginger.registra_allegati(tag="Files",
                                      estensioni=[".zip", ".rar", ".7z"])

        self.ginger.scansiona()

    def test_documenti_trovati(self):
        self.assertEqual(len(self.ginger.documenti), 100, "Ci dovevano essere 100 elenco")

    def test_tutti_hanno_titolo_e_tag(self):
        for indice, elemento in enumerate(self.ginger, start=1):
            try:
                self.assertIn(str(indice),
                              elemento.meta["title"],
                              "Non ci doveva essere un documento senza titolo")
                """
                self.assertNotEqual(elemento.meta["tags"],
                                    "",
                                    "Non ci doveva essere un documento senza tag")
                """
            except TypeError as e:
                print(elemento.meta["title"])

    def test_il_primo_ha_almeno_un_immagine(self):
        """
        Il primo elemento ha sempre almeno un'immagine, per via di come creo
        i files nel pacchetto mytests
        """
        
        ciccio = self.ginger.find("element0001")
        self.assertGreaterEqual(len(ciccio.meta["images"]), 1,
                                "Il primo elemento doveva avere almeno un'immagine")

if __name__ == "__main__":
    unittest.main()
