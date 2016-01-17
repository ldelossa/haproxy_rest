import socket
from time import sleep
from haproxy_rest.functions import Socket_Action


class HaProxy(object):
    def __init__(self, socket_file):
        self.socket_file = socket_file
        self.socket_type = socket.AF_UNIX
        self.socket_stream = socket.SOCK_STREAM
        self.socket = None
        self.info = None

    def _connect_to_socket(self):
        self.socket = socket.socket(self.socket_type, self.socket_stream)
        self.socket.connect(self.socket_file)

    def _get_info(self):
        info_dict = self.send_command('show info')
        info_dict = info_dict.split('\n')
        info_dict = [x.split(': ') for x in info_dict]
        info_dict = {key: value for key, *value in info_dict if len(value) > 0}
        self.info = info_dict


    def send_command(self, cmd):
        with Socket_Action(self):
            cmd += '\n'
            self.socket.send(cmd.encode('utf-8'))
            data = self.socket.recv(8192)

        return data.decode('ASCII')

    def disable_server(self, input_dict):
        # self._connect_to_socket()

        with Socket_Action(self):
            backend = input_dict['backend']
            server = input_dict['server']
            stats = list(self.get_stats(backend, server))[0]
            command = 'disable server {}/{}'.format(backend, server)
            self.send_command(command)

            while int(stats['scur']) > 0:
                sleep(.1)
        return


    def enable_server(self, input_dict):

        with Socket_Action(self):
            backend = input_dict['backend']
            server = input_dict['server']
            command = 'enable server {}/{}'.format(backend, server)
            self.send_command(command)



    def get_stats(self, type, svname=None):
        with Socket_Action(self):
            out = self.send_command('show stat')
            key = out.split()[1:2][0].split(',')
            values = out.split()[2:]

            stats_list = []
            for value in values:
                value_list = value.split(',')
                new_dict = {value_list[0]: {value_list[1]: dict(zip(key[2:], value_list[2:]))}}
                stats_list.append(new_dict)

            if svname is None:
                for stats in stats_list:
                    try:
                        yield stats[type]
                    except KeyError:
                        pass

            for stats in stats_list:
                try:
                    if stats[type][svname]:
                        yield stats[type][svname]
                except KeyError:
                    pass


