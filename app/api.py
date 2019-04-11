from flask import Blueprint, jsonify, current_app, request
from datetime import datetime as dt
import datetime
from hashlib import sha1

from .cache import cache
from .conf import blacklist

api = Blueprint("api", __name__)


@api.route("/api/query/<host>")
def api_query(host):
    if cache.get(host):
        r = cache.get(host)
        tz_local = datetime.timezone(datetime.timedelta(hours=current_app.config['TIME_ZONE']))
        times = dt.fromtimestamp(r["time"], tz = tz_local)
        r["time_readable"] = times.strftime("%Y-%m-%d %H:%M:%S")
        r["host"] = host
        return jsonify(r)
    else:
        return jsonify({"error": "no such host info"})


@api.route("/api/hosts")
def api_hosts():
    hosts = cache.get("all")
    corre = {}
    for h in hosts:
        corre[h] = cache.get(h)["ip"]
    return jsonify(corre)


@api.route("/api/apply/<host>", methods=["POST"])
def api_apply(host):
    if host in blacklist:
        return jsonify({"error": "your host name is not supported"})

    if not request.json:
        return jsonify({"error": "fail to autheticate the ip record"})

    passwd = sha1((host + current_app.config["AUTH_SALT"]).encode('utf-8')).hexdigest()
    if passwd != request.json.get("auth"):
        return jsonify({"error": "fail to autheticate the ip record"})

    info = {}
    now = dt.now()
    info["time"] = now.timestamp()

    ip = request.json.get("ip")
    if not ip:
        ip = request.remote_addr
        current_app.logger.info("use default ip of the sender")
    info["ip"] = ip
    old = cache.get(host)
    if not old:
        current_app.logger.info("ip has been created for %s" % host)
    elif old["ip"] != ip:
        current_app.logger.info("ip has been changed for %s" % host)
    cache.set(host, info)
    hosts = cache.get("all")
    if not hosts:
        hosts = [host]
    elif host not in hosts:
        hosts.append(host)
    cache.set("all", hosts)
    return jsonify({"success": "the ip for %s is updated" % host})
