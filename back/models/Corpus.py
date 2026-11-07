import re
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from typing import Dict, List, Optional
from services.helpers.Singleton import singleton
from services.helpers.TextCleaner import nettoyer_texte
from models.Author import Author


@singleton
class Corpus:
    """
    Represente une collection de documents.
    """
    def __init__(self) -> None:
        self.name: str = "Corpus for SearchEngine"
        self.documents: Dict[int, object] = {}
        self.nb_docs: int = 0
        self.authors: Dict[str, Author] = {}

        self._texte_concat: Optional[str] = None
        self._vocab: Optional[Dict[str, dict]] = None
        self._freq: Optional[pd.DataFrame] = None
        self._mat_TF: Optional[csr_matrix] = None
        self._mat_TFxIDF: Optional[csr_matrix] = None

    def add_document(self, doc) -> None:
        """
        Ajoute un document dans la collection.
        """
        doc_id = self.nb_docs
        self.documents[doc_id] = doc
        self.nb_docs += 1

        self._texte_concat = None
        self._vocab = None
        self._freq = None
        self._mat_TF = None
        self._mat_TFxIDF = None

        if hasattr(doc, "author") and doc.author:
            author_name = doc.author
            if author_name not in self.authors:
                self.authors[author_name] = Author(name=author_name)
            self.authors[author_name].add(doc)

    @property
    def texte_concat(self) -> str:
        """
        Retourne tous les textes assembles en une seule chaine.
        """
        if self._texte_concat is None:
            textes = []
            for doc in self.documents.values():
                if hasattr(doc, "text") and doc.text:
                    textes.append(doc.text)
            self._texte_concat = "\n".join(textes)
        return self._texte_concat

    def search(self, keyword: str, context_size: int = 30) -> List[str]:
        """
        Recherche des passages contenant le mot cle.
        """
        if not keyword:
            return []
        if not self.texte_concat:
            return []

        motif = re.escape(keyword)
        pattern_str = rf".{{0,{context_size}}}{motif}.{{0,{context_size}}}"
        regex = re.compile(pattern_str, re.IGNORECASE)

        passages = regex.findall(self.texte_concat)
        return passages

    def concorde(self, expression: str, context_size: int = 30) -> pd.DataFrame:
        """
        Construit un concordancier pour l'expression demandee.
        """
        colonnes = ["contexte gauche", "motif trouvé", "contexte droit"]
        if not expression:
            return pd.DataFrame(columns=colonnes)
        if not self.texte_concat:
            return pd.DataFrame(columns=colonnes)

        motif = re.escape(expression)
        pattern_str = rf"(.{{0,{context_size}}})({motif})(.{{0,{context_size}}})"
        regex = re.compile(pattern_str, re.IGNORECASE)

        matches = regex.findall(self.texte_concat)
        df = pd.DataFrame(matches, columns=colonnes)
        return df

    @staticmethod
    def nettoyer_texte(text: str) -> str:
        """
        Nettoie le texte donne.
        """
        return nettoyer_texte(text)

    def _calculer_frequences_et_vocabulaire(self) -> None:
        """
        Construit le vocabulaire et les frequences des termes.
        """
        term_freq = {}
        doc_freq = {}

        for doc in self.documents.values():
            texte_brut = getattr(doc, "text", "")
            if not texte_brut:
                continue

            texte_propre = nettoyer_texte(texte_brut)
            mots = texte_propre.split()

            mots_uniques = set()
            for mot in mots:
                term_freq[mot] = term_freq.get(mot, 0) + 1
                if mot not in mots_uniques:
                    doc_freq[mot] = doc_freq.get(mot, 0) + 1
                    mots_uniques.add(mot)

        serie_tf = pd.Series(term_freq)
        serie_df = pd.Series(doc_freq)
        freq_df = pd.DataFrame({
            "term frequency": serie_tf,
            "document frequency": serie_df
        })
        freq_df.index.name = "mot"
        freq_df = freq_df.sort_values(by="term frequency", ascending=False)
        self._freq = freq_df

        mots_tries = sorted(term_freq.keys())
        vocab_dict = {}
        for index, mot in enumerate(mots_tries):
            total_occurrences = term_freq[mot]
            nombre_documents = doc_freq.get(mot, 0)
            vocab_dict[mot] = {
                "id": index,
                "term_frequency": total_occurrences,
                "document_frequency": nombre_documents
            }
        self._vocab = vocab_dict

    @property
    def vocab(self) -> Dict[str, dict]:
        """
        Retourne le vocabulaire sous forme de dictionnaire.
        """
        if self._vocab is None:
            self._calculer_frequences_et_vocabulaire()
        return self._vocab

    @property
    def freq(self) -> pd.DataFrame:
        """
        Retourne le tableau des frequences des mots.
        """
        if self._freq is None:
            self._calculer_frequences_et_vocabulaire()
        return self._freq

    def _construire_matrices(self) -> None:
        """
        Construit les matrices mat_TF et mat_TFxIDF.
        """
        vocabulaire = self.vocab
        nb_mots = len(vocabulaire)
        nb_documents = self.nb_docs

        lignes = []
        colonnes = []
        valeurs = []

        for doc_id, doc in self.documents.items():
            texte_brut = getattr(doc, "text", "")
            texte_propre = nettoyer_texte(texte_brut)
            mots = texte_propre.split()

            comptage = {}
            for mot in mots:
                comptage[mot] = comptage.get(mot, 0) + 1

            for mot, compte in comptage.items():
                if mot in vocabulaire:
                    col_id = vocabulaire[mot]["id"]
                    lignes.append(doc_id)
                    colonnes.append(col_id)
                    valeurs.append(compte)

        taille = (nb_documents, nb_mots)
        coordonnees = (valeurs, (lignes, colonnes))
        self._mat_TF = csr_matrix(coordonnees, shape=taille, dtype=float)

        vecteur_idf = np.zeros(nb_mots)
        for mot, infos in vocabulaire.items():
            col_id = infos["id"]
            df = infos["document_frequency"]
            calcul_idf = np.log((1.0 + nb_documents) / (1.0 + df)) + 1.0
            vecteur_idf[col_id] = calcul_idf

        self._mat_TFxIDF = self._mat_TF.multiply(vecteur_idf).tocsr()

    @property
    def mat_TF(self) -> csr_matrix:
        """
        Retourne la matrice creuse Term Frequency.
        """
        if self._mat_TF is None:
            self._construire_matrices()
        return self._mat_TF

    @property
    def mat_TFxIDF(self) -> csr_matrix:
        """
        Retourne la matrice creuse TF-IDF.
        """
        if self._mat_TFxIDF is None:
            self._construire_matrices()
        return self._mat_TFxIDF

    def stats(self, n: int = 10) -> pd.DataFrame:
        """
        Affiche les statistiques globales du corpus.
        """
        tableau = self.freq
        total_mots = len(tableau)

        print("=== Statistiques du Corpus ===")
        print(f"Nombre de mots différents dans le corpus : {total_mots}")
        print(f"\nLes {n} mots les plus fréquents :")
        premiers_mots = tableau.head(n)
        print(premiers_mots)
        print("================================")

        return tableau

    def __repr__(self) -> str:
        return f"Corpus '{self.name}' with {self.nb_docs} documents"

    def display(self, n: int = 5) -> None:
        """
        Affiche les premiers documents tries par date et titre.
        """
        documents_tries = sorted(
            self.documents.values(),
            key=lambda item: (item.date, item.title)
        )
        for doc in documents_tries[:n]:
            print(doc)
