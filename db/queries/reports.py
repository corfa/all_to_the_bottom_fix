from sqlalchemy.orm import Session

from db.models import Cart, Transaction, User, ContentCarts, Category
from db.queries.content_carts import carts_when_have_need_category, carts_when_not_have_category
from db.queries.transaction import get_all_paid_carts
from db.queries.user import get_all_user_ip
from db.queries.visits import get_visitors_ip_on_category, get_visitors_time_on_category, get_visit_all_time
from helper.helper import most_popular_country, from_data_time_to_part_of_the_day, count_request_in_hour, duplicate_elements, \
    find_most_popular_element

"""functions in this file access the database and return analytical reports"""


def which_country_most_often_visits(session: Session) -> str:
    allUser = get_all_user_ip(session)
    country = most_popular_country(allUser)
    return country


def which_country_most_often_looks_at_the_category(session: Session, category: str) -> str:
    allVisits = get_visitors_ip_on_category(session, category)
    country = most_popular_country(allVisits)
    return country


def what_time_of_day_the_category_is_viewed(session: Session, category: str) -> str:
    allTime = get_visitors_time_on_category(session, category)
    time_of_day = from_data_time_to_part_of_the_day(allTime)
    return time_of_day


def maximum_number_of_requests_per_hour(session: Session) -> int:
    allTime = get_visit_all_time(session)
    digit = count_request_in_hour(allTime)
    return digit


def what_they_buy_together_from_categories(session: Session, category_: str) -> str:
    category = session.query(Category).filter(Category.name == category_).first()
    allCart = session.query(ContentCarts).all()
    id_cart = []
    for i in allCart:
        id_cart.append(i.cart_id)
    carts_when_more_one_goods = duplicate_elements(id_cart)
    cart_where_have_need_category = carts_when_have_need_category(session, carts_when_more_one_goods, int(category.id))
    all_cart_paid = get_all_paid_carts(session, cart_where_have_need_category)
    two_most_category = carts_when_not_have_category(session, all_cart_paid, int(category.id))
    res_id = find_most_popular_element(two_most_category)
    res_category = session.query(Category).filter(Category.id == res_id).first()
    return str(res_category.name)


def how_many_unpaid_carts(session: Session) -> int:
    allCarts = session.query(Cart).all()
    count_notPaidCarts = 0
    for cart in allCarts:
        transaction = session.query(Transaction).filter(Transaction.cart_id == cart.id).first()
        if transaction is None:
            count_notPaidCarts += 1
    return count_notPaidCarts


def how_many_users_bought_more_than_once(session: Session) -> int:
    allUsers = session.query(User).all()
    count_users = 0
    for user in allUsers:
        q = session.query(Transaction).filter(Transaction.user_id == user.id).count()
        if q >= 2:
            count_users += 1
    return count_users
