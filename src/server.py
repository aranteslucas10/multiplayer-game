import json
from threading import Thread
from time import sleep

from flask import Flask, request
from flask.templating import render_template
from flask_socketio import SocketIO, send, emit
import socketio

from game import Game

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

game = Game(screen_width=20, screen_height=20)

def command_broadcast(command: dict):
    print(f"> Emitting {command['type']}")
    emit(command['type'], command, broadcast=True)

    
game.subscribe(command_broadcast)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    player_id = request.sid
    game.add_player(player_id=player_id)
    game.add_fruit()
    emit('setup', game.state)


@socketio.on('disconnect')
def handler_disconnect():
    game.remove_player(request.sid)


@socketio.on('move-player')
def hanlder_move_player(command):
    game.player_action(player_id=request.sid, action=command['keyPressed'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
