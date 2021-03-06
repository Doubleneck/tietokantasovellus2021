from os import abort
from flask import render_template,redirect,request,flash,session
from app import app
import visits,users,messages,utils
import secrets

@app.route("/")
def index():
    try:         
        logged_user = users.username()
        visitscounter = visits.get_counter()
        topic_areas = messages.get_topicareas()
        secret_topicareas = []
        if users.is_admin() or users.is_puser:
            secret_topicareas = messages.get_secrettopicareas()
            return render_template("index.html", counter = visitscounter, logged = logged_user,
            count = len(topic_areas), topicareas = topic_areas, secretareas = secret_topicareas)
    except:
        return render_template("index.html")

@app.route("/login", methods = ["POST"])
def login():
    '''user and admin login'''
    username = request.form["username"]   
    password = request.form["password"]
    if users.login(username, password):
        session["csrf_token"] = secrets.token_hex(16)
        visits.add_visit()
        return redirect("/")
    else:
        flash("Käyttäjätunnus tai salasana ei täsmää, muistithan isot ja pienet kirjaimet?","error")
        return redirect(request.referrer)

@app.route("/logout")
def logout():
    '''user logout'''
    try:
        users.logout()
        return redirect("/")
    except:        
        return redirect("/")

@app.route("/register")
def view_register():
    '''show user registration form'''
    return render_template("registration.html")

@app.route("/register",methods = ["POST"])
def register():
    '''user registration'''
    username = request.form["username"]
    password = request.form["password"]
    if utils.validate_username(username):
        if users.username_available(username):
            if utils.validate_password(password):
                users.register(username,password)
                return redirect("/registerok")
            else:
                flash("Salasana saa sisältää vain kirjaimia (ei skandeja) " 
                      "ja numeroita, ja sen pitää olla vähintää 6 merkkiä pitkä","error")
                return redirect(request.referrer)     
        else:
            flash("Käyttäjätunnus on varattu","error") 
            return redirect(request.referrer)   
    else:
        flash("Käyttäjätunnus saa sisältää vain kirjaimia (ei skandeja) ja numeroita, "
            " ja sen pitää olla vähintää 6 merkkiä pitkä","error") 
        return redirect(request.referrer)

@app.route("/admin")
def admin_page():
    try:
        users_list = users.users()
        pusers_list = users.pusers()
        if users.is_admin():
            return render_template("admin.html", users = users_list, pusers = pusers_list)
        else:
            return "Ei oikeutta nähdä sivua"
    except:
        return "Not allowed"

@app.route("/registerok")
def view_registerok():
    '''show user registration form succeed'''
    return render_template("registerok.html")

@app.route("/newtopicarea", methods = ["GET","POST"])
def add_newtopicarea():
    '''Adds new topic areas'''
    try:
        if users.is_admin():
            if request.method == "GET":
                return render_template("newtopicarea.html")               
            if request.method == "POST":
                if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
                topicarea_name = request.form["content"]
                messages.add_newtopicarea(topicarea_name)
                return redirect("/")
        else:
            return redirect("/")
    except:
        return "Not allowed"

@app.route("/newsecrettopicarea", methods = ["GET","POST"])
def newsecret_area():
    '''Adds new secret topic areas'''
    try:
        if users.is_admin():
            if request.method == "GET":
                return render_template("newtopicarea.html")
            if request.method == "POST":
                if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
                topicarea_name = request.form["secretcontent"]
                messages.add_secrettopicarea(topicarea_name)
                return redirect("/")
        else:
            return redirect("/")
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>")
def view_topics(topicarea_id):
    '''topics get'''
    try:
        selectedtopics = messages.get_topics(topicarea_id)
        topicarea = messages.get_topicareaname(topicarea_id)
        return render_template ("topics.html", count = len(selectedtopics), topics = selectedtopics,
                                topicareaid = topicarea_id, topicareaname = topicarea)
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/newtopic", methods = ["GET","POST"])
def add_newtopic(topicarea_id):
    '''add new topic = title for chain of messages & first message'''
    try:
        if request.method == "GET":
            return render_template("newtopic.html", topicareaid = topicarea_id)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
            name = request.form["title"]
            message_content = request.form["content"]
            if utils.validate_topic(name):
                if utils.validate_message(message_content):                
                    user_id = users.user_id()
                    topic_id = messages.add_newtopic (topicarea_id, user_id, name, message_content)
                    return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
                else:
                    flash("Sallittu viestin koko on 3-200 merkkiä","error")
                return redirect(request.referrer)     
            else:
                flash("Keskusteluotsikon sallittu koko on 10-70 merkkiä","error")
                return redirect(request.referrer)                    
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/<int:topic_id>")
def view_messages(topicarea_id,topic_id):
    '''messages get'''
    try:
        topic_user_id = messages.get_topicowner(topic_id)
        selected_messages = messages.view_messages(topic_id)
        topic_name = messages.get_topicname(topic_id)
        return render_template("topic.html", messages = selected_messages, topicareaid = topicarea_id,
                               topicid = topic_id, topicname = topic_name, topicuserid = topic_user_id)
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/<int:topic_id>/addnewmessage", methods = ["POST"])
def add_newmessage(topicarea_id,topic_id):
    '''adds new message as a reply to the topic'''
    try:
        content = request.form["content"]
        user_id = users.user_id()
        if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
        if utils.validate_message(content):
            messages.new_message(topic_id,content,user_id)
            return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
        else:
            flash("Sallittu viestin koko on 3-200 merkkiä","error")
            return redirect(request.referrer)   
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/<int:topic_id>/delete", methods = ["POST"])
def delete_topic(topicarea_id,topic_id):
    '''deletes topic (owner or admin)'''
    if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
    messages.delete_messages(topic_id)
    messages.delete_topic(topic_id)
    return redirect("/"+str(topicarea_id))

