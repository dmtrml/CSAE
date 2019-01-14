from db import db_session, User
import csv
import datetime

row_list = []
with open('Monefy.Data.converted.full.final.csv', 'r', encoding='windows-1251') as f:
    fields = ['date', 'category', 'comment', 'outcome_account', 'outcome',
              'outcome_currency', 'income_account', 'income', 'income_currency']
    reader = csv.DictReader(f, fields, delimiter=';')
    for row in reader:
        print(row)

        if row['date'] != 'date':
            row['date'] = datetime.datetime.strptime(row['date'], '%d/%m/%Y')
            new_user = User(row['date'], row['category'], row['comment'], row['outcome_account'],
                            row['outcome'], row['outcome_currency'], row['income_account'], row['income'], row['income_currency'])
            db_session.add(new_user)

db_session.commit()

