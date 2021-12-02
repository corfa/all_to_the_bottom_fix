from sqlalchemy.orm import Session

from db.models import Goods, Cart, ContentCarts


def create_content_carts(session: Session, goods_web_id: str, amount: str, carts_web_id: str):
    carts = session.query(Cart).filter(Cart.web_id == carts_web_id).first()
    goods = session.query(Goods).filter(Goods.web_id == goods_web_id).first()

    newContentCarts = ContentCarts(
        cart_id=carts.id,
        goods_id=goods.id,
        amount=amount
    )
    session.add(newContentCarts)
    session.commit()
    return newContentCarts


def carts_when_have_need_category(session: Session, mass: list, category_id: int) -> list:
    """Args:
            :param1 (Session)
            :param2 (list)
            :param3 (int)

        Returns:
             list: list with ContentCarts
            the function returns all ContentCarts where there is a goods from the desired category
          """
    result = []
    for i in mass:
        all_element = session.query(ContentCarts).filter(ContentCarts.cart_id == i).all()
        for j in all_element:
            goods = session.query(Goods).filter(Goods.id == j.goods_id).first()
            if int(goods.category_id) == category_id:
                result.append(j)
    return result


def carts_when_not_have_category(session: Session, mass: list, category_id: int) -> list:
    """Args:
              :param1 (Session)
              :param2 (list)
              :param3 (int)

          Returns:
               list: list with ContentCarts
              the function returns all baskets where there is no product from the desired category
            """
    result = []
    for i in mass:
        all = session.query(ContentCarts).filter(ContentCarts.cart_id == i.cart_id).all()
        for j in all:
            goods = session.query(Goods).filter(Goods.id == j.goods_id).first()
            if int(goods.category_id) != category_id:
                result.append(goods.category_id)
    return result
