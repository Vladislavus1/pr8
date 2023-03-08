from database import session, User
from db_controls import add_new_item
from werkzeug.security import generate_password_hash

pwd = generate_password_hash("admin")
admin = User("admin", pwd, "admin@gmail.com")
add_new_item(admin)
users = session.query(User).first()


print(users, "query")