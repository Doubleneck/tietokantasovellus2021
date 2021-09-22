from db import db
import users

def get_topicareas():
    '''for starting page: counts for messages,chains and lastmessagetime in every topicarea'''
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    list=[]
    for t in topicareas:
        list.append((t[0],t[1],count_messages(t[0]),count_chains(t[0]),last_messagetime(t[0])))
    return list

def add_newtopicarea(topicarea_name):#TO BE CHANGED ADMIN ONLY
    '''creates new topicarea'''
    sql = "INSERT INTO topicareas (name) VALUES (:name)"
    db.session.execute(sql, {"name":topicarea_name})
    db.session.commit()

def get_topicareaname(topicarea_id):
    '''name for topicarea'''
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topicarea_name= result.fetchone()[0]
    return topicarea_name

def count_chains(topicarea_id):
    '''counts message chains intopicarea'''
    sql = "SELECT COUNT(*) FROM topicareas WHERE id=:topicareaid and visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topicarea_id})
    count = result.fetchone()[0]
    return count

def get_topics(topicarea_id):
    '''all topics in topicarea'''
    sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    selected_topics = result.fetchall()
    return selected_topics

def add_newtopic (topicarea_id,user_id,topic_name,message_content):
    '''adds new topic, adds also the first message under this topic'''
    sql = ("INSERT INTO topics (topicarea_id,name,user_id,visible)"
           " VALUES (:topicarea_id,:name,:user_id,TRUE) returning id")
    res=db.session.execute(sql, {"name":topic_name,"topicarea_id":topicarea_id,"user_id":user_id})
    topic_id = res.fetchone()[0]
    db.session.commit()
    sql2 = ("INSERT INTO messages (topics_id, content, created_at,user_id,visible)"
            "VALUES (:topic_id,:content,NOW(),:user_id,TRUE)")
    db.session.execute(sql2, {"topic_id":topic_id,"content":message_content,"user_id":user_id})
    db.session.commit()
    return topic_id 

def get_topicname(topic_id):
    '''returns topic name by id'''
    sql="SELECT name FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    topic_name=result.fetchone()[0]
    return topic_name

def view_messages(topic_id):
    '''views messages with value TRUE in column VISIBILITY'''
    sql =  "SELECT M.id,M.content, U.username, M.created_at FROM messages M, users U WHERE M.user_id=U.id AND topics_id=:topic_id AND visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topic_id})
    selected_messages= result
    return selected_messages

def count_messages(topic_id):
    '''counts visible messages by topic_id'''
    sql = "SELECT COUNT(*) FROM messages WHERE topics_id=:topic_id and visible=TRUE"
    result = db.session.execute(sql, {"topic_id":topic_id})
    count = result.fetchone()[0]
    return count

def last_messagetime(topicarea_id):
    '''returns last message's posting time in topicarea'''
    sql = "SELECT M.created_at FROM messages M, topics T, topicareas A WHERE M.topics_id=T.id and T.topicarea_id=A.id and A.id=:topicarea_id and M.visible=TRUE order by M.created_at DESC"  
    result = db.session.execute(sql, {"topicarea_id":topicarea_id}) 
    print(result.fetchone())
    return result.fetchone()

def count_chains(topicarea_id):
    sql = "SELECT count(*) FROM topics T, topicareas A WHERE T.topicarea_id=A.id  and A.id=:topicarea_id"  #PUUTTUU TOPIC VISIBLE
    result = db.session.execute(sql, {"topicarea_id":topicarea_id}) 
    return result.fetchone()[0]

def count_messages(topicarea_id):
    sql = "SELECT count(*) FROM messages M, topics T, topicareas A WHERE M.topics_id=T.id and T.topicarea_id=A.id  and A.id=:topicarea_id and M.visible=TRUE"  
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
  
#def search_messages(query):        
#    sql = "SELECT id, content FROM messages WHERE content LIKE :query"
#    result = db.session.execute(sql, {"query":"%"+query+"%"})
#    messages = result.fetchall()
    
#    return messages