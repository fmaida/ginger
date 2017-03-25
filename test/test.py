import os
import unittest

from test.creator import create
from rosie import Rosie


class RosieTest(unittest.TestCase):

    def setUp(self):
        basedir = os.path.join(os.path.expanduser("~"), "Documents",
                               "Progetti", "HTML-CSS", "rosie-output")
        cartelle = []
        cartelle.append(os.path.join(basedir, "_content"))
        # cartelle.append(os.path.join(basedir, "_files"))
        cartelle.append(os.path.join(basedir, "_images"))

        self.rosie = Rosie(*cartelle)
        self.rosie.registra_allegati(tag="Images",
                                     estensioni=[".jpg", ".jpeg", ".png", ".gif"])
        self.rosie.registra_allegati(tag="Files",
                                     estensioni=[".zip", ".rar", ".7z"])

        self.rosie.scan()

    def test_documenti_trovati(self):
        self.assertEqual(len(self.rosie.elenco), 100, "Ci dovevano essere 100 documenti")

    def test_tutti_hanno_titolo_e_tag(self):
        for indice, elemento in enumerate(self.rosie, start=1):
            self.assertTrue("title" in elemento.meta.keys(),
                            "Non ci doveva essere un documento senza titolo")
            self.assertTrue("date" in elemento.meta.keys(),
                            "Non ci doveva essere un documento senza data")

    def test_il_primo_ha_almeno_un_immagine(self):
        """
        Il primo elemento ha sempre almeno un'immagine, per via di come creo
        i files nel pacchetto test
        """

        ciccio = self.rosie.find("element0001")
        self.assertTrue("images" in ciccio.meta,
                        "Il primo elemento doveva avere almeno un'immagine")

    def tearDown(self):
        print(self.rosie.json())
        pass


if __name__ == "__main__":
    create(100)
    unittest.main()
