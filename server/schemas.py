from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    name: str
    family: str
    password: str
    rule: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class NewsCreate(BaseModel):
    title: str
    body: str
    image_url: str = ""
