import socket
import host.server

HOST = '0.0.0.0'
PORT = 8808

# Get self IP
# conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# conn.connect(('1.1.1.1', 80))
# ip = conn.getsockname()[0]
# conn.close()
# print(f'Server running on http://{ip}:{PORT}')

host.server.run(HOST, PORT)

# EOF