from db import db

def get_topicareas():
    '''all topic areas, starting page'''
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    return topicareas

def add_newtopicarea(topicarea_name):
    sql = "INSERT INTO topicareas (name) VALUES (:name)"
    db.session.execute(sql, {"name":topicarea_name})
    db.session.commit()    

def get_topicareaname(topicarea_id):
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topicarea_name= result.fetchone()[0]
    return topicarea_name


def get_topics(topicarea_id):
     sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "
     result = db.session.execute(sql, {"id":topicarea_id})
     selected_topics = result.fetchall()
     return selected_topics

def add_newtopic (topicarea_id,user_id,topic_name,message_content):
    '''adds also the first message'''
    sql = "INSERT INTO topics (topicarea_id,name,user_id) VALUES (:topicarea_id,:name,:user_id) returning id"
    result=db.session.execute(sql, {"name":topic_name,"topicarea_id":topicarea_id,"user_id":user_id})
    topic_id = result.fetchone()[0]    
    db.session.commit()
    sql2 = "INSERT INTO messages (topics_id, content, created_at,user_id) VALUES (:topic_id,:content,NOW(),:user_id)"
    db.session.execute(sql2, {"topic_id":topic_id,"content":message_content,"user_id":user_id})
    db.session.commit()
    return topic_id 

def get_topicname(topic_id):
    sql="SELECT name FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    topic_name=result.fetchone()[0]
    return topic_name

def view_messages(topicarea_id,topic_id):
    sql = "SELECT content FROM messages WHERE topics_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    selected_messages= result
    return selected_messages

def new_message(topicarea_id,topic_id,content,user_id):
    sql = "INSERT INTO messages (topics_id, content, created_at,user_id) VALUES (:topic_id,:content,NOW(),:user_id)"
    db.session.execute(sql, {"topic_id":topic_id,"content":content,"user_id":user_id})
    db.session.commit()  

