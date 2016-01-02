#!/usr/bin/env python3
"""
Usage:
  port-scan --host HOST --port PORT
  port-scan (-h | --help)

Options:
  --host HOST   : Hostname
  --port PORT   : Port

"""
import sys
import socket
from docopt import docopt

__author__ = 'Gokhan MANKARA <gokhan@mankara.org>'


def main(h, p):

    print("Connecting HOST: {} PORT: {}".format(h, p))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((h, int(p)))

    if 0 == result:
        print("Port {} ACTIVE for {}".format(p, h))
    else:
        print("Port {} NOT ACTIVE for {}".format(p, h))

if __name__ == "__main__":
    args = docopt(__doc__)

    host = args['--host']
    port = args['--port']

    main(host, port)
