from datetime import datetime
from db import db
import users

def get_topicareas():
    '''for starting page: counts for messages,chains and lastmessagetime in non-secret topicarea'''
    result = db.session.execute("SELECT id , name FROM topicareas where "
                                "visible=True and secret=False")
    topicareas = result.fetchall()
    list=[]
    for t in topicareas:
        list.append((t[0],t[1],count_messages(t[0]),count_chains(t[0]),last_messagetime(t[0])))
    return list

def add_newtopicarea(topicarea_name):
    '''creates new topicarea, only admin allowed'''
    sql = "INSERT INTO topicareas (name,visible,secret) VALUES (:name,True,False)"
    db.session.execute(sql, {"name":topicarea_name})
    db.session.commit()

def get_secrettopicareas():
    '''for starting page: counts for messages,chains and lastmessagetime in secret topicarea'''
    result = db.session.execute("SELECT id , name FROM topicareas where "
                                "visible=True and secret=True")
    topicareas = result.fetchall()
    list=[]
    for t in topicareas:
        list.append((t[0],t[1],count_messages(t[0]),count_chains(t[0]),last_messagetime(t[0])))
    return list

def add_secrettopicarea(topicarea_name):
    '''creates new secret topicarea, only admin allowed'''
    sql = "INSERT INTO topicareas (name,visible,secret) VALUES (:name,True,True)"
    db.session.execute(sql, {"name":topicarea_name})
    db.session.commit()

def delete_topicarea(topicarea_id):
    '''deletes topicarea, only admin allowed'''
    sql = "UPDATE topicareas SET visible = False where id=:topicarea_id"
    db.session.execute(sql, {"topicarea_id":topicarea_id})
    db.session.commit()

def get_topicareaname(topicarea_id):
    '''name for topicarea'''
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topicarea_name= result.fetchone()[0]
    return topicarea_name

def get_topics(topicarea_id):
    '''all topics in topicarea'''
    sql = "SELECT id , name, user_id FROM topics WHERE topicarea_id=:id and visible=True ORDER BY ID DESC"
    result = db.session.execute(sql, {"id":topicarea_id})
    selected_topics = result.fetchall()
    print("täällä")
    return selected_topics

def add_newtopic (topicarea_id,user_id,topic_name,message_content):
    '''adds new topic, adds also the first message under this topic'''
    sql = ("INSERT INTO topics (topicarea_id,name,user_id,visible) "
           "VALUES (:topicarea_id,:name,:user_id,TRUE) returning id")
    res=db.session.execute(sql, {"name":topic_name,"topicarea_id":topicarea_id,"user_id":user_id})
    topic_id = res.fetchone()[0]
    sql2 = ("INSERT INTO messages (topics_id, content, created_at, user_id, visible) "
            "VALUES (:topic_id, :content, NOW(), :user_id, TRUE)")
    db.session.execute(sql2, {"topic_id":topic_id, "content":message_content,"user_id":user_id})
    db.session.commit()
    return topic_id

def delete_topic(topic_id):
    '''deletes topic, admin , owner allowed'''
    sql = "UPDATE topics SET visible = False where id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()

def edit_topic(topic_id, content):
    '''edit topic, admin, owner allowed'''
    sql = "UPDATE topics SET name=:content where id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id,"content":content})
    db.session.commit()

def is_topicowner(topic_id):
    sql = "SELECT user_id FROM topics where id =:topic_id"
    result = db.session.execute(sql,{"topic_id":topic_id})
    owner = result.fetchone()[0]
    return owner == users.user_id()

def delete_messages(topic_id):
    '''deletes messages by topic id'''
    sql = "UPDATE messages SET visible = FALSE WHERE topics_id=:topic_id"
    db.session.execute(sql,{"topic_id":topic_id})
    db.session.commit()

def new_message(topic_id,content,user_id):
    '''creates new message'''
    sql = ("INSERT INTO messages (topics_id, content, created_at, user_id, visible) "
           "VALUES (:topic_id, :content, NOW(), :user_id, TRUE)")
    db.session.execute(sql, {"topic_id":topic_id, "content":content,"user_id":user_id})
    db.session.commit()

def delete_message(message_id):
    '''deletes message'''
    sql = "UPDATE messages SET visible = FALSE WHERE id=:message_id"
    db.session.execute(sql,{"message_id":message_id})
    db.session.commit()

def edit_message(message_id, new_content):
    '''updates message'''
    sql = "UPDATE messages SET content =:new_content WHERE id=:message_id"
    db.session.execute(sql,{"message_id":message_id,"new_content":new_content})
    db.session.commit()

def get_messagecontent(message_id):
    ''' message content by message id'''
    sql = "Select content from messages WHERE id=:message_id"
    result=db.session.execute(sql,{"message_id":message_id})
    return result.fetchone()[0] 


def get_topicname(topic_id):
    '''returns topic name by id'''
    sql="SELECT name FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    topic_name=result.fetchone()[0]
    return topic_name

def get_topicowner(topic_id):
    '''returns topic name by id'''
    sql="SELECT user_id FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    topic_owner=result.fetchone()[0]
    return topic_owner

def view_messages(topic_id):
    '''views messages with value TRUE in column VISIBILITY'''
    sql = ("SELECT M.id,M.content, U.username, M.created_at, M.user_id FROM messages M, users U "
           "WHERE M.user_id=U.id AND topics_id=:topic_id AND visible=TRUE ORDER BY ID DESC")
    result = db.session.execute(sql, {"topic_id":topic_id})
    selected_messages= result
    return selected_messages

def count_topicmessages(topic_id):
    '''counts visible messages by topic_id'''
    sql = "SELECT COUNT(*) FROM messages WHERE topics_id=:topic_id and visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topic_id})
    count = result.fetchone()[0]
    return count

def is_messageowner(message_id):
    '''checking message´s owner by id'''
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql,{"message_id":message_id})
    owner = result.fetchone()[0]
    return owner == users.user_id()

def last_messagetime(topicarea_id):
    '''returns last message's posting time in topicarea'''
    sql = ("SELECT M.created_at FROM messages M, topics T, topicareas A "
           "WHERE M.topics_id=T.id and T.topicarea_id=A.id and A.id=:topicarea_id "
           "and M.visible=TRUE order by M.created_at DESC")
    result = db.session.execute(sql, {"topicarea_id":topicarea_id})
    ret=result.fetchone()
    if ret == None:
        return datetime.now()
    else:
        return ret[0]

def count_chains(topicarea_id):
    '''counts visible message chains (=topics) of topicarea'''
    sql = ("SELECT count(*) FROM topics T, topicareas A "
           "WHERE T.topicarea_id=A.id and A.id=:topicarea_id and T.visible=TRUE")
    result = db.session.execute(sql, {"topicarea_id":topicarea_id})
    return result.fetchone()[0]

def count_messages(topicarea_id):
    '''counts all visible messages of topicarea'''
    sql = ("SELECT count(*) FROM messages M, topics T, topicareas A WHERE M.topics_id=T.id "
           "and T.topicarea_id=A.id and A.id=:topicarea_id and M.visible=TRUE")
    result = db.session.execute(sql, {"topicarea_id":topicarea_id})
    return result.fetchone()[0]
