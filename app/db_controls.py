from app.database import session, User


def add_new_item(obj):
    session.add()
    session.commit()

def check_if_user_exist(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first
    return user