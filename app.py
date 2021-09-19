'''the main app'''
from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    '''all topic areas, starting page'''
    result = db.session.execute("SELECT id , name FROM topicareas")
    topicareas = result.fetchall()
    return render_template("index.html", count=len(topicareas), topicareas=topicareas)

@app.route("/login",methods=["POST"])
def login():
    '''user login'''
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    
    if not user:
        # TODO: invalid username
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            # TODO: invalid password
            return redirect("/")

        

@app.route("/logout")
def logout():
    '''user logout'''
    del session["username"]
    return redirect("/")    

@app.route("/register")
def register():
    '''user registration form GET'''   
    return render_template("registration.html")


@app.route("/registeruser",methods=["POST"])
def registeruser():
    '''user registration'''
    username = request.form["username"]
    password = request.form["password"]

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/") 

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
    name= request.form["title"]
    sql = "INSERT INTO topics (topicarea_id,name) VALUES (:topicarea_id,:name) returning id"
    result=db.session.execute(sql, {"name":name,"topicarea_id":topicrea_id})
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
    return render_template("topics.html", count=len(selectedtopics), topics=selectedtopics,
    topicareaid=topicrea_id, topicareaname=topicarea )

@app.route("/<int:topicarea_id>/<int:topic_id>")
def messages(topicarea_id,topic_id):
    '''messages get'''
    sql = "SELECT content FROM messages WHERE topics_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    selectedmessages= result
    sql = "SELECT name FROM topics WHERE id=:topic_id "
    result = db.session.execute(sql, {"topic_id":topic_id})
    topicname= result.fetchone()[0]
    return render_template("topic.html", messages=selectedmessages,topicareaid=topicarea_id,topicid=topic_id, topicname=topicname)


@app.route("/<int:topicarea_id>/<int:topic_id>/addnewmessage", methods=["POST"])
def addnewmessage(topicarea_id,topic_id):
    '''adds new message as a reply to the topic'''
    content = request.form["content"]
    sql = "INSERT INTO messages (topics_id, content) VALUES (:topic_id,:content)"
    db.session.execute(sql, {"topic_id":topic_id,"content":content})
    db.session.commit()
    return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
