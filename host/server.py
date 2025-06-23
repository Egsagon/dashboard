import flask
import flask_socketio

from . import utils

app = flask.Flask('run', static_folder = 'app/', static_url_path = '')
socket = flask_socketio.SocketIO(app, async_mode = 'threading')
polls: dict[str, utils.Poll] = {}

@app.before_request
def check_http():
    if not flask.request.remote_addr in utils.config['whitelist']:
        print('Unauthorized IP:', flask.request.remote_addr)
        flask.abort(401)

@socket.on('connect')
def check_socket():
    if not flask.request.remote_addr in utils.config['whitelist']:
        print('Unauthorized IP in sockets:', flask.request.remote_addr)
        flask_socketio.disconnect(flask.request.sid)

@app.route('/')
def serve():
    # Serve a dashboard

    utils.refresh_config()
    board = flask.request.args.get('board', utils.config['default'])

    if board not in utils.config['boards']:
        return flask.send_file('app/404.html')

    return utils.build(board)

@socket.on('start')
def poll(tasks: dict[int, dict]):
    # Start a poll

    sid: str = flask.request.sid

    polls[sid] = utils.poll(tasks, lambda r: socket.emit('poll', r, to = sid))
    return 'ok'

@socket.on('ping')
def ping():
    # Ensures frontend cares about polls

    sid: str = flask.request.sid

    # Tell frontend to restart a poll because it is too old
    if not sid in polls: return 'no'

    # Ping poll
    polls[sid].ping()
    return 'ok'

@socket.on('exec')
def execute(command: str):
    # Execute a command

    return utils.run(command)

@socket.on('disconnect')
def cleanup():
    # Cleanup poll on disconnect

    if poll := polls.get(flask.request.sid):
        poll.stop()

def run(host: str = None, port: int = None) -> None:
    # Run the server

    socket.run(app, host, port, debug = False, log_output = False)

# EOF