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

@app.route("/<int:id>/newtopic")
def newtopic(id):
    '''new topics get'''
    return render_template("newtopic.html",topicareaid=id)

@app.route("/<int:id>/addnewtopic", methods=["POST"])
def addnewtopic(id):
    '''add new topics'''
    content = request.form["content"]
    sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:content)"
    db.session.execute(sql, {"content":content,"topicarea_id":id})
    db.session.commit()
    return redirect("/"+str(id))

@app.route("/<int:id>")
def topics(id):
    '''topics get'''
    sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "
    result = db.session.execute(sql, {"id":id})
    topics = result.fetchall()
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":id})
    topicarea= result.fetchone()[0]
    return render_template("topics.html", count=len(topics), topics=topics, topicareaid=id, topicareaname=topicarea )

@app.route("/<int:topicarea_id>/<int:topic_id>")  
def messages(topicarea_id,topic_id):
    '''messages get'''
    sql = "SELECT id , content FROM messages WHERE topics_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    messages= result.fetchall()
    sql = "SELECT name FROM topics WHERE id=:topic_id "
    result = db.session.execute(sql, {"topic_id":topic_id})
    topicname= result.fetchone()[0]
    return render_template("topic.html", messages=messages, topicname=topicname)