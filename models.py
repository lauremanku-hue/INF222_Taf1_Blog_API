from sqlalchemy import Column, Integer, String, Text
from database import Base
from pydantic import BaseModel
from typing import Optional

# --- MODÈLE SQLALCHEMY (Pour la table dans la base de données) ---
class ArticleDB(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    contenu = Column(Text)
    auteur = Column(String)

# --- SCHÉMAS PYDANTIC (Pour la validation des données API) ---
class ArticleBase(BaseModel):
    titre: str
    contenu: str
    auteur: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int

    class Config:
        orm_mode = True 
