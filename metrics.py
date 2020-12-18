# -*- coding: utf-8 -*-
"""
    Prometheus memcached exporter.
    Created by Rayzh.
"""
import memcache

class MemcacheStat:
    def __init__(self, hostport):
        self.mc = memcache.Client(hostport, debug=0)

    def stats(self):
        stat = self.mc.get_stats()
        res = stat[0][1]
        ret = dict()

        ret['curr_items'] = res['curr_items']
        ret['uptime'] = res["uptime"]
        ret['curr_connections'] = res['curr_connections']
        ret['cmd_get'] = res['cmd_get']
        ret['get_hits'] = res['get_hits']
        ret['cmd_set'] = res['cmd_set']
        ret['storebytes'] = res['bytes']
        ret['limit_maxbytes'] = res['limit_maxbytes']

        return ret