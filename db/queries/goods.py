from sqlalchemy.orm import Session

from db.models import Goods, Category


def create_goods(session: Session, goods_web_id: str, category_and_name: str):
    category_and_name = category_and_name.split(" ")
    category = session.query(Category).filter(Category.name == category_and_name[0]).first()
    newGood = Goods(
        web_id=goods_web_id,
        name=category_and_name[1],
        category_id=int(category.id)

    )
    session.add(newGood)
    session.commit()
    return newGood
