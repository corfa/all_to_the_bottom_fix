from sqlalchemy.orm import Session

from db.models import Category


def create_category(session: Session, category: str):
    newCategory = Category(
        name=category,

    )
    session.add(newCategory)
    session.commit()
    return newCategory
