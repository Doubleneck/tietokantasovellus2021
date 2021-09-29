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
    return session["access_level"] == "admin"

def is_puser():  
    "evaluates if user is priviledged user (puser)" 
    return session["access_level"] == "puser"    
      
def add_puser(user_id): 
    sql = "UPDATE users SET access_level = 'puser' where id=:user_id"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()

def remove_puser(user_id): 
    sql = "UPDATE users SET access_level = 'user' where id=:user_id"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()

def users():
    sql = "SELECT username, access_level, id from USERS where access_level = 'user'"
    list = db.session.execute(sql).fetchall()
    return list

def pusers():
    '''priviledged users'''
    sql = "SELECT username, access_level, id from USERS where access_level = 'puser'"
    list = db.session.execute(sql).fetchall()
    return list