'''the main app'''
from os import getenv
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    '''all topic areas, so far in the root'''
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    return render_template("index.html", count=len(topicareas), topicareas=topicareas)

@app.route("/newtopicarea")
def newtopicarea():
    '''Path for creating new topic areas (admin only'''
    return render_template("newtopicarea.html")

@app.route("/addnewtopicarea", methods=["POST"])
def addnewtopicarea():
    '''Adds new topic areas'''
    content = request.form["content"]
    sql = "INSERT INTO topicareas (name) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/<int:topicrea_id>/newtopic")
def newtopic(topicrea_id):
    '''new topics get'''
    return render_template("newtopic.html",topicareaid=topicrea_id)

@app.route("/<int:topicrea_id>/addnewtopic", methods=["POST"])
def addnewtopic(topicrea_id):
    '''adds new topic, also adds the first message to the topic chain'''
    title = request.form["title"]
    sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:title) returning id"
    result=db.session.execute(sql, {"title":title,"topicarea_id":topicrea_id})
    topic_id = result.fetchone()[0]
    print(topic_id)
    db.session.commit()
    content = request.form["content"]#tämä laitetaan MENEMÄÄN ekaks messageksi TARVITAAN TOPIC ID
    sql = "INSERT INTO messages (topics_id,content) VALUES (:topic_id,:content)"
    db.session.execute(sql, {"content":content,"topic_id":topic_id})
    db.session.commit()
    return redirect("/"+str(topicrea_id)+"/"+str(topic_id))

@app.route("/<int:topicrea_id>")
def topics(topicrea_id):
    '''topics get'''
    sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "
    result = db.session.execute(sql, {"id":topicrea_id})
    selectedtopics = result.fetchall()
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicrea_id})
    topicarea= result.fetchone()[0]
    return render_template("topics.html", count=len(topics), topics=selectedtopics,
    topicareaid=topicrea_id, topicareaname=topicarea )

@app.route("/<int:topicarea_id>/<int:topic_id>")
def messages(topic_id):
    '''messages get'''
    sql = "SELECT id , content FROM messages WHERE topics_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    selectedmessages= result.fetchall()
    sql = "SELECT name FROM topics WHERE id=:topic_id "
    result = db.session.execute(sql, {"topic_id":topic_id})
    topicname= result.fetchone()[0]
    return render_template("topic.html", messages=selectedmessages, topicname=topicname)

@app.route("/<int:topicarea_id>/<int:topic_id>/addnewmessage", methods=["POST"])
def addnewmessage(topicarea_id,topic_id):
    '''adds new message as a reply to the topic'''
    content = request.form["content"]#tämä laitetaan ekaks messageksi
 #   sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:title) RETURNING id"
 #   result=db.session.execute(sql, {"title":title,"topicarea_id":topicarea_id})
 #   topic_id = result.fetchone()[0]
 #   db.session.commit()
    print(content)
    #sql = "INSERT INTO messages (topics_id,content) VALUES (:topicarea_id,:title)"
    #db.session.execute(sql, {"content":content,"topics_id":})
 #   db.session.commit()
    return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
