from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./leaderboard.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()


class PlayerScore(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    score = Column(Integer)


Base.metadata.create_all(bind=engine)


class ScoreRequest(BaseModel):
    name: str
    score: int


@app.post("/submit-score")
def submit_score(score_data: ScoreRequest):
    db = SessionLocal()
    new_score = PlayerScore(name = score_data.name, score = score_data.score)
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    db.close()
    return {"message": "Score submitted successfully"}


@app.get("/leaderboard")
def get_leaderboard():
    db=SessionLocal()
    scores = db.query(PlayerScore).order_by(PlayerScore.score.desc()).limit(10).all()
    db.close()
    return scores
