class Socket_Action():
    def __init__(self, haproxy_inst):
        self.haproxy = haproxy_inst

    def __enter__(self):
        self.haproxy._connect_to_socket()
        return self.haproxy

    def __exit__(self, type, value, traceback):
        self.haproxy.socket.close()

