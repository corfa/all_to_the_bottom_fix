from sqlalchemy.orm import Session

from ParserLog import ParserLog
from db.queries.cart import create_cart
from db.queries.content_carts import create_content_carts
from db.queries.category import create_category
from db.queries.goods import create_goods
from db.queries.transaction import create_transaction
from db.queries.user import create_user, add_web_id
from db.queries.visits import create_visits

"""the function fills the database with data from ParserLog"""


def fill_data_in_tables(mapLog: ParserLog, session: Session):
    for i in mapLog.userIPadres:
        create_user(session, i)

    add_web_id(session, mapLog.webUserId)

    print("table user are full")

    for i in mapLog.Category:
        create_category(session, i)

    print("table category are full")
    for i in mapLog.webCartId:
        create_cart(session, i)

    print("table cart are full")

    for i in range(len(mapLog.SuccessfulTransactions["user_web_id"])):
        create_transaction(session, mapLog.SuccessfulTransactions["user_web_id"][i],
                           mapLog.SuccessfulTransactions["cart_web_id"][i])
    print("table transactions are full")

    for i in range(len(mapLog.Goods["id"])):
        create_goods(session, mapLog.Goods["id"][i], mapLog.Goods["category_and_name"][i])
    print("table goods are full")

    for i in range(len(mapLog.ContentCarts["goods_id"])):
        create_content_carts(session, mapLog.ContentCarts["goods_id"][i], mapLog.ContentCarts["amount"][i],
                             mapLog.ContentCarts["cart_id"][i])

    print("table content carts are full")

    for i in range(len(mapLog.visits["ip"])):
        create_visits(session, mapLog.visits["ip"][i], mapLog.visits["category"][i], mapLog.visits["time"][i],
                      mapLog.visits["date"][i])
    print("table visits are full")

    print("all tables are full")
