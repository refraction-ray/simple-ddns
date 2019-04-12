import click
import requests


@click.command()
@click.option("-i", "--input", default="/etc/hosts",
              help="Input file to be updated")
@click.option("-o", "--output", default="",
              help="Output file for the updated version")
@click.option('-s', '--server',
              help='the ddns server to update hosts')
def main(input, output, server):
    r = requests.get(server + "/api/hosts")
    if not r:
        click.echo("no hosts to update")
        return
    if not output:
        output = input

    newhost = []
    r = r.json()
    r_keys = [k for k in r.keys()]

    chg = False

    with open(input, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                newhost.append(line)
            else:
                hostname = line.split(" ")[-1]
                hostname = hostname.split("\t")[-1]
                if hostname not in r_keys:
                    newhost.append(line)
                else:
                    chg = True
                    newhost.append(r[hostname] + "  " + hostname)

    if chg is True:
        with open(output, "w+") as f:
            for line in newhost:
                f.write(line + "\n")
        click.echo("The host is successfully updated to %s" % output)
    else:
        click.echo("Nothing needs to update")


if __name__ == "__main__":
    main()
