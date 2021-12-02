from sqlalchemy.orm import Session

from db.models import Visit, User, Category
from helper.helper import get_unique_elements


def create_visits(session: Session, ip: str, category_: str, time_: str, date_: str):
    user = session.query(User).filter(User.lastIp == ip).first()
    category_ = session.query(Category).filter(Category.name == category_).first()

    newVisit = Visit(
        time_visit=time_,
        date_visit=date_,
        user_id=user.id,
        category_id=category_.id

    )
    session.add(newVisit)
    session.commit()
    return newVisit


def get_visitors_ip_on_category(session: Session, category_: str):
    """Args:
                   :param1 (Session)
                   :param2 (str)


               Returns:
                    list: list with unique ip address
                  the function returns unique IPs that have visited the given category
                 """
    category = session.query(Category).filter(Category.name == category_).first()
    id_ = category.id
    allVisits = session.query(Visit).filter(Visit.category_id == id_).all()
    ip = []
    for i in allVisits:
        user = session.query(User).filter(User.id == i.user_id).first()
        ip.append(user.lastIp)
    ip = get_unique_elements(ip)

    return ip


def get_visitors_time_on_category(session: Session, category_: str):
    """Args:
                     :param1 (Session)
                     :param2 (str)


                 Returns:
                      list: list with time visits
                    the function returns all times of a visit to a given category
                   """
    category = session.query(Category).filter(Category.name == category_).first()
    id_ = category.id
    all_visits = session.query(Visit).filter(Visit.category_id == id_).all()
    time = []
    for i in all_visits:
        time.append(i.time_visit)
    return time


def get_visit_all_time(session: Session):
    all_visits = session.query(Visit).all()
    all_time = []
    for i in all_visits:
        all_time.append(i.time_visit)
    return all_time
