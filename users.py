from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def user_id():
    return session.get("user_id", 0)

def username():
    user_id = session.get("user_id", 0)
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def logout():
    del session["user_id"]

def register(username,password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, access_level) VALUES (:username, :password, 'user')"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def username_available (username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return not user
    
def is_admin():   
    user_id=session.get("user_id", 0)
    sql = "SELECT access_level FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
    return result == "admin"
      
    
