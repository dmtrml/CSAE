from db import Category

u = Category

data = u.query.get(1)
a = data.subcategories
for i in a:
    print(i.subcategory)