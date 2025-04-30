from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    rule: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class NewsCreate(BaseModel):
    title: str
    summary: str
    body: str
    image_url: str
    date: str
class NewsOut(NewsCreate):
    news_id: int
    author: str

    class Config:
        orm_mode = True