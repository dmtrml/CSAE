from flask import Flask
from db import User
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

@app.route('/')
def hello_world():
    u = User
    data = u.query.filter(u.category=="Одежда").all()
    for row in data:
        rowpr = row.comment
    return rowpr

if __name__ == '__main__':
    app.run()