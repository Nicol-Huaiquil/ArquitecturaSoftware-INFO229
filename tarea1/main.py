from typing import List
from typing import Optional

from sqlalchemy.sql.type_api import to_instance

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#/v1/news?from=2021-01-01&to=2021-01-31&category=sport
#@app.get
#@app.post
#@app.put

@app.get("/v1/news/", response_model=List[schemas.News])
def read_news(from_: Optional[str], to_: Optional[str], category: Optional[str], db: Session = Depends(get_db) ):
    news = crud.get_news(db, from_=from_, to_=to_,category=category)
    
    return news