from db import User

u = User

data = u.query.order_by(User.category.desc()).all()
print(data)