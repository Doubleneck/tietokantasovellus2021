from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, access_level, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["access_level"] = user.access_level
            return True
        else:
            return False

def user_id():
    return session.get("user_id", 0)

def username():
    if session:
        user_id = session.get("user_id")
        sql = "SELECT username FROM users WHERE id =:id "
        result = db.session.execute(sql, {"id":user_id})
        print (sql)
        return result.fetchone()[0]
    else:
        return "No user"# REMOVE FROM PROD VERSION  

def logout():
    del session["user_id"]
    del session["access_level"]

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
      
def all_users():
    sql = "SELECT username, access_level from USERS"
    list = db.session.execute(sql).fetchall()
    return list

