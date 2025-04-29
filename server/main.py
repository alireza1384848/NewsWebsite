from fastapi import FastAPI, Depends, HTTPException, status, Form, Response, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud, auth
from database import SessionLocal, engine, Base
from datetime import timedelta
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

# اجازه دادن به درخواست از همه جا برای تست
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = crud.get_user_by_username(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
@app.get("/user")
def read_root():
    return {"message": "User created successfully"}
@app.post("/signup")
async def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = auth.get_password_hash(user_data.password)
    user = models.User(
        username=user_data.username,
        name=user_data.name,
        family=user_data.family,
        password=hashed_password,
        rule=user_data.rule
    )
    crud.create_user(db, user)
    return {"message": "User created successfully"}

@app.post("/token")
async def login_for_access_token(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    return {"message": "Login successful"}

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@app.post("/news")
async def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    from datetime import datetime
    db_news = models.News(
        title=news.title,
        body=news.body,
        summary=news.summary,
        image_url=news.image_url,
        author=current_user.username,
        date=datetime.utcnow().isoformat()
    )
    crud.create_news(db, db_news)
    return {"message": "News created successfully"}

@app.get("/news", response_model=list[schemas.NewsCreate])
async def get_all_news(db: Session = Depends(get_db)):
    news_list = crud.get_all_news(db)
    return news_list

@app.delete("/news/{news_id}")
async def delete_news(news_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    if news.author != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this news")
    crud.delete_news(db, news)
    return {"message": "News deleted successfully"}


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
