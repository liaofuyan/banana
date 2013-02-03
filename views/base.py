#!/usr/bin/env python
# -*- coding:utf-8  -*-

from flask import session, Flask, abort
import config

def currentUserGet():
    if "user" in session:
        user = session["user"]
        return user["username"]
    else:
        return None

def isAdmin():
    return currentUserGet() == config.ADMIN_USER

def userAuth(username,password):
    return username == config.ADMIN_USER and password == config.ADMIN_PASSWORD

def currentUserSet(username):
    if username:
        session["user"] = dict({"username":username})
    else:
        session.pop("user",None)

def checkAdmin():
    if not isAdmin():
        abort(404)

def replyerGet():
    if "replyer" in session:
        reply = session["replyer"]
        name = reply["name"]
        return name
    else:
        return None

