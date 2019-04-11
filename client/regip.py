"""
add this script to crontab to make sure the ip is correctly updated on the server side

for the querying part, it is not necesary to write things in python, just one line bash:
say if you want to ping host1 without knowing its ip, try (make sure jq is installed)
ping `curl -s <serverip>/api/query/host1|jq --raw-output .ip`
"""

import click
import requests
from hashlib import sha1


def passwd(host, auth):
    return sha1((host + auth).encode('utf-8')).hexdigest()


@click.command()
@click.option('-s', '--server', help='the ddns server to update ip')
@click.option('-h', '--hostname', help='hostname of local machine')
@click.option('-p', '--password', help='the authetication code of ddns server',
              prompt=True, hide_input=True)
def main(server, hostname, password):
    r = requests.post(server + "/api/apply/" + hostname,
                      json={"auth": passwd(hostname, password)})

    try:
        click.echo(r.json())
    except Exception:
        click.echo("something must go wrong")


if __name__ == "__main__":
    main()
