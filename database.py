from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On définit l'emplacement du fichier de la base de données
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# L'engine est le moteur qui communique avec SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# On crée une session pour faire des requêtes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La classe de base pour nos futurs modèles de table
Base = declarative_base()
