# Prometheus的使用：编写自己的exporter

> 以memcached为例

## 一、监控指标

​    列出需要搜集的指标和含义：

| 指标（Metrics）  | 说明            |
| ---------------- | --------------- |
| curr_items       | 当前key数量     |
| uptime           | 运行时间        |
| curr_connections | 当前连接数      |
| cmd_get          | get命令执行次数 |
| cmd_set          | set命令执行次数 |
| get_hits         | get命令命中次数 |
| storebytes       | 存储内存大小    |
| limit_maxbytes   | 最大内存        |

## 二、Exporter介绍

​    Prometheus Exporter以一个HTTP的服务的形式，将采集到的指标以Prometheus的规范，返回监控的样本数据。以Node Exporter为例，当访问`/metrics`地址时会返回以下内容：

```shell
# HELP node_cpu Seconds the cpus spent in each mode.
# TYPE node_cpu counter
node_cpu{cpu="cpu0",mode="idle"} 262142.1090415
```

​    Exporter返回的样本数据，主要由三个部分组成：样本的一般注释信息（HELP），样本的类型注释信息（TYPE）和样本。Prometheus会对Exporter响应的内容逐行解析。

​    官方支持的Exporter可以参考 https://prometheus.io/docs/instrumenting/exporters/ 。

# 三、自定义Exporter

​    自定义Exporter可以按照如下几个步骤：

1、获取监控目标的指标。比如使用memcached python客户端连接memcached实例，执行stats命令获取到当前memcached实例的运行指标。

```python
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
```

2、暴露HTTP服务。按照Prometheus的规范，使用如Flask、Fastapi等库开发`/metrics` GET接口。

```python
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
```

3、Prometheus配置连接这个Exporter。

## 四、展示和报警

​    采集到上述指标后，可以在Grafna中编写PromSQL去制作可视化的图标。比如内存使用率、item数等等。

![image-20201224163622388](C:\Users\relvr\AppData\Roaming\Typora\typora-user-images\image-20201224163622388.png)

​    比如uptime可以通过 max(max_over_time(uptime{instance=~"$instance"}[$__interval])) 获取。对于每个数据的展示方式可以根据实际业务关注的点去做优化，以上仅仅是示例。

​    报警使用的是Grafna的Alert模块，配置自己的Alert channels去接受报警信息。

## 五、写在最后

​    编写自己的exporter在业务重要指标监控中有重要的作用。可以从项目的维度提取出关注的metrics，制作自己的监控大屏。本篇文章代码地址：https://github.com/Rayzhsre/memcached_exporter