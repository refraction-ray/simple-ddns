from flask import Blueprint, jsonify, current_app, request
from datetime import datetime as dt
import datetime
from hashlib import sha1

from .cache import cache

api = Blueprint("api", __name__)


@api.route("/api/query/<host>")
def api_query(host):
    hostkey = current_app.config["CACHE_KEY"] + host
    r = cache.get(hostkey)
    if r:
        tz_local = datetime.timezone(datetime.timedelta(hours=current_app.config['TIME_ZONE']))
        times = dt.fromtimestamp(r["time"], tz=tz_local)
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
        hkey = current_app.config["CACHE_KEY"]+h
        corre[h] = cache.get(hkey)["ip"]
    return jsonify(corre)


@api.route("/api/apply/<host>", methods=["POST"])
def api_apply(host):
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
        if current_app.config["PROXY_SETTING"] == 0:
            ip = request.remote_addr
        elif current_app.config["PROXY_SETTING"] == 1 or current_app.config["PROXY_SETTING"] == "nginx":
            ip = request.headers.get("X-Real-IP")
        current_app.logger.info("use default ip of the sender")
    info["ip"] = ip
    old = cache.get(host)
    if not old:
        current_app.logger.info("ip has been created for %s" % host)
    elif old["ip"] != ip:
        current_app.logger.info("ip has been changed for %s" % host)
    hostkey = current_app.config["CACHE_KEY"]+host
    cache.set(hostkey, info)
    hosts = cache.get("all")
    if not hosts:
        hosts = [host]
    elif host not in hosts:
        hosts.append(host)
    cache.set("all", hosts)
    return jsonify({"success": "the ip for %s is updated" % host})
