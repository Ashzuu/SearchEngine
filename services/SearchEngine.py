import numpy as np
import pandas as pd
from typing import Optional
from models.Corpus import Corpus
from services.helpers.TextCleaner import nettoyer_texte


class SearchEngine:
    """
    Moteur de recherche par similarite textuelle.
    """
    def __init__(self, corpus: Optional[Corpus] = None) -> None:
        if corpus is None:
            self.corpus = Corpus()
        else:
            self.corpus = corpus

        self.vocab = {}
        self.mat_TF = None
        self.mat_TFxIDF = None
        self.idf = None
        self.doc_norms = None

        self._initialiser_moteur()

    def _initialiser_moteur(self) -> None:
        """
        Initialise le vocabulaire et les matrices creuses.
        """
        self.vocab = self.corpus.vocab
        self.mat_TF = self.corpus.mat_TF
        self.mat_TFxIDF = self.corpus.mat_TFxIDF

        nb_docs = self.corpus.nb_docs
        taille_vocab = len(self.vocab)

        # Calcul du vecteur IDF
        self.idf = np.zeros(taille_vocab)
        for mot, infos in self.vocab.items():
            col_id = infos["id"]
            df = infos["document_frequency"]
            calcul_idf = np.log((1.0 + nb_docs) / (1.0 + df)) + 1.0
            self.idf[col_id] = calcul_idf

        # Normes L2 de chaque document
        carres = self.mat_TFxIDF.power(2)
        sommes = carres.sum(axis=1)
        self.doc_norms = np.sqrt(sommes).A1

    def search(self, query: str, top_n: int = 10) -> pd.DataFrame:
        """
        Recherche les documents les plus pertinents pour une requete.
        """
        colonnes = ["id", "score", "titre", "origine", "auteur", "date", "texte"]

        if not query:
            return pd.DataFrame(columns=colonnes)

        texte_propre = nettoyer_texte(query)
        mots_requete = texte_propre.split()

        if not mots_requete:
            return pd.DataFrame(columns=colonnes)

        # Construction du vecteur de requete
        taille_vocab = len(self.vocab)
        vecteur_requete = np.zeros(taille_vocab)

        for mot in mots_requete:
            if mot in self.vocab:
                col_id = self.vocab[mot]["id"]
                valeur_idf = self.idf[col_id]
                vecteur_requete[col_id] += 1.0 * valeur_idf

        # Norme du vecteur de requete
        norme_requete = np.linalg.norm(vecteur_requete)
        if norme_requete == 0.0:
            return pd.DataFrame(columns=colonnes)

        # Produit scalaire et similarite cosinus
        produit_scalaire = self.mat_TFxIDF.dot(vecteur_requete)
        normes_combinees = self.doc_norms * norme_requete

        nb_docs = self.corpus.nb_docs
        scores = np.zeros(nb_docs)
        masque = normes_combinees > 0
        scores[masque] = produit_scalaire[masque] / normes_combinees[masque]

        # Tri des meilleurs scores
        indices_tries = np.argsort(scores)
        indices_decroissants = indices_tries[::-1]
        meilleurs_indices = indices_decroissants[:top_n]

        resultats = []
        for idx in meilleurs_indices:
            score_brut = scores[idx]
            score_arrondi = round(float(score_brut), 4)

            # Si le score est nul, on peut ignorer
            if score_arrondi <= 0:
                continue

            doc = self.corpus.documents.get(idx)
            texte = getattr(doc, "text", "")
            titre = getattr(doc, "title", "")
            if not titre and texte:
                morceaux = texte.split(". ")
                titre = morceaux[0][:100]

            auteur = getattr(doc, "author", "")
            date = getattr(doc, "date", "")
            origine = "inconnu"
            if hasattr(doc, "getType"):
                origine = doc.getType()

            ligne = {
                "id": idx,
                "score": score_arrondi,
                "titre": titre,
                "origine": origine,
                "auteur": auteur,
                "date": date,
                "texte": texte
            }
            resultats.append(ligne)

        df_resultats = pd.DataFrame(resultats, columns=colonnes)
        return df_resultats

    def concorde(self, expression: str, context_size: int = 30) -> pd.DataFrame:
        """
        Construit le concordancier pour l'expression.
        """
        return self.corpus.concorde(expression, context_size=context_size)

    def stats(self, n: int = 10) -> pd.DataFrame:
        """
        Retourne les statistiques de frequences des mots.
        """
        return self.corpus.stats(n=n)
