from fastapi import FastAPI, Depends
from datetime import datetime
from models import BaseSQL, engine
from services import posts
from sqlalchemy.orm import Session

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/date")
def display_date():
    date = datetime.now()
    return {"La date actuelle est :"
    , date.strftime("%d/%m/%Y")}

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)


@app.get("/posts", tags=["posts"])
async def get_posts():
    return posts.get_all_posts()


@app.post("/posts", tags=["posts"])
async def create_post(post: schemas.Post, db: Session = Depends(models.get_db)):
   return posts.create_post(post=post, db=db)


@app.get("/posts/{post_id}", tags=["posts"])
async def get_post(post_id: str, **kwargs):
    return posts.get_post_by_id(post_id)
    

# @app.put("/posts/{post_id}", tags=["posts"])
# async def update_post_by_id(post_id: str, **kwargs):
#     return posts.update_post(post_id)


# @app.delete("/{post_id}", tags=["posts"])
# async def delete_post_by_id(post_id: str, **kwargs):
#     return posts.delete_post(post_id)
