# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

connected_users = {}

@app.route('/chat/fadillah')
def chat_fadillah():
    return render_template('chat.html', user='Fadillah')

@app.route('/chat/amar')
def chat_amar():
    return render_template('chat.html', user='Amar')

@socketio.on('connect')
def handle_connect():
    user_id = request.sid
    connected_users[user_id] = request.sid
    print(f"User {user_id} connected")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    del connected_users[user_id]
    print(f"User {user_id} disconnected")

@socketio.on('message')
def handle_message(data):
    sender_id = request.sid
    message = data['message']
    sender_name = data['sender_name']

    emit('message', {'sender': sender_name, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
