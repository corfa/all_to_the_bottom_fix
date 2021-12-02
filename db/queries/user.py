from sqlalchemy.orm import Session

from db.models import User


def create_user(session: Session, ip_address: str):
    newUser = User(
        userName="-----",
        lastIp=ip_address,

    )
    session.add(newUser)
    session.commit()
    return newUser


def get_all_user_ip(session: Session):
    result = []
    allUsers = session.query(User).all()
    for i in allUsers:
        result.append(i.lastIp)
    return result


def add_web_id(session: Session, webUserId: dict):
    ip = webUserId["ip"]
    web_id = webUserId["web_id"]
    for i in (range(len(ip))):
        user = session.query(User).filter(User.lastIp == ip[i]).first()
        user.web_id = web_id[i]
        session.commit()
