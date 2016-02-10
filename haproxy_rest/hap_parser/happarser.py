from pyparsing import *
ParserElement.setDefaultWhitespaceChars(' \t')

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

frontend frontend
    bind 127.0.0.1:80
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
# print(config)

new_line = LineEnd()
word = Word(alphanums+"/-:.")
global_block = Keyword('global') + new_line.suppress() + OneOrMore(Group(OneOrMore(word) + new_line.suppress()))
default_block = new_line.suppress() + Keyword('defaults') + new_line.suppress() + OneOrMore(Group(OneOrMore(word) + new_line.suppress()))

print(global_block.parseString(config))
print((global_block + default_block).parseString(config))
