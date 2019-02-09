from db import db_session, User, Category, Subcategory

u = User
c = Category

set_of_category = set()
all_data = u.query.all()
for row in all_data:
    if row.category != '':
        set_of_category.add(row.category)
print(set_of_category)


for category in set_of_category:
    new_category = Category(category)
    db_session.add(new_category)
db_session.commit()

for category in set_of_category:
    for i in range(1, 4):
        subcategory = category + ' ' + str(i)
        category_id = c.query.filter(c.category == category).first()
        new_subcategory = Subcategory(subcategory, category_id.id)
        db_session.add(new_subcategory)
db_session.commit()