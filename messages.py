from db import db
import users

def get_topicareas():
    '''all topic areas, starting page'''
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    list=[]
    for t in topicareas:
        
        count_messages(t[0])
        list.append((t[0],t[1],count_messages(t[0])))
    print(list)    
    return list

def add_newtopicarea(topicarea_name):
    sql = "INSERT INTO topicareas (name) VALUES (:name)"
    db.session.execute(sql, {"name":topicarea_name})
    db.session.commit()    

def get_topicareaname(topicarea_id):
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topicarea_name= result.fetchone()[0]
    return topicarea_name

def count_chains(topicarea_id):
    sql = "SELECT COUNT(*) FROM topicareas WHERE id=:topicareaid and visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topicarea_id})
    count = result.fetchone()[0]
    return count

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
    sql2 = "INSERT INTO messages (topics_id, content, created_at,user_id,visible) VALUES (:topic_id,:content,NOW(),:user_id,TRUE)"
    db.session.execute(sql2, {"topic_id":topic_id,"content":message_content,"user_id":user_id})
    db.session.commit()
    return topic_id 

def get_topicname(topic_id):
    sql="SELECT name FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    topic_name=result.fetchone()[0]
    return topic_name

def view_messages(topicarea_id,topic_id):#views VISIBLE=TRUE messages so far
    "SELECT M.content, U.username, M.created_at FROM messages M, users U WHERE M.user_id=U.id AND topics_id=:topic_id AND visible=TRUE"
    #sql = "SELECT content, created_at, user_id   FROM messages WHERE topics_id=:topic_id and visible=TRUE"
    sql =  "SELECT M.id,M.content, U.username, M.created_at FROM messages M, users U WHERE M.user_id=U.id AND topics_id=:topic_id AND visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topic_id})
    selected_messages= result
    return selected_messages

def count_visiblemessages(topic_id):
    sql = "SELECT COUNT(*) FROM messages WHERE topics_id=:topic_id and visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topic_id})
    count = result.fetchone()[0]
    return count



def count_messages(topicarea_id):
#    sql = "SELECT COUNT(*) FROM messages WHERE topics_id=:topic_id and visible=TRUE"
#    result = db.session.execute(sql, {"topic_id":topic_id})
#    count = result.fetchone()[0]
#    return countdef get_list():count(*)
    sql = "SELECT count(*) FROM messages M, topics T, topicareas A WHERE M.topics_id=T.id and T.topicarea_id=A.id  and A.id=:topicarea_id and M.visible=TRUE"  
    #sql = "SELECT count(*) FROM messages M, Topics T WHERE M.topic_id=T.id and T.id=:topic_id"  
    result = db.session.execute(sql, {"topicarea_id":topicarea_id})
    return result.fetchone()[0]

def new_message(topicarea_id,topic_id,content,user_id):
    sql = "INSERT INTO messages (topics_id, content, created_at,user_id,visible) VALUES (:topic_id,:content,NOW(),:user_id,TRUE)"
    db.session.execute(sql, {"topic_id":topic_id,"content":content,"user_id":user_id})
    db.session.commit()  

def delete_message(message_id):
    sql = "UPDATE messages SET visible = FALSE WHERE id=:message_id"
    db.session.execute(sql,{"message_id":message_id})
    db.session.commit()  

def is_messageowner(message_id):
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql,{"message_id":message_id})
    owner = result.fetchone()[0]
    return owner == users.user_id()
  

        