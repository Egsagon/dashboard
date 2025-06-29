# This script was designed to be run by pythonw.exe in
# the Task Scheduler, hence the pipe redirection.

import sys
import logging

sys.stdout = sys.stderr = open(f'app.log', 'a', encoding = 'utf-8')
logging.basicConfig(
    level = 'INFO',
    format = '%(asctime)-17s │ %(levelname)-8s │ %(name)-6s │ %(message)s',
    datefmt = '%H:%M:%S %d/%m/%y'
)

# Start server
import host.server
logging.info(f'Starting server')

host.server.socket.run(
    app = host.server.app,
    debug = False,
    host = '0.0.0.0',
    port = host.server.utils.config['port'],
    certfile = 'cert/cert.pem',
    keyfile = 'cert/key.pem'
)

# EOF