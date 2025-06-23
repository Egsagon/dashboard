import time
import yaml
import json
import typing
import threading
import subprocess
import dataclasses

def refresh_config() -> None:
    '''
    Refresh the server configuration.
    '''

    global config

    with open('config.yml') as file:
        config = yaml.safe_load(file)

config: dict = None
refresh_config()

@dataclasses.dataclass
class Poll:
    process: threading.Thread = None
    event: threading.Event = dataclasses.field(default_factory = threading.Event)
    pinged: float = dataclasses.field(default_factory = time.time)

    def start(self, target: typing.Callable) -> None:
        '''
        Start the internal thread.
        '''

        self.event.clear()
        self.process = threading.Thread(target = target, daemon = True)
        self.process.start()
    
    def stop(self) -> None:
        '''
        Gracefully stops the thread.
        '''

        self.event.set()
    
    def ping(self) -> None:
        '''
        Inform the threads that it should not die.
        '''

        self.pinged = time.time()

def poll(tasks: dict[int, dict], callback: typing.Callable) -> Poll:
    '''
    Create a new poll.
    [[ Spaguetti code alert ]]
    '''

    p = Poll()

    def loop() -> None:
        while not p.event.is_set():

            cycle_start = time.time()

            # Check if poll is unpinged
            if time.time() - p.pinged > 60:
                print('Warning: Closing unpinged poll', p.process.native_id)
                return p.stop()

            # Execute commands
            output = {}
            lock = threading.Lock()
            threads: list[threading.Thread] = []

            # Start each command run in a separate thread
            for tid, task in tasks.items():
                def wrap(t, c):
                    result = run(c)
                    with lock: output[t] = result
                
                thread = threading.Thread(target = wrap, args = [tid, task['command']] , daemon = True)
                threads.append(thread)
                thread.start()
            
            # Wait for all command threads to resolve
            for thread in threads:
                thread.join()
            
            # Send results back
            callback(output)

            cycle_time = time.time() - cycle_start

            # Do not perform any time shortcut if cycle takes too long to finish
            if cycle_time > config['refresh_rate']:
                print('Warning: Cycle behind, forcing cycle restart')
                cycle_time = 0

            # Substract cycle time to ensure constant refresh
            time.sleep(max(0, config['refresh_rate'] - cycle_time))
    
    p.start(loop)
    return p

def run(command: str) -> list[int, str]:
    '''
    Runs a shell command in a PS context.
    '''

    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )

        text = result.stdout if result.returncode <= 0 else result.stderr
        return [result.returncode, text.strip()]

    except Exception as err:
        return [1, repr(err)]

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

# EOF