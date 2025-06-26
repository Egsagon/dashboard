import host.server

host.server.socket.run(
    app = host.server.app,
    host = '0.0.0.0',
    port = 8808
)

# EOF