import flask
import logging
import flask_socketio

from . import utils

logger = logging.getLogger('server')
app = flask.Flask('run', static_folder = 'app/', static_url_path = '')
socket = flask_socketio.SocketIO(app, async_mode = 'eventlet')

@socket.on('connect')
def wss_auth(auth: str):
    # Check socket connections

    if auth['token'] != utils.config['token']:
        flask_socketio.disconnect(flask.request.sid)

@app.before_request
def http_auth():
    # Check HTTP connections

    allowed_pathes = ('/', '/auth', '/assets/icon.svg')

    if flask.request.cookies.get('token') != utils.config['token'] and not flask.request.path in allowed_pathes:
        flask.abort(401)

@app.after_request
def log_request(response: flask.Response):
    # handle HTTP logging

    logger.info(f'{flask.request.method} {flask.request.remote_addr} > {flask.request.url}: {response.status_code}')
    return response

@app.route('/')
def serve():
    # Serve a dashboard

    if flask.request.cookies.get('token') != utils.config['token']:
        return flask.redirect('/auth')

    utils.refresh_config()
    board = flask.request.args.get('b', utils.config['default'])

    if board not in utils.config['boards']:
        return flask.send_file('app/404.html')

    return utils.build(board)

@app.route('/auth')
def auth():
    # Serve the auth page
    
    return flask.send_file('app/auth.html')

@socket.on('start')
def poll(tasks: dict[int, dict]):
    # Start a poll

    sid: str = flask.request.sid

    socket.start_background_task(
        utils.poller, sid, tasks,
        lambda r: socket.emit('poll', r, to = sid)
    )
    return 'ok'

@socket.on('ping')
def ping():
    # Ensures frontend cares about polls

    sid: str = flask.request.sid

    # Tell frontend to restart a poll because it is too old
    if not sid in utils.polls: return 'no'

    # Ping poll
    utils.polls[sid].send('ping')
    return 'ok'

@socket.on('exec')
def execute(command: str):
    # Execute a command

    return utils.eventlet.tpool.execute(utils.run, command)

@socket.on('disconnect')
def cleanup():
    # Cleanup poll on disconnect

    if event := utils.polls.get(flask.request.sid):
        event.send('stop')

# EOF