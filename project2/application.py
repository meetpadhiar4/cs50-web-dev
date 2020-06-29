from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask import Flask, render_template, request, session
from flask_session import Session
from collections import deque
import os

from time import localtime, strftime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

channels = []
users = []
channelMsgs = dict()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    session.clear()
    name = request.form.get("name")
    session["user_id"] = name
    users.append(name)
    return render_template('home.html', name=session['user_id'], channels=channels)


@app.route("/channel", methods=["POST"])
def channel():
    channelname = request.form.get("channelname")
    channels.append(channelname)
    channelMsgs[channelname] = []
    return render_template('home.html', name=session["user_id"], channels=list(dict.fromkeys(channels)), messages=channelMsgs[channelname])


@socketio.on('message')
def message(data):
    print(f"\n\n{data['channel']}\n\n")
    room = session.get('current_channel')
    print(room)
    channelMsgs[room[1:]].append([
        session.get('user_id'), strftime('%I:%M %p', localtime()), data['msg']])
    print(channelMsgs[room[1:]])
    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%I:%M %p', localtime())}, room=data['channel'])


@socketio.on('join')
def join(data):
    join_room(data['channel'])
    session['current_channel'] = data['channel']
    send({'msg': data['username'] + " has joined the " +
          data['channel'] + " channel."}, room=data['channel'])


@socketio.on('leave')
def leave(data):
    leave_room(data['channel'])
    send({'msg': data['username'] + " has left the " +
          data['channel'] + " channel."}, room=data['channel'])


if __name__ == "__main__":
    socketio.run(app, debug=True)
