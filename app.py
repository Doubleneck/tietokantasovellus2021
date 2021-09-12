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
def newtopic(topicarea_id):
    '''new topics get'''
    return render_template("newtopic.html",topicareaid=topicarea_id)

@app.route("/<int:id>/addnewtopic", methods=["POST"])
def addnewtopic(topicarea_id):
    '''add new topics'''
    content = request.form["content"]
    sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:content)"
    db.session.execute(sql, {"content":content,"topicarea_id":topicarea_id})
    db.session.commit()
    return redirect("/"+str(id))


@app.route("/<int:id>")
def topics(topicarea_id):
    '''topics get'''
    sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topics = result.fetchall()
    sql = "SELECT name FROM topicareas WHERE id=:id "
    result = db.session.execute(sql, {"id":topicarea_id})
    topicarea= result.fetchone()[0]
    print(topicarea)
    return render_template("topics.html", count=len(topics), topics=topics, topicareaid=id, topicareaname=topicarea )
