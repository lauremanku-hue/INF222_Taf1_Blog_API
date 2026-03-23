from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Crée les tables dans le fichier blog.db s'il n'existe pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=title="Blog API Professionnelle - INF222",
    description="""
    Bienvenue sur l'API de Gestion de Blog
    ## Système CRUD Complet
    Cette API permet la gestion totale du cycle de vie des articles
     **Fonctionnalités incluses :**
    * 📝 **Création** d'articles
    * **Modification**
    * **Suppression**
    * 📖 **Lecture** de la liste complète 
    * 🔍 **Recherche** par mots-clés
    * 🚀 **Redirection automatique** 
    """,
    version="1.1.0",
     contact={
        "name": "Laure Manku",
        "email": "laure.manku@exemple.com",})

# Fonction pour obtenir l'accès à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/", response_model=models.Article)
def create_article(article: models.ArticleCreate, db: Session = Depends(get_db)):
    # On transforme le schéma Pydantic en modèle de base de données
    db_article = models.ArticleDB(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.get("/articles/", response_model=list[models.Article])
def read_articles(db: Session = Depends(get_db)):
    return db.query(models.ArticleDB).all()

# --- RECHERCHE (Search) ---
@app.get("/articles/search/", response_model=list[models.Article], tags=["Recherche"])
def search_articles(keyword: str, db: Session = Depends(get_db)):
    """Recherche des articles dont le titre ou le contenu contient le mot-clé"""
    articles = db.query(models.ArticleDB).filter(
        (models.ArticleDB.titre.contains(keyword)) | 
        (models.ArticleDB.contenu.contains(keyword))
    ).all()
    return articles

# --- UPDATE (Mise à jour) ---
@app.put("/articles/{article_id}", response_model=models.Article, tags=["Articles"])
def update_article(article_id: int, article_update: models.ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(models.ArticleDB).filter(models.ArticleDB.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    
    # Mise à jour des champs
    db_article.titre = article_update.titre
    db_article.contenu = article_update.contenu
    db_article.auteur = article_update.auteur
    
    db.commit()
    db.refresh(db_article)
    return db_article

# --- DELETE (Suppression) ---
@app.delete("/articles/{article_id}", tags=["Articles"])
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(models.ArticleDB).filter(models.ArticleDB.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    
    db.delete(db_article)
    db.commit()
    return {"message": "Article supprimé avec succès"}
