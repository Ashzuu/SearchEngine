import unittest
from services.helpers.TextCleaner import nettoyer_texte


class TestTextCleaner(unittest.TestCase):
    """
    Tests unitaires pour le nettoyage de texte (Partie 2, section 2.1 du cahier des charges Partie 2).
    """

    def test_lowercase_conversion(self):
        texte = "MACHINE LEARNING and Artificial Intelligence"
        nettoye = nettoyer_texte(texte)
        self.assertEqual(nettoye, "machine learning and artificial intelligence")

    def test_line_breaks_and_tabs_removal(self):
        texte = "First line.\nSecond line.\r\nThird line.\rFourth line.\tEnd."
        nettoye = nettoyer_texte(texte)
        self.assertNotIn("\n", nettoye)
        self.assertNotIn("\r", nettoye)
        self.assertNotIn("\t", nettoye)

    def test_punctuation_and_numbers_removal(self):
        texte = "Hello, world! 123 numbers and @#$% symbols _underscores_."
        nettoye = nettoyer_texte(texte)
        self.assertEqual(nettoye, "hello world numbers and symbols underscores")

    def test_multiple_spaces_and_trimming(self):
        texte = "   Too    many      spaces     "
        nettoye = nettoyer_texte(texte)
        self.assertEqual(nettoye, "too many spaces")

    def test_non_string_input(self):
        self.assertEqual(nettoyer_texte(None), "")
        self.assertEqual(nettoyer_texte(123), "")
        self.assertEqual(nettoyer_texte([]), "")


if __name__ == "__main__":
    unittest.main()
