from flask import render_template,redirect,request
from app import app
import visits,users,messages

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    topicareas=messages.get_topicareas()
    return render_template("index.html", counter=counter,
    count=len(topicareas), topicareas=topicareas)

@app.route("/login", methods=["POST"])
def login():
    '''user login'''
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    '''user logout'''
    users.logout()
    return redirect("/")

@app.route("/register")
def view_register():
    '''show user registration form'''
    return render_template("registration.html")

@app.route("/register",methods=["POST"])
def register():
    '''user registration'''
    username = request.form["username"]
    password = request.form["password"]
    #print(users.username_available(username))
    if users.username_available(username):
        users.register(username,password)
        return redirect("/registerok")
    else:
        return redirect("/register")     #Error message missing so far

@app.route("/registerok")
def view_registerok():
    '''show user registration form succeed'''
    return render_template("registerok.html")

@app.route("/newtopicarea", methods=["GET","POST"])
def add_newtopicarea():
    '''Adds new topic areas'''#Change rights: user -> admin
    if request.method == "GET":
        return render_template("newtopicarea.html")
    if request.method == "POST":
        topicarea_name = request.form["content"]
        messages.add_newtopicarea(topicarea_name)
        return redirect("/")

@app.route("/<int:topicarea_id>")
def view_topics(topicarea_id):
    '''topics get'''
    selectedtopics=messages.get_topics(topicarea_id)
    topicarea=messages.get_topicareaname(topicarea_id)
    return render_template ("topics.html", count=len(selectedtopics), topics=selectedtopics,
                            topicareaid=topicarea_id, topicareaname=topicarea)

@app.route("/<int:topicarea_id>/newtopic", methods=["GET","POST"])
def add_newtopic(topicarea_id):
    '''new topic = title for chain of messages'''
    if request.method == "GET":
        return render_template("newtopic.html", topicareaid=topicarea_id)
    if request.method == "POST":
        name= request.form["title"]
        message_content = request.form["content"]
        user_id=users.user_id()
        topic_id=messages.add_newtopic (topicarea_id, user_id,name, message_content)
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))

@app.route("/<int:topicarea_id>/<int:topic_id>")
def view_messages(topicarea_id,topic_id):
    '''messages get'''
    selected_messages=messages.view_messages(topic_id)
    topic_name=messages.get_topicname(topic_id)
    count=messages.count_messages(topic_id)
    return render_template("topic.html", messages=selected_messages, topicareaid=topicarea_id,
                           topicid=topic_id, topicname=topic_name, count=count)

@app.route("/<int:topicarea_id>/<int:topic_id>/addnewmessage", methods=["POST"])
def add_newmessage(topicarea_id,topic_id):
    '''adds new message as a reply to the topic'''
    content = request.form["content"]
    user_id=users.user_id()
    messages.new_message(topicarea_id,topic_id,content,user_id)
    return redirect("/"+str(topicarea_id)+"/"+str(topic_id))

@app.route("/<int:topicarea_id>/<int:topic_id>/<int:message_id>", methods=["POST"])
def delete_message (topicarea_id,topic_id,message_id):
    if messages.is_messageowner(message_id):
        messages.delete_message(message_id)
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
    else:
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
