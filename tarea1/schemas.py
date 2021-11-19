from typing import List, Optional

from pydantic import BaseModel

class News(BaseModel):
    id_news: int
    title : str
    url : str
    date : str
    media_outlet : str
    category : str

    class Config:
        orm_mode = True