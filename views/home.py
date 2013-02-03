#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint,Flask,request,session,g,redirect
from flask import render_template, abort
from helpers import *
from pymongo import DESCENDING,ASCENDING
from bson.objectid import ObjectId
import config
import base
import markdown
import time
home = Blueprint("home", __name__)

@home.route("/", defaults = {"page":1})
@home.route("/<page>")
@home.route("/page/<page>")
def index(page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page <= 0:
        return "FUCK YOU!"
    count = config.post.find().count()
    page_count = (count + config.BLOG_PERPAGE - 1) / config.BLOG_PERPAGE
    recent_replys = config.reply.find().sort("craeted_date" , ASCENDING).limit(6)
    posts = config.post.find().sort("created_date",ASCENDING).skip((page - 1)*config.BLOG_PERPAGE).limit(config.BLOG_PERPAGE)
    return render_template("home.html" , replyContent = replyContent ,getAvatar = getAvatar, recent_replys = recent_replys , \
                           getDay = getDay , getMonth = getMonth , formatDate = formatDate , formatDate2 = formatDate2 , \
                           posts = posts , showPost = showPost ,page_count = page_count ,page = page)


@home.route("/archive")
@home.route("/archive/page/<page>")
def list_archive(page = 1):
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page <= 0 :
        return "FUCK YOU!"
    count = config.post.find().count()
    page_count = (count + config.BLOG_PERARCHIVE - 1) / config.BLOG_PERARCHIVE
    posts = config.post.find().sort("created_date",ASCENDING).skip((page - 1)*config.BLOG_PERARCHIVE).limit(config.BLOG_PERARCHIVE)
    return render_template("archive.html",page_count = page_count,page = page,posts = posts , formatDate2 = formatDate2 , getAvatar = getAvatar)

@home.route("/login", methods = ["GET" , "POST"])
def login():
    if request.method == "GET":
        if base.isAdmin():
            return redirect("/")
        else:
            return render_template("login.html",getAvatar = getAvatar)

    username = request.form["username"]
    password = request.form["password"]
    if base.userAuth(username,password):
        base.currentUserSet(username)
        return redirect("/")
    else:
        return redirect("/login")

@home.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

@home.route("/post/add", methods=["GET", "POST"])
def add_post():
    if request.method == "GET":
        base.checkAdmin()
        return render_template("postadd.html",getAvatar = getAvatar)

    base.checkAdmin()
    title = request.form["post[title]"]
    origin_content = request.form["post[content]"]
    content = markdown.markdown(origin_content)
    if title != "" and origin_content != "":
        config.post.insert({"title":title,"content":content,"origin_content":origin_content,"created_date":time.time(),"update_date":time.time()})
        return redirect("/")
    else:
        return render_template("postadd.html", getAvatar = getAvatar, error = u"标题或内容不能为空")

@home.route("/post/<pid>")
def show_post(pid):
    replyer = base.replyerGet()
    if replyer is None:
        replyer = {}
        replyer["name"] = ""
        replyer["email"] = ""
        replyer["website"] = ""
    if base.currentUserGet():
        replyer = {}
        replyer["name"] = config.ADMIN_USERNAME
        replyer["email"] = config.ADMIN_EMAIL
        replyer["website"] = config.BLOG_URL
    id = ObjectId(pid)
    posts = config.post.find({"_id":id})
    for i in posts:
        post = i
    if type(post) != type({}): abort(404)
    replys = config.reply.find({"pid":pid})
    replys_count = replys.count()
    return render_template("post.html", post = post ,formatDate = formatDate, \
                    formatDate2 = formatDate2 ,getAvatar = getAvatar , replyer = replyer,
                    replys = replys ,replys_count = replys_count)
   


@home.route("/reply/<pid>/add" , methods = ["POST"])
def add_reply(pid):
    name = request.form["reply[name]"]
    email = request.form["reply[email]"]
    website = request.form["reply[website]"]
    origin_content = request.form["reply[content]"]
    content = markdown.markdown(formatText(origin_content))
    if name == "":
        return redirect("/post/%s" % pid ,error = u"请输入名字")
    if email == "":
        return redirect("/post/%s" % pid ,error = u"请输入邮箱")
    if origin_content == "":
        return redirect("/post/%s" % pid ,error = u"请输入评论内容")
    config.reply.insert({"number":int(config.reply.find({"pid":pid}).count()) + 1,"name":name,"email":email,"website":website,"content":content,"origin_content":origin_content,"pid":pid,"created_date":time.time()})
    return redirect("/post/%s" % pid)

@home.route("/post/edit/<pid>",methods = ["GET","POST"])
def edit_post(pid):
    if request.method == "GET":
        base.checkAdmin()
        post = None
        for i in config.post.find({"_id":ObjectId(pid)}):
            post = i
        if post is None:
            abort(404)
        return render_template("postedit.html",post = post, getAvatar = getAvatar)
        
    base.checkAdmin()
    title = request.form["post[title]"]
    origin_content = request.form["post[content]"]
    content = markdown.markdown(origin_content)
    if title != "" and origin_content != "":
        for i in config.post.find({"_id":ObjectId(pid)}):
            post = i
        post["title"] = title
        post["origin_content"] = origin_content
        post["content"] = content
        config.post.update({"_id":ObjectId(pid)},post)
        return redirect("/post/%s" % pid)
    else:
        return render_template("postedit.html",error=u"标题或内容不能为空",getAvatar = getAvatar)

