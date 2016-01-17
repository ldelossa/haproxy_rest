import json
from haproxy_rest.haproxy_cls import HaProxy
from operator import itemgetter

ha = HaProxy('/var/run/haproxysock')
out = ha.send_command('show stat')
key = out.split()[1:2][0].split(',')
values = out.split()[2:]

stats_list = []
for value in values:
    value_list = value.split(',')
    new_dict = {value_list[0]: {value_list[1]: dict(zip(key[2:], value_list[2:]))}}
    stats_list.append(new_dict)
