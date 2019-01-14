from db import User

u = User

data = u.query.order_by(User.email.desc()).all()
print(data)