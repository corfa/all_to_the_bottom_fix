from sqlalchemy.orm import Session

from db.models import Cart, Transaction


def create_cart(session: Session, web_id_: str):
    newCart = Cart(
        web_id=web_id_,
    )
    session.add(newCart)
    session.commit()
    return newCart


