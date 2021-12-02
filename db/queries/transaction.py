from sqlalchemy.orm import Session

from db.models import Transaction, User, Cart


def create_transaction(session: Session, user_web_id: str, cart_web_id: str):
    user = session.query(User).filter(User.web_id == user_web_id).first()
    cart = session.query(Cart).filter(Cart.web_id == cart_web_id).first()
    if user is not None and cart is not None:
        newTransaction = Transaction(
            user_id=user.id,
            cart_id=cart.id,

        )
        session.add(newTransaction)
        session.commit()
        return newTransaction


def get_all_paid_carts(session: Session, mass: list) -> list:
    """Args:
                :param1 (Session)
                :param2 (list)


            Returns:
                 list: list with id paid carts
               the function returns the id of all paid cards
              """
    result = []
    for i in mass:
        transaction = session.query(Transaction).filter(Transaction.cart_id == i.id).first()
        if transaction is not None:
            result.append(i)
    return result
