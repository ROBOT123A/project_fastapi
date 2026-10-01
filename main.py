import  models
from database import  get_db,engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from  schema import  *

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/test_db")
def test_db(db:Session = Depends(get_db)):
    post=db.query(models.Post).all()
    return {"message": "Database connection successful!", "data": post}

@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)  
    db.commit()
    db.refresh(new_post) #  this retrieve  the created  datavase filed
    return {"message": "Post created successfully!", "data": new_post}

@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post retrieved successfully!", "data": post}

@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db)
):
    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published

    db.commit()
    db.refresh(post)

    return {
        "message": "Post updated successfully!",
        "data": post
    }
