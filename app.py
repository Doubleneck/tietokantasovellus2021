from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    return render_template("index.html", count=len(topicareas), topicareas=topicareas) 

@app.route("/newtopicarea")
def newtopicarea():
    return render_template("newtopicarea.html")

@app.route("/<int:id>/newtopic") 
def newtopic(id):  
    return render_template("newtopic.html",topicareaid=id)    

@app.route("/addnewtopicarea", methods=["POST"]) #TÄMÄ VAIN ADMINILLE: AIHEPIIRIEN LISÄÄMINEN
def addnewtopicarea():
    content = request.form["content"]
    sql = "INSERT INTO topicareas (name) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/<int:id>/addnewtopic", methods=["POST"])                 # UUDEN KESKUSTELUN LISÄÄMINEN
def addnewtopic(id):
    content = request.form["content"]
    topicarea_id=id
    sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:content)"
    db.session.execute(sql, {"content":content,"topicarea_id":topicarea_id})
    db.session.commit()
    return redirect("/"+str(id))


@app.route("/<int:id>") #KESKUSTELUKETJUT GET
def topics(id):
    sql = "SELECT id , name FROM topics WHERE topicarea_id=:id "  
    result = db.session.execute(sql, {"id":id})
    topics = result.fetchall()
    sql = "SELECT name FROM topicareas WHERE id=:id "  
    result = db.session.execute(sql, {"id":id})
    topicarea= result.fetchone()[0]
    print(topicarea)
    return render_template("topics.html", count=len(topics), topics=topics, topicareaid=id, topicareaname=topicarea )    



