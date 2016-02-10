config = """global
    log 127.0.0.1 local1 notice
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon
    stats socket /var/run/haproxysock level admin

defaults
    log global
    mode http
    option httplog
    option dontlognull
    option forwardfor
    option http-server-close
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend frontend1
    bind 127.0.0.1:80
    option tcplog
    default_backend backend

frontend frontend2
    bind 127.0.0.2:80
    option tcplog
    default_backend backend

backend backend
    balance roundrobin
    server redirect01 192.168.122.112:80 check
    server redirect02 192.168.122.202:80 check

listen stats 127.0.0.1:1936
    mode http
    stats enable
    stats uri /
    stats hide-version
    stats auth user:user"""

class StateMachine:
    def __init__(self):
        self.cur_state = 'start'
        self.cur_frontend = None
        self.cur_backend = None
        self.states = ['global', 'defaults', 'backend', 'frontend', 'listen']
        self.global_dict = {'global': []}
        self.defaults_dict = {'defaults': []}
        self.frontend_dict = {}
        self.backend_dict = {}

    def _keyword_check(self, line):
        keyword = line.split()[0]

        if keyword == 'global':
            print("state changed to global")
            self.cur_state = 'global'
        if keyword == 'defaults':
            print("state changed to defaults")
            self.cur_state = 'defaults'
        if keyword == 'backend':
            print("state changed to backend")
            self.cur_state = 'backend'
            self.cur_backend = line.split()[1]
        if keyword == 'frontend':
            print("state changed to frontend")
            self.cur_state = 'frontend'
            self.cur_frontend = line.split()[1]
            print(self.cur_frontend)

    def start_handler(self, line):
        self._keyword_check(line)

    def global_handler(self, line):
        self._keyword_check(line)
        if self.cur_state != 'global':
            return
        self.global_dict['global'].append(line.split())

    def defaults_handler(self, line):
        self._keyword_check(line)
        if self.cur_state != 'defaults':
            return
        self.defaults_dict['defaults'].append(line.split())

    def frontend_handler(self, line):
        self._keyword_check(line)
        if self.cur_state != 'frontend':
            return

        try:
            self.frontend_dict[self.cur_frontend].append(line.split())
        except LookupError:
            self.frontend_dict[self.cur_frontend] = []
            self.frontend_dict[self.cur_frontend].append(line.split())

    def backend_handler(self,line):
        self._keyword_check(line)
        if self.cur_state != 'backend':
            return

        try:
            self.backend_dict[self.cur_backend].append(line.split())
        except LookupError:
            self.backend_dict[self.cur_backend] = []
            self.backend_dict[self.cur_backend].append(line.split())


    def run(self, line):
        if self.cur_state == 'start':
            self.start_handler(line)
        elif self.cur_state == 'global':
            self.global_handler(line)
        elif self.cur_state == 'defaults':
            self.defaults_handler(line)
        elif self.cur_state == 'frontend':
            self.frontend_handler(line)
        elif self.cur_state == 'backend':
            self.backend_handler(line)

fsm = StateMachine()
for line in config.split("\n"):
    if len(line) >= 1:
        fsm.run(line)

print(fsm.global_dict)
print(fsm.defaults_dict)
print(fsm.frontend_dict)
print(fsm.backend_dict)
