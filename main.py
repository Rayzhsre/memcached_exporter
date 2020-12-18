# -*- coding: utf-8 -*-
"""
    Created by Rayzh.
"""

from prometheus_client import generate_latest, Gauge, CollectorRegistry
from metrics import MemcacheStat
from flask import Response, Flask
import json
import os

app = Flask(__name__)


@app.route("/")
def index():
    return 'prometheus memcached exporter'


@app.route("/metrics")
def memcachedResponse():
    crr_items.set(stats['curr_items'])
    uptime.set(stats['uptime'])
    crr_connections.set(stats['curr_connections'])
    cmd_get.set(stats['cmd_get'])
    get_hits.set(stats['get_hits'])
    cmd_set.set(stats['cmd_set'])
    storebytes.set(stats['storebytes'])
    limit_maxbytes.set(stats['limit_maxbytes'])

    return Response(generate_latest(REGISTRY), mimetype="text/plain")


if __name__ == '__main__':
    REGISTRY = CollectorRegistry(auto_describe=False)
    #  memcached stats
    memcached_hostport = os.environ.get('memcached_hostport')
    if not memcached_hostport:
        memcached_hostport = ['localhost:21220']

    st = MemcacheStat(memcached_hostport)
    stats = st.stats()

    crr_items = Gauge('curr_items', 'current items', registry=REGISTRY)
    uptime = Gauge('uptime', 'uptime', registry=REGISTRY)
    crr_connections = Gauge('curr_connections', 'current connections', registry=REGISTRY)
    cmd_get = Gauge('cmd_get', 'cmd_get', registry=REGISTRY)
    get_hits = Gauge('get_hits', 'get_hits', registry=REGISTRY)
    cmd_set = Gauge('cmd_set', 'cmd_set', registry=REGISTRY)
    storebytes = Gauge('storebytes', 'storebytes', registry=REGISTRY)
    limit_maxbytes = Gauge('limit_maxbytes', 'maxbytes', registry=REGISTRY)

    app.run(host="0.0.0.0")