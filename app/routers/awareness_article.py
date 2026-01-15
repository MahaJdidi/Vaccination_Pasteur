from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..utils import get_db, require_admin, get_current_user

router = APIRouter(prefix="/articles", tags=["AwarenessArticles"])

# GET all articles
@router.get("/", response_model=list[schemas.AwarenessArticleOut])
def get_articles(db: Session = Depends(get_db)):
    return db.query(models.AwarenessArticle).all()

# HEAD article
@router.head("/{article_id}")
def head_article(article_id: int, db: Session = Depends(get_db)):
    exists = db.query(models.AwarenessArticle).filter(models.AwarenessArticle.id == article_id).first()
    if not exists:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

# GET article by ID
@router.get("/{article_id}", response_model=schemas.AwarenessArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.AwarenessArticle).filter(models.AwarenessArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# POST article (admin only)
@router.post("/", response_model=schemas.AwarenessArticleOut)
def create_article(article: schemas.AwarenessArticleBase, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    new_article = models.AwarenessArticle(**article.dict(), created_by=admin.id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# PATCH article (admin only)
@router.patch("/{article_id}", response_model=schemas.AwarenessArticleOut)
def update_article(article_id: int, article: schemas.AwarenessArticleBase, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    db_article = db.query(models.AwarenessArticle).filter(models.AwarenessArticle.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

# DELETE article (admin only)
@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    article = db.query(models.AwarenessArticle).filter(models.AwarenessArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return Response(status_code=204)
