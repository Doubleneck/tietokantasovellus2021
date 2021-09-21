from db import db

def add_visit():
    db.session.execute("INSERT INTO visitors (moment) VALUES (NOW())")
    db.session.commit()

def get_counter():
    result = db.session.execute("SELECT COUNT(*) FROM visitors")
    counter = result.fetchone()[0]
    return counter