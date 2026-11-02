import re


def nettoyer_texte(text: str) -> str:
    """
    Nettoie un texte pour faciliter son analyse.
    """
    if not isinstance(text, str):
        return ""

    texte_propre = text.lower()
    texte_propre = texte_propre.replace("\r\n", " ")
    texte_propre = texte_propre.replace("\n", " ")
    texte_propre = texte_propre.replace("\r", " ")
    texte_propre = texte_propre.replace("\t", " ")
    texte_propre = re.sub(r"[^\w\s]|[\d_]", " ", texte_propre)
    texte_propre = re.sub(r"\s+", " ", texte_propre)
    texte_propre = texte_propre.strip()

    return texte_propre