@app.route("/<int:topicarea_id>/<int:topic_id>/edit", methods = ["GET"])
def view_edit_topic(topicarea_id,topic_id):
    topicname = messages.get_topicname(topic_id)
    return render_template("renametopic.html", topicareaid = topicarea_id, topicid = topic_id, topicname = topicname)

@app.route("/<int:topicarea_id>/<int:topic_id>/edit", methods = ["POST"])
def edit_topic(topicarea_id,topic_id):
    '''edit topic = messages title (owner or admin)'''
    if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
    content = request.form["content"]
    if utils.validate_topic(content):
        messages.edit_topic(topic_id, content)
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
    else:
        flash("Keskusteluotsikon sallittu koko on 10-70 merkkiä","error")
        return redirect(request.referrer) 

@app.route("/<int:topicarea_id>/<int:topic_id>/<int:message_id>", methods = ["POST"])
def delete_message (topicarea_id,topic_id,message_id):
    '''deletes message'''
    try:
        if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
        if messages.is_messageowner(message_id) or users.is_admin():
            messages.delete_message(message_id)
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/<int:topic_id>/<int:message_id>/edit", methods = ["GET"])
def view_edit_message (topicarea_id,topic_id,message_id):
    '''shows page for editing message'''
    content = messages.get_messagecontent(message_id)
    return render_template("editmessage.html", topicareaid = topicarea_id,topicid = topic_id, messageid = message_id, content = content)

@app.route("/<int:topicarea_id>/<int:topic_id>/<int:message_id>/edit", methods = ["POST"])
def edit_message (topicarea_id,topic_id,message_id):
    '''handles form for editing message'''
    try:
        if session["csrf_token"] != request.form["csrf_token"]:            
                    abort(403) 
        if messages.is_messageowner(message_id) or users.is_admin():
            new_content = request.form["content"]
            if utils.validate_message(new_content):
                messages.edit_message(message_id,new_content)
            else:
                flash("Sallittu viestin koko on 3-200 merkkiä","error")
                return redirect(request.referrer)
        return redirect("/"+str(topicarea_id)+"/"+str(topic_id))
    except:
        return "Not allowed"

@app.route("/<int:topicarea_id>/<int:topic_id>/result/")
def result(topicarea_id,topic_id):
    '''search function'''
    try:
        query = request.args["query"]
        messagelist = messages.search_messages(query, topic_id)
        return render_template("result.html", messages = messagelist,
                               topicareaid = topicarea_id, topicid = topic_id)
    except:
        return "Not allowed"

@app.route("/admin/users/<int:user_id>/", methods = ["POST"])
def add_puser(user_id):
    '''adds access to secret areas'''    
    if session["csrf_token"] != request.form["csrf_token"]:            
        abort(403) 
    users.add_puser(user_id)
    return redirect("/admin")

@app.route("/admin/pusers/<int:user_id>/", methods = ["POST"])
def remove_puser(user_id):
    if session["csrf_token"] != request.form["csrf_token"]:            
        abort(403) 
    users.remove_puser(user_id)
    return redirect("/admin")

@app.route("/admin/remove/<int:topicarea_id>/", methods = ["POST"])
def remove_topicarea(topicarea_id):
    try:
        if session["csrf_token"] != request.form["csrf_token"]:            
            abort(403) 
        if users.is_admin():
            messages.delete_topicarea(topicarea_id)
            return redirect("/")
        else:
            return "ei sallittu"
    except:
        return "Not allowed"
