import socket
import logging
import host.server

PORT = 8808

logging.basicConfig(
    level = 'INFO',
    format = '%(levelname)-8s %(name)-6s :: %(message)s'
)

# Get local IP
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect(('1.1.1.1', 80))
ip = conn.getsockname()[0]
conn.close()

logging.info(f'Server running on https://{ip}:{PORT}')

host.server.socket.run(
    app = host.server.app,
    debug = False,
    host = '0.0.0.0',
    port = PORT,
    certfile = 'cert/cert.pem',
    keyfile = 'cert/key.pem'
)

# EOF