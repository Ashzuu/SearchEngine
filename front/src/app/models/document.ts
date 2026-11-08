export class Document {
  id: number;
  score: number;
  titre: string;
  origine: string;
  url: string;
  auteur: string;
  date: Date;
  texte: string;

  constructor(id: number, score: number, titre: string, origine: string, url:string, auteur: string, date: Date, texte: string) {
    this.id = id;
    this.score = score;
    this.titre = titre;
    this.origine = origine;
    this.url = url;
    this.auteur = auteur;
    this.date = date;
    this.texte = texte;
  }
}
