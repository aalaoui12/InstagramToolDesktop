#!/home/ali/anaconda3/envs/insta_env/bin/python
from flask import Flask, jsonify, request, session
import instagramfollowers as insta
import json
import os

app = Flask(__name__)

driver = None


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        global driver
        driver = insta.startDriver()

        loginInfo = request.get_json(force=True)
        session['user'] = loginInfo["Username"]  # save username to session for further use
        password = loginInfo["Password"]

        loggedIn = insta.login(driver, session['user'], password)
        return jsonify({'logged': loggedIn})


@app.route('/nonfollowers', methods=["GET"])
def getNonFollowers():

    followers = insta.getFollowers(driver, session['user'])
    following = insta.getFollowing(driver, session['user'])

    nonFollowers = insta.getNonFollowers(followers, following)
    insta.quitDriver(driver)  # quit driver on server
    return jsonify(nonFollowers)


app.secret_key = os.urandom(16)
app.run(host='0.0.0.0', debug=True)
