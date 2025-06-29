import re
import time
import json
import yaml
import logging
import subprocess

import eventlet
import eventlet.tpool

def refresh_config() -> None:
    '''
    Refresh the server configuration.
    '''

    global config
    with open('config.yml') as file:
        config = yaml.safe_load(file)

def build(name: str) -> str:
    '''
    Build a custom dashboard.
    '''

    CONF_ANCHOR = '<!-- CONFIG -->'
    CELL_ANCHOR = '<!-- MODULES -->'
    
    board = config['boards'][name]

    with open('app/index.html', encoding = 'utf-8') as file:
        page = file.read()
    
    # Insert board config for frontend
    page = page.replace(CONF_ANCHOR, f'<script>const config={json.dumps(config)}, board="{name}"</script>')
    
    # Insert modules
    for module in board['modules'][::-1]:
        with open(f'cells/{module["name"]}.html', encoding = 'utf-8') as file:
            page = page.replace(CELL_ANCHOR, CELL_ANCHOR + file.read())
    
    return page

def _run(command: str) -> list[int, str]:
    '''
    Runs a shell command in a PS context.
    '''

    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            creationflags = subprocess.CREATE_NO_WINDOW
        )

        text = result.stdout if result.returncode <= 0 else result.stderr
        return [result.returncode, text.strip()]

    except Exception as err:
        return [1, repr(err)]

def run(command: str) -> list[int, str]:
    '''
    Wraps _run with caching behavior.
    '''

    cached = command.startswith('[cache')
    frame = time.time()

    if cached:
        cache, command = re.findall(r'\[cache=(\d+?)\]\s?(.*)', command)[0]
        capture = poll_cache.get(command)

        if capture and frame - capture[0] < config['refresh_rate'] * int(cache):
            return capture[1]
    
    if cached:
        print('REFRESHING CACHE')

    response = _run(command)

    if cached:
        poll_cache[command] = (frame, response)
    
    return response

def poller(sid: str, tasks: dict[int, str], callback: callable) -> None:
    '''
    Create an eventlet shell poll.
    '''

    if event := polls.get(sid):
        logger.info(f'Killing precedant poller for {sid}')
        event.send()
    
    event = polls[sid] = eventlet.Event()
    ping = time.time()

    while 1:
        frame = time.time()

        # Check for new events
        if event.has_result():
            if event.wait() == 'ping':
                ping = frame
                event.reset()
            else:
                logger.info(f'Killed poll {sid}')
                break
        
        # Verify client is alive
        if frame - ping > 60:
            return logger.warning(f'Destroying abandonned poller {sid}')

        # Start all tasks
        threads = {
            tid: eventlet.spawn(eventlet.tpool.execute, run, task['command'])
            for tid, task in tasks.items()
        }

        # Send output
        callback({tid: task.wait() for tid, task in threads.items()})

        cycle = time.time() - frame
        if cycle > config['refresh_rate']:
            logger.warning('Cycle behind, forcing poll restart')
            cycle = 0
        
        # Wait for next cycle
        eventlet.sleep(config['refresh_rate'] - cycle)

logger = logging.getLogger('runner')
config: dict = None
refresh_config()

poll_cache: dict[str, tuple[int, list[int, str]]] = {}
polls: dict[str, eventlet.Event] = {}

# EOF