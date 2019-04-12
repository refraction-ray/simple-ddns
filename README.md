# Usage

## Server side

Just `./run.sh` or use gunicorn to run the flask app if you like.

### Configurations

One can change the default configuration in `config.yaml` or write in `config_override.yaml` to overwrite the corresponding default options.

* CACHE_TYPE: `simple`, `fs` and `redis` are supported, which utilize memory, file and redis db as cache backend respectively. If fs or redis cache is configured, further cache related options should be set, see `app/cache.py` for details.
* CACHE_TIMEOUT: the storage time of ip address, 0 for no time out
* AUTH_SALT: the password for ip registration.
* TIME_ZONE: keep the server and client sync when talking about time, eg. 8 for Asia/Beijing
* PROXY_SETTING: 0 for no proxy, 1 for nginx as the reverse proxy of the app, remember editing the config of nginx to add the line `proxy_set_header X-Real-IP $remote_addr;` in the corresponding server part.
* CACHE_KEY: no real meaning, any string to avoid key collsion for general usage
* LOG_ITEMS: determine how many items are recorded as history change

## Client side

Firstly, one should make sure python package click and requests as well as *nix CLI tool curl and jq are installed on your system.

To notify your ip with the server, try `python3 client/regip.py -h hostname -s serverip -p authcode`.

You can add this command to crontab to keep the server sync with the ip address of local machines.

Getting the ip of given host is as simple as `curl -s serverip/api/query/hostname|jq --raw-out .ip`.

*Note: serverip should include the protocol head, i.e `http://` or `https://`. For example, serverip can be in the form https://example.com or http://8.8.8.8*.